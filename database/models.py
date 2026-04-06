from typing import List, Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String
import uuid

# Class ini yang bakal otomatis jadi tabel "projects" di Supabase
class Project(SQLModel, table=True):
    __tablename__ = "projects" # Nama tabelnya

    # Pake UUID biar ID-nya random dan aman
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    title: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    description: str
    cover_image_url: str
    
    # Cara khusus declare Postgres Array di SQLModel
    features: List[str] = Field(default=[], sa_column=Column(ARRAY(String)))
    tech_stack: List[str] = Field(default=[], sa_column=Column(ARRAY(String)))
    screenshots: List[str] = Field(default=[], sa_column=Column(ARRAY(String)))
    
    live_demo_url: Optional[str] = None
    github_url: Optional[str] = None
    project_duration: str
    team_size: int
    project_year: int
    
    is_published: bool = Field(default=False)