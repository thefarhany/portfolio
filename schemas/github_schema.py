from pydantic import BaseModel
from typing import Optional

class GithubRepo(BaseModel):
    id: int
    name: str
    html_url: str
    description: Optional[str] = None
    language: Optional[str] = None
    stargazers_count: int
    forks_count: int
    
class GithubStats(BaseModel):
    followers: int
    following: int
    public_repos: int