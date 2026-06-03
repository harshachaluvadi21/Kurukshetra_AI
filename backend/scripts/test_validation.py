import asyncio
import uuid
from app.db.database import AsyncSessionLocal
from app.db.models import Project, ProjectVersion, Run
from sqlalchemy import select

async def run_tests():
    project_id = uuid.uuid4()
    version_id = uuid.uuid4()
    run_id = uuid.uuid4()
    
    json_data = {
        "idea": "AI Attendance System for Colleges",
        "market": "EdTech"
    }

    try:
        async with AsyncSessionLocal() as session:
            # Insert
            new_project = Project(id=project_id, name="Test Project")
            new_version = ProjectVersion(
                id=version_id, 
                project_id=project_id, 
                version_tag="v1", 
                concept=json_data
            )
            new_run = Run(
                id=run_id, 
                project_id=project_id, 
                project_version_id=version_id, 
                idea="test idea", 
                status="created",
                final_state={"some_key": "some_value"}
            )
            
            session.add(new_project)
            session.add(new_version)
            session.add(new_run)
            await session.commit()

            print("Insert successful.")

            # Retrieve Project
            res = await session.execute(select(Project).where(Project.id == project_id))
            p = res.scalar_one()
            print(f"Project UUID validation: {type(p.id)} - {p.id}")
            
            # Retrieve ProjectVersion
            res = await session.execute(select(ProjectVersion).where(ProjectVersion.id == version_id))
            pv = res.scalar_one()
            print(f"JSONB Concept Validation: {type(pv.concept)} - {pv.concept}")
            
            # Retrieve Run
            res = await session.execute(select(Run).where(Run.id == run_id))
            r = res.scalar_one()
            print(f"Run UUID validation: {type(r.id)} - {r.id}")
            
            print("Validation successful!")
            
    except Exception as e:
        print("Validation failed:", e)

if __name__ == "__main__":
    asyncio.run(run_tests())
