from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from database.connection import get_session
from database.models import Project
from schemas.project_schema import ProjectCreate, ProjectUpdate
from services import project_service

from core.security import verify_token

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)

@router.get("/", response_model=List[Project])
def read_projects(db: Session = Depends(get_session)):
    return project_service.get_all_projects(db)

@router.get("/{project_id}", response_model=Project)
def read_project_by_id(project_id: str, db: Session = Depends(get_session)):
    return project_service.get_project_by_id(db, project_id)

@router.get("/slug/{slug}", response_model=Project)
def read_project_by_slug(slug: str, db: Session = Depends(get_session)):
    return project_service.get_project_by_slug(db, slug)

@router.post("/", response_model=Project)
def create_project(
    project: ProjectCreate, 
    db: Session = Depends(get_session),
    user_data: dict = Depends(verify_token)
):
    return project_service.create_new_project(db, project)

@router.patch("/{project_id}", response_model=Project)
def update_project(
    project_id: str,
    project: ProjectUpdate,
    db: Session = Depends(get_session),
    user_data: dict = Depends(verify_token)
):
    return project_service.update_project(db, project_id, project)

@router.delete("/{project_id}")
def delete_project(
    project_id: str,
    db: Session = Depends(get_session),
    user_data: dict = Depends(verify_token)
):
    return project_service.delete_project(db, project_id)