from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db, AsyncSessionLocal
from app.db.models import Run
from app.schemas.run import RunCreate, RunResponse, RunStatusResponse
import uuid
import asyncio
import json

from app.graph.main_graph import graph
from app.graph.state import GraphState
from app.schemas.project import StartupIdea, ProjectVersion
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType
from datetime import datetime
from pathlib import Path

router = APIRouter()
REPORTS_DIR = Path(__file__).resolve().parents[3] / "outputs" / "reports"

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
                # Save final state to DB for history/reports
                
                # Make sure to convert any non-serializable objects inside final_state if needed, 
                # but graph states should be mostly serializable. We might need to dict-ify BaseModel instances.
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
                data={"errors": final_state['errors']}
            ))
        else:
            await event_bus.publish(AppEvent(
                event_type=EventType.EXECUTION_COMPLETED,
                run_id=run_id,
                timestamp=datetime.utcnow(),
                data={"message": "Run completed successfully."}
            ))

    except Exception as e:
        print(f"Graph execution failed: {e}")
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
            data={"errors": [str(e)]}
        ))


@router.post("/", response_model=RunResponse)
async def start_run(run_data: RunCreate, db: AsyncSession = Depends(get_db)):
    run_id = uuid.uuid4()
    
    try:
        parsed_project_id = uuid.UUID(run_data.project_id) if run_data.project_id else None
    except ValueError:
        # Invalid UUID string provided; treat as no project ID
        parsed_project_id = None
    
    if parsed_project_id:
        from app.db.models import Project
        query = select(Project).where(Project.id == parsed_project_id)
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            dummy_proj = Project(id=parsed_project_id, name="Auto-created Project")
            db.add(dummy_proj)
            await db.commit()

    # Store run metadata
    idea_payload = {
        "idea": run_data.idea,
        "problem_statement": run_data.problem_statement,
        "target_users": run_data.target_users,
        "revenue_model": run_data.revenue_model,
    }
    new_run = Run(
        id=run_id,
        project_id=parsed_project_id,
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
async def execute_run(run_id: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Run).where(Run.id == uuid.UUID(run_id))
        result = await db.execute(query)
        run = result.scalar_one_or_none()
        
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
            
        background_tasks.add_task(
            execute_graph_run, 
            str(run.id), 
            str(run.project_id) if run.project_id else str(uuid.uuid4()), 
            run.idea or "Unknown"
        )
        return {"status": "execution_started", "run_id": run_id}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid run_id format")

@router.get("/{run_id}", response_model=RunStatusResponse)
async def get_run_status(run_id: str, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Run).where(Run.id == uuid.UUID(run_id))
        result = await db.execute(query)
        run = result.scalar_one_or_none()
        
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
            
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
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid run_id format")

@router.get("/{run_id}/report")
async def get_run_report(run_id: str):
    manifest_path = REPORTS_DIR / f"manifest_{run_id}.json"
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
async def list_runs(db: AsyncSession = Depends(get_db)):
    query = select(Run).order_by(Run.created_at.desc())
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
