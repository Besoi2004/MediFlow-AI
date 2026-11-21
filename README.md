# MediFlow-AI

Nền tảng đặt lịch gói khám sức khỏe định kỳ của nhiều bệnh viện (dữ liệu mô phỏng), có trợ lý AI tích hợp. Dự án học tập theo đề VMEC-15.

- Thiết kế: [docs/superpowers/specs/2026-11-21-mediflow-ai-design.md](docs/superpowers/specs/2026-11-21-mediflow-ai-design.md)
- Kế hoạch: [docs/superpowers/plans/](docs/superpowers/plans/)

## Cần có

Docker Desktop, Python 3.13 + [uv](https://docs.astral.sh/uv/), Node 22 + npm.

## Chạy local

```powershell
# 1. Postgres + pgvector
docker compose up -d

# 2. Backend
cd backend
copy ..\.env.example .env      # rồi điền JWT_SECRET, GUEST_COOKIE_SECRET, mật khẩu seed, GOOGLE_API_KEY
uv sync
uv run alembic upgrade head
uv run python scripts/seed.py
uv run uvicorn app.main:app --reload   # http://localhost:8000/docs

# 3. Frontend (terminal khác)
cd frontend
npm install
npm run dev                            # http://localhost:3000
```

## Test

```powershell
cd backend
uv run pytest
```

Test chạy trên database `mediflow_test` trong Postgres của Docker (tự tạo nếu chưa có), nên cần `docker compose up -d` trước.
