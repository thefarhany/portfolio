import os
import requests
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()

def fetch_repositories(username: str):
    all_repos = []
    page = 1
    per_page = 100
    
    github_token = os.getenv("GITHUB_TOKEN")
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    if github_token:
        headers["Authorization"] = f"token {github_token}"
        
    try:
        while True:
            url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page={per_page}&page={page}"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 403:
                raise HTTPException(
                    status_code=403, 
                    detail="Waduh, kena limit Github API bro! Udah bener belom masukin tokennya?"
                )
                
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail="Waduh, gagal ngambil data dari Github nih bro."
                )
                
            data = response.json()
            
            if not data:
                break
                
            all_repos.extend(data)
            page += 1
            
        return all_repos
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Koneksi ke Github bermasalah: {str(e)}"
        )
        
def fetch_user_stats(username: str):
    github_token = os.getenv("GITHUB_TOKEN")
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    if github_token:
        headers["Authorization"] = f"token {github_token}"
        
    try:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 403:
            raise HTTPException(
                status_code=403, 
                detail="Waduh, kena limit Github API bro! Udah bener belom masukin tokennya?"
            )
            
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail="Waduh, gagal ngambil data profil Github nih bro."
            )
            
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Koneksi ke profil Github bermasalah: {str(e)}"
        )