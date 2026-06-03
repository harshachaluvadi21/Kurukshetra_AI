from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_project():
    return {"status": "placeholder"}

@router.get("/{project_id}")
async def get_project(project_id: str):
    return {"status": "placeholder", "id": project_id}
