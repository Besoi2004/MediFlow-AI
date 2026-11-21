# Kế hoạch 6: Deploy lên cloud (Neon + Render + Vercel)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** App chạy trên internet:
- frontend Next.js trên Vercel;
- backend FastAPI (Docker) trên Render;
- Postgres + pgvector trên Neon.

Có script kiểm tra nhanh chạy được với cả local lẫn production.

**Architecture:**
- Trình duyệt chỉ nói chuyện với domain Vercel. Next rewrites chuyển `/api/*` sang Render, nên cookie đăng nhập là cookie của domain Vercel.
- Container backend chạy `alembic upgrade head` rồi `uvicorn` mỗi lần khởi động. Migration chạy lại không sao.
- Seed dữ liệu và embedding RAG chạy **từ máy local** với `DATABASE_URL` trỏ sang Neon, vì gói miễn phí của Render không có shell.

**Tech Stack:** Docker (`python:3.13-slim` + uv), Render Web Service (Docker, Free), Neon Postgres (Free, extension `vector`), Vercel (Hobby). Không thêm thư viện.

**Spec:** `docs/superpowers/specs/2026-11-21-mediflow-ai-design.md` (mục 5, 12, 13 giai đoạn 6, 15, 17 quyết định 10)

**Điều kiện:** Kế hoạch 1–5 đã xong, `main` đã push lên GitHub.

## Global Constraints

- **Việc chỉ người dùng được làm:**
  - tạo tài khoản Neon / Render / Vercel, và kết nối các dịch vụ này với GitHub;
  - dán secret và API key vào trang cấu hình của từng dịch vụ.

  Claude **không** tạo tài khoản, **không** nhập mật khẩu hay key thay người dùng. Claude chỉ hướng dẫn và kiểm tra kết quả.
- **Secret production phải khác secret dev:** `JWT_SECRET` và `GUEST_COOKIE_SECRET` mới, ngẫu nhiên, dài ít nhất 48 ký tự. Mật khẩu tài khoản seed cũng mới.
- **Database URL:** dùng chuỗi kết nối **direct** (không qua pooler) của Neon, thêm `?sslmode=require`, đổi tiền tố thành `postgresql+psycopg://`.
- **Cookie:** production đặt `COOKIE_SECURE=true`.
- **Kiểm tra giới hạn miễn phí lúc deploy:** xem lại giới hạn hiện tại của Neon / Render / Vercel (RAM, thời gian ngủ, số kết nối) rồi ghi vào README. Các con số trong spec chưa được xác minh.
- **Commit:** message một dòng tiếng Việt, không có Co-Authored-By.

## Review Focus

1. **Render ngủ, lần gọi đầu mất 30–60 giây:** sau 5 giây frontend hiện "Máy chủ đang khởi động, có thể mất tới 1 phút…" thay vì để trống. → kiểm tra tay ở Task 4.
2. **Cookie qua Vercel rewrite với `COOKIE_SECURE=true`:** đăng nhập xong tải lại trang vẫn còn đăng nhập, cookie thuộc domain Vercel. → kiểm tra bằng `scripts/smoke.py` và tay ở Task 4.
3. **URL Neon có `?sslmode=require`:** cả SQLAlchemy lẫn checkpointer (`psycopg_url`) đều kết nối được. → kiểm tra ở Task 2 và Task 5.
4. **Render khởi động lại:** `alembic upgrade head` chạy lại không lỗi, `PostgresSaver.setup()` chạy lại không lỗi. → kiểm tra ở Task 1 (chạy container 2 lần).
5. **Thiếu biến môi trường hoặc secret còn là giá trị mẫu:** container dừng ngay với log rõ ràng (validator đã có từ Kế hoạch 1), không chạy với cấu hình yếu. → kiểm tra ở Task 1.

---

## Cấu trúc file

```
backend/Dockerfile
backend/.dockerignore
backend/scripts/smoke.py
frontend/components/PageState.tsx   # PageSkeleton hiện gợi ý "máy chủ đang khởi động" sau 5 giây
README.md                           # + mục "Deploy"
```

---

### Task 1: Docker image của backend

**Files:**
- Create: `backend/Dockerfile`, `backend/.dockerignore`

**Interfaces:**
- Produces:
  - **Image:**
    - `FROM python:3.13-slim`; uv lấy bằng `COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /bin/uv` (ghim đúng bản đang dùng);
    - `WORKDIR /app`; copy `pyproject.toml` + `uv.lock` trước rồi `uv sync --frozen --no-dev --no-install-project` (để cache layer); sau đó copy mã nguồn;
    - `ENV PATH=/app/.venv/bin:$PATH PYTHONUNBUFFERED=1`;
    - `CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]`.
  - **`.dockerignore`:** `.venv`, `.env`, `tests`, `__pycache__`, `.pytest_cache`, `.ruff_cache`, `*.pyc`.

- [ ] **Step 1: Viết Dockerfile và .dockerignore**

- [ ] **Step 2: Build và chạy trên máy, nối vào Postgres của docker compose**

```powershell
docker build -t mediflow-backend backend
docker run --rm -d --name mf-api --network mediflow-ai_default -p 127.0.0.1:8001:8000 --env-file backend/.env `
  -e DATABASE_URL=postgresql+psycopg://mediflow:mediflow@db:5432/mediflow mediflow-backend
docker logs mf-api
curl.exe http://127.0.0.1:8001/api/health
docker restart mf-api; docker logs --tail 5 mf-api; curl.exe http://127.0.0.1:8001/api/health
```
Tên network kiểm tra bằng `docker network ls`.

Expected:
- log có `Running upgrade` (hoặc báo không có gì để chạy) và `Uvicorn running`;
- health trả `{"status":"ok"}` cả trước lẫn sau `docker restart` (Review Focus 4);
- image không chứa `.env`: `docker run --rm mediflow-backend ls -a` không có `.env`.

- [ ] **Step 3: Kiểm tra validator khi secret yếu**

```powershell
docker run --rm --network mediflow-ai_default --env-file backend/.env -e JWT_SECRET=doi-gia-tri-nay mediflow-backend
```
Expected: container thoát ngay, log có `Secret phải dài ít nhất 32 ký tự` (Review Focus 5). Dừng `mf-api` sau khi kiểm tra.

- [ ] **Step 4: Commit**

```powershell
git add backend/Dockerfile backend/.dockerignore
git commit -m "build: dockerfile cho backend"
```

---

### Task 2: Script kiểm tra nhanh (smoke test)

**Files:**
- Create: `backend/scripts/smoke.py`

**Interfaces:**
- Produces: `uv run python -m scripts.smoke --base-url <URL> [--with-chat]`. Dùng `httpx` (dev dependency, đã cài) và một `httpx.Client` giữ cookie. In `[ĐẠT]` / `[SAI] <lý do>` từng bước, có bước sai thì exit code 1. Các bước:
  1. `GET /api/health` (timeout 90 giây để chờ Render thức dậy).
  2. `GET /api/packages`: có ít nhất 15 gói.
  3. Đăng ký tài khoản ngẫu nhiên `smoke-<uuid8>@mediflow.test`, mật khẩu ngẫu nhiên (không in ra).
  4. `GET /api/auth/me` bằng cookie vừa nhận.
  5. Lấy `slots` của `ALP-CB01`, đặt khung đầu tiên, `GET checklist`, rồi hủy lịch.
  6. `--with-chat`: tạo hội thoại, gửi "Gói tổng quát ở Hà Nội cho nam 35 tuổi", kiểm tra có block `packages`. Bước này tốn vài lượt Gemini.
- Script để lại một tài khoản test cho mỗi lần chạy. Ghi `shortcut:` trong code: chưa có API xóa tài khoản.

- [ ] **Step 1: Viết script**

- [ ] **Step 2: Chạy với backend local và với container**

Run: `uv run python -m scripts.smoke --base-url http://127.0.0.1:8000`, rồi chạy lại với `http://127.0.0.1:8001` (container của Task 1).
Expected: toàn bộ `[ĐẠT]`.

- [ ] **Step 3: Commit**

```powershell
git add backend/scripts/smoke.py
git commit -m "test: script kiểm tra nhanh sau deploy"
```

---

### Task 3: Database Neon

**Files:** không có file code; ghi lại các bước vào README ở Task 5.

- [ ] **Step 1 (người dùng làm): tạo project Neon và lấy chuỗi kết nối**

1. Tạo project Neon ở region gần Việt Nam (ví dụ Singapore).
2. Lấy chuỗi kết nối **direct**, đổi tiền tố thành `postgresql+psycopg://` và thêm `?sslmode=require`.
3. Dán vào biến môi trường của phiên PowerShell hiện tại, **không** ghi vào file:
   ```powershell
   $env:DATABASE_URL="..."
   ```

- [ ] **Step 2: Chạy migration và seed từ máy local**

Dùng mật khẩu seed mới cho production; người dùng tự đặt `$env:SEED_CONSULTANT_PASSWORD` và `$env:SEED_CUSTOMER_PASSWORD` trong phiên đó.
```powershell
cd backend
uv run alembic upgrade head
uv run python -m scripts.seed
uv run python -c "from app.db import SessionLocal; from sqlalchemy import text; s=SessionLocal(); print(s.execute(text('select (select count(*) from packages),(select count(*) from prep_chunks),(select count(*) from pg_extension where extname=''vector'')')).one())"
```
Expected: `(15, N>=5, 1)` (Review Focus 3).

Sau đó đóng phiên PowerShell, hoặc xóa biến bằng `Remove-Item Env:DATABASE_URL`, để lần chạy test sau không trỏ nhầm sang Neon.

---

### Task 4: Backend trên Render và frontend trên Vercel

**Files:**
- Modify: `frontend/components/PageState.tsx`

**Interfaces:**
- Produces:
  - `PageSkeleton` có prop `slowHintAfterMs = 5000`. Sau thời gian đó hiện dòng "Máy chủ đang khởi động, có thể mất tới 1 phút…".
  - Panel trợ lý: khi đang chờ trả lời quá 5 giây, hiện cùng dòng đó.

- [ ] **Step 1: Thêm gợi ý chờ, kiểm tra và commit**

Thêm gợi ý vào `PageSkeleton` và vào panel trợ lý. Run: `cd frontend; npm test; npm run lint; npm run build`, phải sạch.
```powershell
git add frontend
git commit -m "feat: gợi ý chờ khi máy chủ đang khởi động"
git push
```

- [ ] **Step 2 (người dùng làm): tạo Web Service trên Render**

1. Tạo Web Service từ repo GitHub với các thiết lập: Root Directory `backend`, Runtime Docker, Plan Free, Region Singapore, Health Check Path `/api/health`.
2. Đặt biến môi trường:
   - `DATABASE_URL` (Neon);
   - `JWT_SECRET`, `GUEST_COOKIE_SECRET` (mới);
   - `COOKIE_SECURE=true`;
   - `LLM_PROVIDER`, `LLM_MODEL`, `GOOGLE_API_KEY`, `EMBEDDING_MODEL`, `EMBEDDING_DIM`;
   - `CHAT_DAILY_LIMIT_PER_USER`, `CHAT_DAILY_LIMIT_PER_GUEST`, `CHAT_DAILY_LIMIT_ALL_GUESTS`.

   Tạo secret bằng: `uv run python -c "import secrets; print(secrets.token_urlsafe(48))"`.

- [ ] **Step 3: Kiểm tra backend trên Render**

Run: `uv run python -m scripts.smoke --base-url https://<tên-dịch-vụ>.onrender.com`
Expected: toàn bộ `[ĐẠT]`. Bước đầu có thể chậm tới 60 giây.

- [ ] **Step 4 (người dùng làm): tạo project Vercel**

1. Import repo, Root Directory `frontend`, Framework Next.js.
2. Biến môi trường `BACKEND_URL=https://<tên-dịch-vụ>.onrender.com`.
3. Deploy.

- [ ] **Step 5: Kiểm tra toàn bộ qua domain Vercel**

Run: `uv run python -m scripts.smoke --base-url https://<project>.vercel.app --with-chat`
Expected: toàn bộ `[ĐẠT]`. Cookie đi qua rewrite (Review Focus 2).

Kiểm tra tay trên trình duyệt:
1. Mở trang lần đầu: trợ lý tự mở.
2. Đăng ký, tải lại trang: vẫn còn đăng nhập.
3. Đặt lịch qua form và qua trợ lý.
4. Tư vấn viên (tài khoản seed production) thấy lịch và cảnh báo.
5. Để Render ngủ (khoảng 15 phút không dùng), mở lại trang: thấy gợi ý "Máy chủ đang khởi động…" (Review Focus 1).

---

### Task 5: Ghi lại cách deploy

**Files:**
- Modify: `README.md`, `CLAUDE.md`, `docs/superpowers/specs/2026-11-21-mediflow-ai-design.md` (mục 15: ghi giới hạn miễn phí đã kiểm tra)

- [ ] **Step 1: Viết mục "Deploy" trong README**

Mục này gồm:
- 3 dịch vụ và vai trò của từng dịch vụ;
- danh sách biến môi trường của Render và Vercel (chỉ ghi tên, không ghi giá trị);
- cách chạy migration và seed sang Neon từ máy local (Task 3);
- cách chạy `scripts.smoke`;
- giới hạn miễn phí đã kiểm tra lúc deploy.

- [ ] **Step 2: Cập nhật trạng thái và commit**

Sửa bảng trong `CLAUDE.md`: Kế hoạch 6 → "xong". Thêm URL production vào `CLAUDE.md`.
```powershell
git add README.md CLAUDE.md docs
git commit -m "docs: hướng dẫn deploy và trạng thái dự án"
git push
```
