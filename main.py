from fastapi import FastAPI
from handlers.projects import router as projects_router
from pydantic import BaseModel


app = FastAPI()

app.include_router(projects_router)
