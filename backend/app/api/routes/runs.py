from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db, AsyncSessionLocal
from app.db.models import Run, User
from app.schemas.run import RunCreate, RunResponse, RunStatusResponse
from app.core.auth import get_current_user
from app.core.settings import settings
from app.core.rate_limit import limiter
from app.core.ai_limits import ai_limits_manager
from app.core.security_logging import log_security_event
import uuid
import asyncio
import json
import logging

from app.graph.main_graph import graph
from app.graph.state import GraphState
from app.schemas.project import StartupIdea, ProjectVersion
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType
from datetime import datetime
from pathlib import Path

router = APIRouter()
REPORTS_DIR = Path(__file__).resolve().parents[3] / "outputs" / "reports"
run_logger = logging.getLogger("kurukshetra.runs")

def parse_idea_payload(raw_idea: str) -> dict:
    try:
        payload = json.loads(raw_idea or "{}")
        if isinstance(payload, dict) and payload.get("idea"):
            return payload
    except Exception:
        pass
    return {"idea": raw_idea or "Unknown"}

def infer_company_name(idea_text: str) -> str:
    clean = (idea_text or "Unknown").strip()
    if not clean:
        return "Unknown"
    return clean.splitlines()[0].strip()[:80]

async def execute_graph_run(run_id: str, project_id: str, idea_text: str):
    # This runs in background
    try:
        # Emit RUN_STARTED
        await event_bus.publish(AppEvent(
            event_type=EventType.RUN_STARTED,
            run_id=run_id,
            timestamp=datetime.utcnow(),
            data={"message": f"Run {run_id} started."}
        ))
        
        payload = parse_idea_payload(idea_text)
        concept = payload.get("idea") or idea_text or "Unknown"
        idea = StartupIdea(
            company_name=payload.get("company_name") or infer_company_name(concept),
            business_concept=concept,
            industry=payload.get("industry") or "Unknown",
            problem_statement=payload.get("problem_statement"),
            target_users=payload.get("target_users"),
            revenue_model=payload.get("revenue_model")
        )
        version = ProjectVersion(version_tag="v1.0", idea=idea)
        
        initial_state = GraphState(
            run_id=run_id,
            project_id=project_id,
            startup_idea=idea,
            idea_version=version,
            commander_output=None,
            scout_output=None,
            analyst_output=None,
            treasury_output=None,
            critic_output=None,
            swot_analysis=None,
            gtm_strategy=None,
            debate_records=[],
            battle_score=None,
            battle_verdict=None,
            confidence_score=None,
            final_report=None,
            pivot_mandated=False,
            errors=[],
            execution_logs=[]
        )
        
        final_state = await graph.ainvoke(initial_state)
        
        # Update DB status
        async with AsyncSessionLocal() as session:
            query = select(Run).where(Run.id == uuid.UUID(run_id))
            result = await session.execute(query)
            run = result.scalar_one_or_none()
            if run:
                run.status = "failed" if final_state.get('errors') else "completed"
                
                def serialize_obj(obj):
                    if hasattr(obj, "model_dump"):
                        return obj.model_dump()
                    elif isinstance(obj, list):
                        return [serialize_obj(i) for i in obj]
                    elif isinstance(obj, dict):
                        return {k: serialize_obj(v) for k, v in obj.items()}
                    return obj
                
                serialized_state = serialize_obj(final_state)
                run.final_state = serialized_state
                await session.commit()
                
        # Emit EXECUTION_COMPLETED or FAILED
        if final_state.get('errors'):
            await event_bus.publish(AppEvent(
                event_type=EventType.EXECUTION_FAILED,
                run_id=run_id,
                timestamp=datetime.utcnow(),
                data={"errors": ["Simulation encountered an internal error during execution."]}
            ))
        else:
            await event_bus.publish(AppEvent(
                event_type=EventType.EXECUTION_COMPLETED,
                run_id=run_id,
                timestamp=datetime.utcnow(),
                data={"message": "Run completed successfully."}
            ))

    except Exception as e:
        run_logger.error(f"Graph execution failed for run {run_id}: {e}", exc_info=True)
        async with AsyncSessionLocal() as session:
            query = select(Run).where(Run.id == uuid.UUID(run_id))
            result = await session.execute(query)
            run = result.scalar_one_or_none()
            if run:
                run.status = "failed"
                await session.commit()
                
        await event_bus.publish(AppEvent(
            event_type=EventType.EXECUTION_FAILED,
            run_id=run_id,
            timestamp=datetime.utcnow(),
            data={"errors": ["Simulation failed. Please verify provider connectivity and retry."]}
        ))


@router.post("/", response_model=RunResponse)
@limiter.limit(f"{settings.ai_rate_limit * 2}/minute")
async def start_run(
    request: Request,
    run_data: RunCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ip = request.client.host if request.client else "unknown"

    # Enforce AI Kill Switch
    if not settings.ai_enabled:
        log_security_event(
            event_type="KILL_SWITCH_ACTIVE",
            ip=ip,
            user_id=str(current_user.id),
            details={"action": "start_run_blocked"},
            severity="WARNING"
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI services are temporarily disabled by the administrator."
        )

    # Check daily quota
    current_usage = ai_limits_manager.get_user_daily_usage(str(current_user.id))
    if current_usage >= settings.ai_daily_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Daily AI usage limit of {settings.ai_daily_limit} runs exceeded. Quota resets at 00:00 UTC."
        )

    run_id = uuid.uuid4()
    
    parsed_project_id = None
    if run_data.project_id:
        try:
            parsed_project_id = uuid.UUID(run_data.project_id)
        except ValueError:
            parsed_project_id = None
    
    if parsed_project_id:
        from app.db.models import Project
        query = select(Project).where(Project.id == parsed_project_id)
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            dummy_proj = Project(id=parsed_project_id, name="Auto-created Project")
            db.add(dummy_proj)
            await db.commit()

    # Store run metadata, linked to the authenticated user
    idea_payload = {
        "idea": run_data.idea.strip(),
        "problem_statement": run_data.problem_statement.strip() if run_data.problem_statement else None,
        "target_users": run_data.target_users.strip() if run_data.target_users else None,
        "revenue_model": run_data.revenue_model.strip() if run_data.revenue_model else None,
    }
    new_run = Run(
        id=run_id,
        project_id=parsed_project_id,
        user_id=current_user.id,
        idea=json.dumps(idea_payload),
        status="created"
    )
    db.add(new_run)
    await db.commit()
    await db.refresh(new_run)
    
    return RunResponse(
        run_id=str(new_run.id),
        project_id=str(new_run.project_id) if new_run.project_id else None,
        idea=run_data.idea,
        status=new_run.status,
        created_at=new_run.created_at
    )

@router.post("/{run_id}/execute")
@limiter.limit(f"{settings.ai_rate_limit}/minute")
async def execute_run(
    request: Request,
    run_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ip = request.client.host if request.client else "unknown"

    # Validate UUID format strictly
    try:
        run_uuid = uuid.UUID(run_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid run_id format")

    # Enforce AI Kill Switch & Daily Limit
    ai_limits_manager.check_and_increment(str(current_user.id), ip)

    query = select(Run).where(Run.id == run_uuid)
    result = await db.execute(query)
    run = result.scalar_one_or_none()
    
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
        
    # IDOR Check: Ensure run belongs to current authenticated user
    if run.user_id and run.user_id != current_user.id:
        log_security_event(
            event_type="AUTHZ_VIOLATION",
            ip=ip,
            user_id=str(current_user.id),
            details={"action": "execute_run", "target_run_id": run_id, "owner_id": str(run.user_id)},
            severity="WARNING"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not have permission to execute this run."
        )

    background_tasks.add_task(
        execute_graph_run, 
        str(run.id), 
        str(run.project_id) if run.project_id else str(uuid.uuid4()), 
        run.idea or "Unknown"
    )
    return {"status": "execution_started", "run_id": run_id}

@router.get("/{run_id}", response_model=RunStatusResponse)
async def get_run_status(
    run_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        run_uuid = uuid.UUID(run_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid run_id format")

    query = select(Run).where(Run.id == run_uuid)
    result = await db.execute(query)
    run = result.scalar_one_or_none()
    
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # IDOR Check: Ensure run belongs to current authenticated user
    if run.user_id and run.user_id != current_user.id:
        log_security_event(
            event_type="AUTHZ_VIOLATION",
            user_id=str(current_user.id),
            details={"action": "get_run_status", "target_run_id": run_id},
            severity="WARNING"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not have permission to view this run."
        )
        
    progress = 0
    if run.status == "completed":
        progress = 100
    elif run.status == "failed":
        progress = 0
    else:
        progress = 50 
        
    return {
        "run_id": str(run.id),
        "status": run.status,
        "progress": progress,
        "final_state": run.final_state
    }

@router.get("/{run_id}/report")
@limiter.limit("30/minute")
async def get_run_report(
    request: Request,
    run_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        run_uuid = uuid.UUID(run_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid run_id format")

    # IDOR Check: Ensure run belongs to current authenticated user
    query = select(Run).where(Run.id == run_uuid)
    result = await db.execute(query)
    run = result.scalar_one_or_none()
    
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    if run.user_id and run.user_id != current_user.id:
        log_security_event(
            event_type="AUTHZ_VIOLATION",
            user_id=str(current_user.id),
            details={"action": "get_run_report", "target_run_id": run_id},
            severity="WARNING"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not have permission to view this report."
        )

    # Path traversal protection: ensure file resides strictly inside REPORTS_DIR
    manifest_path = (REPORTS_DIR / f"manifest_{run_id}.json").resolve()
    try:
        if not manifest_path.is_relative_to(REPORTS_DIR.resolve()):
            raise HTTPException(status_code=400, detail="Invalid report path traversal detected")
    except AttributeError:
        # Python < 3.9 compatibility fallback
        if not str(manifest_path).startswith(str(REPORTS_DIR.resolve())):
            raise HTTPException(status_code=400, detail="Invalid report path traversal detected")

    if not manifest_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")

    with open(manifest_path, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)

    def to_web_path(path_value: str | None):
        if not path_value:
            return None
        return f"/outputs/reports/{Path(path_value).name}"

    return {
        "report_id": run_id,
        "manifest_path": f"/outputs/reports/{manifest_path.name}",
        "pdf_path": to_web_path(manifest.get("pdf_path")),
        "json_path": to_web_path(manifest.get("json_path")),
        "md_path": to_web_path(manifest.get("md_path")),
    }

@router.get("/")
async def list_runs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only return runs that belong to the authenticated user
    query = select(Run).where(Run.user_id == current_user.id).order_by(Run.created_at.desc())
    result = await db.execute(query)
    runs = result.scalars().all()
    
    run_list = []
    for r in runs:
        final_state = r.final_state or {}
        battle_score = final_state.get("battle_score")
        confidence_score = final_state.get("confidence_score")
        verdict = final_state.get("battle_verdict")
        
        run_list.append({
            "run_id": str(r.id),
            "project_id": str(r.project_id) if r.project_id else None,
            "idea": parse_idea_payload(r.idea).get("idea", r.idea),
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "battle_score": battle_score,
            "confidence_score": confidence_score,
            "verdict": verdict,
            "has_report": r.status == "completed" and bool(final_state)
        })
    return {"runs": run_list}
