from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from database.connection import engine
from database.models import Project

from routers import projects
from routers import github
from routers import auth
from routers import upload

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Portfolio API", lifespan=lifespan)

app.include_router(projects.router)
app.include_router(github.router)
app.include_router(auth.router)
app.include_router(upload.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend Portfolio Online! 🚀"}