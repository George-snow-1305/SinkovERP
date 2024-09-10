from fastapi import FastAPI
from handlers.projects import router as projects_router

app = FastAPI()

app.include_router(projects_router)