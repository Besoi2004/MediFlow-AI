"""Tạo FastAPI app và gắn các router dưới /api."""
from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import auth, bookings, consultant, hospitals, packages

app = FastAPI(title="MediFlow API")

_MESSAGES = {
    "missing": "Bắt buộc",
    "string_too_short": "Cần ít nhất {min_length} ký tự",
    "string_too_long": "Tối đa {max_length} ký tự",
    "string_pattern_mismatch": "Sai định dạng",
    "greater_than_equal": "Phải từ {ge} trở lên",
    "less_than_equal": "Không được lớn hơn {le}",
}


def _message(err: dict) -> str:
    ctx = err.get("ctx") or {}
    if err["type"] == "value_error":
        return str(ctx["error"])  # ValueError trong schemas đã viết tiếng Việt
    template = _MESSAGES.get(err["type"])
    return template.format(**ctx) if template else "Giá trị không hợp lệ"


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    # loc = ("body" | "query" | "path", tên ô, ...): giao diện chỉ cần tên ô cuối cùng
    errors = [{"field": str(e["loc"][-1]) if len(e["loc"]) > 1 else "", "message": _message(e)} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": "Dữ liệu không hợp lệ", "errors": errors})

api = APIRouter(prefix="/api")


@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


api.include_router(auth.router)
api.include_router(hospitals.router)
api.include_router(packages.router)
api.include_router(bookings.router)
api.include_router(consultant.router)
app.include_router(api)
