from sqlmodel import Session, select
from database.models import Project
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from schemas.project_schema import ProjectCreate, ProjectUpdate

def check_unique_fields(db: Session, title: str = None, slug: str = None, exclude_id: str = None):
    if title:
        query = select(Project).where(Project.title == title)
        if exclude_id:
            query = query.where(Project.id != exclude_id)
        if db.exec(query).first():
            raise HTTPException(status_code=400, detail=f"Title '{title}' Already Exists!!")
            
    if slug:
        query = select(Project).where(Project.slug == slug)
        if exclude_id:
            query = query.where(Project.id != exclude_id)
        if db.exec(query).first():
            raise HTTPException(status_code=400, detail=f"Slug '{slug}' Already Exists!!")


def get_all_projects(db: Session):
    statement = select(Project)
    results = db.exec(statement).all()
    return results

def create_new_project(db: Session, project_data: ProjectCreate):
    check_unique_fields(db, title=project_data.title, slug=project_data.slug)
    
    db_project = Project.model_validate(project_data)
    
    try:
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Waduh, data ini udah ada di database bro! Coba ganti yang lain."
        )

def get_project_by_id(db: Session, project_id: str):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project nggak ketemu bro!")
    return project

def get_project_by_slug(db: Session, slug: str):
    statement = select(Project).where(Project.slug == slug)
    project = db.exec(statement).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project nggak ketemu bro!")
    return project

def update_project(db: Session, project_id: str, project_data: ProjectUpdate):
    db_project = get_project_by_id(db, project_id)
    
    check_unique_fields(
        db, 
        title=project_data.title, 
        slug=project_data.slug, 
        exclude_id=project_id
    )
    
    update_data = project_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_project, key, value)
        
    try:
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Data bentrok sama yang udah ada di database bro!")

def delete_project(db: Session, project_id: str):
    db_project = get_project_by_id(db, project_id)
    
    db.delete(db_project)
    db.commit()
    return {"message": "Project berhasil dihapus bro!"}