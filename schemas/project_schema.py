from sqlmodel import SQLModel
from typing import List, Optional

class ProjectCreate(SQLModel):
    title: str
    slug: str
    description: str
    cover_image_url: str
    features: List[str] = []
    tech_stack: List[str] = []
    screenshots: List[str] = []
    live_demo_url: Optional[str] = None
    github_url: Optional[str] = None
    project_duration: str
    team_size: int
    project_year: int
    is_published: bool = False
    
class ProjectUpdate(SQLModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    features: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
    screenshots: Optional[List[str]] = None
    live_demo_url: Optional[str] = None
    github_url: Optional[str] = None
    project_duration: Optional[str] = None
    team_size: Optional[int] = None
    project_year: Optional[int] = None
    is_published: Optional[bool] = None