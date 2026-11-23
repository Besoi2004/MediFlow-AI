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
uv run python -m scripts.seed
uv run uvicorn app.main:app --reload   # http://localhost:8000/docs

# 3. Frontend (terminal khác)
cd frontend
copy .env.example .env.local   # BACKEND_URL trỏ tới backend ở bước 2
npm install
npm run dev                            # http://localhost:3000
```

## Test

```powershell
cd backend
uv run pytest
```

Test chạy trên database `mediflow_test` trong Postgres của Docker (tự tạo nếu chưa có), nên cần `docker compose up -d` trước.

## Chạy trên máy khác

File `backend/.env` không nằm trong git, nên trên máy mới phải tạo lại.

1. Cài Git, Docker Desktop, Node 22, uv (`winget install --id=astral-sh.uv -e` trên Windows, hoặc xem trang của uv).
2. `git clone https://github.com/Besoi2004/MediFlow-AI.git` rồi `cd MediFlow-AI`.
3. Tạo `backend/.env` từ `.env.example`, rồi điền:
   - `JWT_SECRET` và `GUEST_COOKIE_SECRET`: mỗi cái một chuỗi ngẫu nhiên dài ít nhất 32 ký tự. Tạo bằng `cd backend; uv run python -c "import secrets; print(secrets.token_urlsafe(48))"`.
   - `SEED_CONSULTANT_PASSWORD`, `SEED_CUSTOMER_PASSWORD`: mật khẩu tài khoản mẫu, tự đặt.
   - `GOOGLE_API_KEY`: key Gemini lấy từ Google AI Studio.
4. `docker compose up -d`, rồi làm tiếp các bước ở mục "Chạy local" (uv sync, alembic, seed).
5. `cd backend; uv run pytest`: phải ra toàn bộ PASS trước khi làm tiếp.
6. Xem `CLAUDE.md` để biết kế hoạch nào làm tiếp theo.
