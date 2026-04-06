from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login_for_access_token(req: LoginRequest):
    supabase_url = os.getenv("SUPABASE_URL")

    auth_url = f"{supabase_url}/auth/v1/token?grant_type=password"
    headers = {
        "apikey": os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY", ""),
        "Content-Type": "application/json"
    }
    
    response = requests.post(auth_url, headers=headers, json={"email": req.email, "password": req.password})
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Login gagal bro! Cek email/password lu.")
        
    data = response.json()
    return {
        "access_token": data.get("access_token"),
        "token_type": "bearer"
    }
    
@router.post("/logout")
def logout(authorization: str = Header(...)):
    supabase_url = os.getenv("SUPABASE_URL")
    logout_url = f"{supabase_url}/auth/v1/logout"
    
    headers = {
        "apikey": os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY", ""),
        "Authorization": authorization
    }
    
    response = requests.post(logout_url, headers=headers)
    
    return {"message": "Sip bro, lo berhasil logout! Jangan lupa hapus token di frontend juga ya."}