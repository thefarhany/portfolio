from fastapi import APIRouter
from typing import List

from schemas.github_schema import GithubRepo, GithubStats
from services import github_service

router = APIRouter(
    prefix="/api/repositories",
    tags=["Github"]
)

@router.get("/", response_model=List[GithubRepo])
def get_my_github_repos():
    github_username = "thefarhany" 
    
    return github_service.fetch_repositories(github_username)

@router.get("/stats", response_model=GithubStats)
def get_my_github_stats():
    github_username = "thefarhany" 
    
    return github_service.fetch_user_stats(github_username)