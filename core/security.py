import os
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()

SUPABASE_URL = os.getenv("SUPABASE_URL")
ANON_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

JWKS_URL = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"

jwks_client = jwt.PyJWKClient(
    JWKS_URL,
    headers={"apikey": ANON_KEY}
)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        payload = jwt.decode(
            token, 
            signing_key.key, 
            algorithms=["ES256", "HS256", "RS256"],
            options={"verify_aud": False}
        )
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Waktu login lo udah habis bro, login lagi ya."
        )
    except jwt.PyJWKClientError as e:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Gagal ngambil public key dari Supabase: {str(e)}"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Token lo nggak valid nih: {str(e)}"
        )
