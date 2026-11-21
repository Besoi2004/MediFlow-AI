"""Tạo FastAPI app và gắn các router dưới /api."""
from fastapi import APIRouter, FastAPI

app = FastAPI(title="MediFlow API")

api = APIRouter(prefix="/api")


@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api)
