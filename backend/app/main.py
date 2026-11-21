"""Tạo FastAPI app và gắn các router dưới /api."""
from fastapi import APIRouter, FastAPI

from app.api import auth, hospitals, packages

app = FastAPI(title="MediFlow API")

api = APIRouter(prefix="/api")


@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


api.include_router(auth.router)
api.include_router(hospitals.router)
api.include_router(packages.router)
app.include_router(api)
