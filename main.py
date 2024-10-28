from fastapi import FastAPI
from handlers.projects import router as projects_router
from handlers.catalog import router as catalog_router
from handlers.operations import router as catalog_operations_router

app = FastAPI()

app.include_router(projects_router)
app.include_router(catalog_router)
app.include_router(catalog_operations_router)