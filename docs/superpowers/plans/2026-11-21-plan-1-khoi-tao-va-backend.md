# Kế hoạch 1: Khởi tạo dự án + nền backend

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tạo toàn bộ cấu trúc thư mục của MediFlow-AI và một backend FastAPI chạy được, có test. Backend gồm: danh mục bệnh viện/gói, so sánh gói, khung giờ, đặt/hủy lịch, đăng nhập 2 vai trò, trang tư vấn viên xem lịch hẹn. Thêm một script thử Gemini.

**Architecture:** Monorepo `backend/` (FastAPI đồng bộ + SQLAlchemy 2.0 + Alembic, Postgres/pgvector chạy bằng Docker) và `frontend/` (Next.js, ở kế hoạch này mới chỉ có khung). Logic nghiệp vụ nằm trong `app/services/` để kế hoạch agent sau này dùng lại. Test chạy trên Postgres thật, không mock DB.

**Tech Stack:** Python 3.13 + uv, FastAPI, SQLAlchemy 2.0, psycopg 3, Alembic, PyJWT, pwdlib[argon2], pydantic-settings, pytest; Node 22 + npm, Next.js (create-next-app), shadcn/ui; Docker `pgvector/pgvector:pg17`.

**Spec:** `docs/superpowers/specs/2026-11-21-mediflow-ai-design.md`

**Các kế hoạch tiếp theo (viết sau):**
- Kế hoạch 2: lõi an toàn.
- Kế hoạch 3: giao diện đặt khám.
- Kế hoạch 4: agent.
- Kế hoạch 5: trợ lý trên giao diện.
- Kế hoạch 6: deploy.

## Global Constraints

- Python 3.13 quản lý bằng `uv`; Node 22 + npm. Thư viện dùng bản ổn định mới nhất lúc cài, khóa trong `uv.lock` / `package-lock.json`.
- Toàn bộ chữ hiển thị cho người dùng (thông báo lỗi API, nội dung seed) bằng tiếng Việt.
- Chỉ dùng dữ liệu mô phỏng. Tên bệnh viện hư cấu, luôn có hậu tố "(mô phỏng)".
- Tiền là số nguyên VND (`int`).
- Thời gian lưu `timestamptz` (UTC). Ngày giờ do người dùng nhập (ví dụ `date_from=2026-11-22`) hiểu theo múi giờ `Asia/Ho_Chi_Minh`.
- Mã bệnh viện viết hoa 3 chữ (`ALP`, `BET`, `GAM`). Mã gói có dạng `{MÃ_BV}-{LOẠI}` (`ALP-CB01`).
- Xem bệnh viện/gói/khung giờ: công khai. Đặt/xem/hủy lịch của mình: role `customer`. Route `/api/consultant/*`: role `consultant`.
- Không ghi PII (tên, email, SĐT) vào log.
- Mọi lệnh backend chạy trong thư mục `backend/` qua `uv run ...`.
- Commit trên nhánh `feat/plan-1-backend`, không commit thẳng vào `main`.

## Review Focus

1. **Tên tỉnh/thành gõ không dấu hoặc khác hoa thường** ("ha noi", "HÀ NỘI") vẫn phải lọc đúng bệnh viện Hà Nội. Agent sau này sẽ truyền chữ tự do. → test ở Task 4.
2. **`date_from` hiểu theo giờ Việt Nam, không phải UTC.** Khung 06:30 sáng ngày D (giờ VN) là 23:30 UTC ngày D-1, nhưng vẫn phải thuộc ngày D. → test ở Task 6.
3. **Bấm "Xác nhận" hai lần** không được tạo hai lịch hẹn trùng (cùng người, cùng gói, cùng khung giờ). → test ở Task 6.
4. **Hủy lịch đã qua giờ khám** phải bị từ chối, không được giảm `booked_count` của khung đã qua. → test ở Task 6.
5. **Email khác hoa thường** ("An@Mail.test" và "an@mail.test") là cùng một tài khoản, cả khi đăng ký lẫn đăng nhập. → test ở Task 5.

---

## Cấu trúc file của kế hoạch này

```
MediFlow-AI/
├── .gitignore · .env.example · docker-compose.yml · README.md
├── backend/
│   ├── pyproject.toml · uv.lock · alembic.ini · alembic/env.py · alembic/versions/
│   ├── app/
│   │   ├── main.py            # tạo app, gắn router (Task 2–6)
│   │   ├── config.py          # Settings (Task 3)
│   │   ├── db.py              # engine, SessionLocal, get_db (Task 3)
│   │   ├── models.py          # 7 bảng nghiệp vụ (Task 3)
│   │   ├── schemas.py         # Pydantic in/out (Task 4–6)
│   │   ├── textnorm.py        # slug_vi() bỏ dấu, VN_TZ (Task 3; Kế hoạch 2 dùng lại cho cờ đỏ)
│   │   ├── auth.py            # băm mật khẩu, JWT, current_user, require_role (Task 5)
│   │   ├── api/{hospitals,packages,auth,bookings,consultant}.py
│   │   ├── api/chat.py        # chỉ docstring, Kế hoạch 4
│   │   ├── services/{catalog,booking,prep}.py
│   │   ├── safety/{red_flags.py,red_flags.yaml,pii.py,output_guard.py}   # chỉ docstring/rỗng, Kế hoạch 2
│   │   └── agent/{llm,state,prompts,tools,graph}.py                    # chỉ docstring, Kế hoạch 4
│   ├── data/{hospitals,service_items,packages}.yaml · data/prep_docs/.gitkeep
│   ├── scripts/{seed.py,spike_llm.py,run_eval.py}
│   └── tests/{conftest.py,test_catalog.py,test_auth.py,test_booking.py,eval/.gitkeep}
└── frontend/                  # create-next-app + shadcn + các trang khung
```

---

### Task 1: Khung dự án (thư mục, Docker, uv, Next.js)

**Files:**
- Create: `.gitignore`, `.env.example`, `docker-compose.yml`, `README.md`
- Create: `backend/` qua `uv init`, các file stub (một dòng docstring nói file làm gì) theo cây ở mục 11 của spec
- Create: `frontend/` qua `create-next-app`, các `page.tsx` khung theo mục 11 của spec

**Interfaces:**
- Produces: Postgres dev ở `localhost:5432` (user/pass/db `mediflow`); lệnh `uv run ...` chạy được trong `backend/`; `npm run build` chạy được trong `frontend/`.

- [ ] **Step 1: Tạo nhánh và cài uv**

```powershell
git checkout -b feat/plan-1-backend
winget install --id=astral-sh.uv -e
uv --version
```
Expected: in ra phiên bản uv (mở terminal mới nếu PATH chưa cập nhật).

- [ ] **Step 2: Viết các file gốc**

- `docker-compose.yml`: service `db`, image `pgvector/pgvector:pg17`, env `POSTGRES_USER/POSTGRES_PASSWORD/POSTGRES_DB=mediflow`, cổng `5432:5432`, volume `pgdata`, healthcheck `pg_isready -U mediflow`.
- `.gitignore`: `.env`, `.venv/`, `__pycache__/`, `.pytest_cache/`, `node_modules/`, `.next/`, `*.pyc`.
- `.env.example`:
  - các biến ở mục 12 của spec;
  - thêm `TEST_DATABASE_URL=postgresql+psycopg://mediflow:mediflow@localhost:5432/mediflow_test`;
  - thêm `COOKIE_SECURE=false`, `JWT_EXPIRE_MINUTES=10080`;
  - thêm tài khoản mẫu cho seed: `SEED_CONSULTANT_EMAIL=tuvanvien@mediflow.test`, `SEED_CONSULTANT_PASSWORD=`, `SEED_CUSTOMER_EMAIL=khachhang@mediflow.test`, `SEED_CUSTOMER_PASSWORD=`. Mật khẩu để trống, người dùng tự điền trong `.env`.
- `README.md`: các bước chạy local (docker compose, uv sync, alembic, seed, uvicorn, npm run dev) và lệnh chạy test.

- [ ] **Step 3: Khởi tạo backend**

```powershell
cd backend
uv init --app --python 3.13 --no-readme
uv add fastapi "uvicorn[standard]" pydantic-settings sqlalchemy "psycopg[binary]" alembic pgvector pyjwt "pwdlib[argon2]" pyyaml langgraph langgraph-checkpoint-postgres langchain langchain-google-genai
uv add --dev pytest httpx ruff
```
- Xóa file `main.py` mẫu do `uv init` sinh ra.
- Thêm vào `pyproject.toml`:
  ```toml
  [tool.pytest.ini_options]
  pythonpath = ["."]
  testpaths = ["tests"]
  ```
- Tạo các file stub của `app/`, `data/`, `scripts/`, `tests/` theo cây ở trên. Mỗi file `.py` chỉ có một dòng docstring. `red_flags.yaml` rỗng. Thư mục trống thì đặt `.gitkeep`.

- [ ] **Step 4: Khởi tạo frontend**

```powershell
cd ..
npx create-next-app@latest frontend --ts --tailwind --eslint --app --no-src-dir --import-alias "@/*" --use-npm --yes
cd frontend
npx shadcn@latest init -d
npx shadcn@latest add button input card table tabs badge select dialog sheet calendar
```
- Tạo các `page.tsx` khung theo mục 11 của spec: `login`, `register`, `hospitals`, `hospitals/[code]`, `packages`, `packages/[code]`, `compare`, `book/[code]`, `bookings`, `consultant`, `consultant/conversations/[id]`. Mỗi trang chỉ render `<main><h1>` tên trang bằng tiếng Việt `</h1></main>`.
- Tạo thư mục `components/{catalog,booking,assistant}/` (có `.gitkeep`) và `lib/api.ts` (chỉ một comment).
- `next.config.ts`: thêm `rewrites()` để `/api/:path*` chuyển sang `${process.env.BACKEND_URL ?? "http://localhost:8000"}/api/:path*`.

- [ ] **Step 5: Kiểm tra**

```powershell
cd ..
docker compose up -d
docker compose ps
cd backend; uv run python -c "import fastapi, sqlalchemy, langgraph, langchain_google_genai; print('ok')"
cd ..\frontend; npm run build
```
Expected:
- `db` ở trạng thái `healthy`.
- Lệnh Python in `ok`.
- `npm run build` thành công, liệt kê đủ các route khung.

- [ ] **Step 6: Commit**

```powershell
cd ..
git add .
git commit -m "chore: khởi tạo cấu trúc dự án MediFlow-AI (backend uv, frontend Next.js, docker postgres)"
```
Commit này kèm luôn spec và kế hoạch trong `docs/`.

---

### Task 2: Config, DB, models, migration đầu tiên, hạ tầng test

**Files:**
- Modify: `backend/app/config.py`, `backend/app/db.py`, `backend/app/models.py`, `backend/app/main.py`
- Create: `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/versions/<rev>_initial_schema.py`
- Create: `backend/.env` (copy từ `.env.example`, điền `JWT_SECRET`, `GUEST_COOKIE_SECRET`, mật khẩu seed; không commit)
- Test: `backend/tests/conftest.py`, `backend/tests/test_schema.py`

**Interfaces:**
- Produces:
  - `app.config.Settings` (pydantic-settings, đọc `backend/.env`). Field theo đúng tên biến môi trường ở `.env.example`, dạng chữ thường: `database_url: str`, `test_database_url: str | None`, `jwt_secret: str`, `jwt_expire_minutes: int = 10080`, `cookie_secure: bool = False`, `guest_cookie_secret: str`, `llm_provider`, `llm_model`, `google_api_key: str | None`, `embedding_model: str | None`, `embedding_dim: int = 768`, ba biến `chat_daily_limit_*`, bốn biến `seed_*`.
  - `app.config.get_settings() -> Settings` (có `lru_cache`).
  - `app.db`: `engine`, `SessionLocal`, `get_db() -> Iterator[Session]` (dependency FastAPI).
  - `app.models`: `Base(DeclarativeBase)` và các model:
    - `User(id, email, password_hash, role, full_name, birth_date, gender, phone, created_at)`
    - `Hospital(id, code, name, city, city_slug, address, phone, description, active)`
    - `Package(id, code, hospital_id→Hospital, name, description, price_vnd, gender_scope, age_min, age_max: int|None, tags: list[str] (ARRAY), active)`, quan hệ `hospital`, `items`
    - `ServiceItem(id, code, name, category, prep_instruction, fasting_hours: int)`
    - `PackageItem(package_id, item_id)` (bảng nối, khóa chính kép)
    - `TimeSlot(id, hospital_id, start_at: timestamptz, capacity, booked_count)`, unique `(hospital_id, start_at)`
    - `Booking(id, user_id, package_id, slot_id, status, price_snapshot_vnd, channel, created_at)`, quan hệ `user`, `package`, `slot`
  - Các trường liệt kê giá trị dùng `sa.Enum(..., native_enum=False)` (VARCHAR + CHECK): `role` ∈ {customer, consultant}, `gender` ∈ {male, female}, `gender_scope` ∈ {any, male, female}, `status` ∈ {booked, cancelled}, `channel` ∈ {web, assistant}.
  - `app.main.app` (FastAPI). Router dưới `/api`. Có `GET /api/health → {"status": "ok"}`.
  - Fixture trong `tests/conftest.py`:
    - `engine` (session scope): tạo database `mediflow_test` nếu chưa có, chạy `alembic upgrade head` lên đó.
    - `db` (function scope): `Session` tới DB test. Sau mỗi test chạy `TRUNCATE ... RESTART IDENTITY CASCADE` mọi bảng.
    - `client`: `TestClient(app)`, override `get_db` bằng session test.

- [ ] **Step 1: Viết test thất bại `tests/test_schema.py`**

```python
def test_migration_creates_business_tables(db):
    names = set(sa.inspect(db.get_bind()).get_table_names())
    assert {"users", "hospitals", "packages", "service_items",
            "package_items", "time_slots", "bookings"} <= names

def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}
```

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `uv run pytest tests/test_schema.py -v`
Expected: FAIL (chưa có models / conftest / app).

- [ ] **Step 3: Cài đặt config, db, models, main, alembic, conftest**

- `uv run alembic init alembic`.
- `env.py`: lấy URL từ `get_settings().database_url`, hoặc từ `config.attributes["url"]` nếu được truyền vào (conftest truyền URL test theo cách này). `target_metadata = Base.metadata`.
- Sinh migration bằng `uv run alembic revision --autogenerate -m "initial schema"` rồi đọc lại file sinh ra. Kiểm tra có ARRAY và các CHECK constraint.

- [ ] **Step 4: Chạy test**

Run: `uv run alembic upgrade head; uv run pytest tests/test_schema.py -v`
Expected: migration chạy được trên DB dev; 2 test PASS.

- [ ] **Step 5: Commit**

```powershell
git add backend
git commit -m "feat(backend): config, models, migration đầu tiên, hạ tầng test với Postgres thật"
```

---

### Task 3: Dữ liệu mô phỏng + seed

**Files:**
- Modify: `backend/data/hospitals.yaml`, `backend/data/service_items.yaml`, `backend/data/packages.yaml`, `backend/scripts/seed.py`
- Create: `backend/app/textnorm.py`
- Test: `backend/tests/test_seed.py`

**Interfaces:**
- Consumes: models và fixture `db` từ Task 2.
- Produces:
  - `app.textnorm.slug_vi(text: str) -> str`: chữ thường, bỏ dấu (NFD + bỏ dấu kết hợp), `đ→d`, chuỗi ký tự không phải chữ/số → `-`, cắt `-` hai đầu. Ví dụ `"Hà Nội" → "ha-noi"`, `"TP. Hồ Chí Minh" → "tp-ho-chi-minh"`.
  - Các hàm trong `scripts.seed`, đều chạy lại nhiều lần được (upsert theo `code` / `email`), commit trong hàm:
    - `seed_catalog(db: Session, data_dir: Path) -> None`: bệnh viện, hạng mục, gói, `city_slug = slug_vi(city)`.
    - `seed_slots(db: Session, start: date, days: int = 14) -> None`: với mỗi bệnh viện, mỗi ngày Thứ 2–Thứ 7 trong `[start, start+days)`, tạo các khung 07:00, 08:00, 09:00, 10:00 giờ `Asia/Ho_Chi_Minh`, `capacity=5`. Bỏ qua khung đã tồn tại.
    - `seed_users(db: Session, settings: Settings) -> None`: 1 tư vấn viên và 1 khách hàng mẫu, lấy email/mật khẩu từ biến `SEED_*`. Bỏ qua nếu mật khẩu trống. Cần `auth.hash_password` từ Task 5, nên **phần này viết ở Task 5**.
  - `python scripts/seed.py`: CLI gọi lần lượt `seed_catalog`, `seed_slots(today local)`, `seed_users`.
- Nội dung YAML lấy từ mục 6 của spec:
  - **3 bệnh viện** ALP / BET / GAM.
  - **15 gói** theo bảng (mỗi bệnh viện 5 gói), với đúng giá, đối tượng và tag trong spec.
  - **Hạng mục:** tối thiểu `KHAM-NOI`, `XN-MAU` (0h), `XN-DUONG` (8h, "Nhịn ăn ít nhất 8 tiếng, được uống nước lọc"), `XN-MO` (8h), `XN-NUOCTIEU`, `XQ-NGUC` ("Không đeo trang sức, đồ kim loại; phụ nữ có thai báo trước cho nhân viên"), `SA-BUNG` (6h, "Nhịn tiểu trước khi siêu âm"), `DIEN-TIM`, `SA-TIM`, `SA-VU`, `PAP`.
  - **Gói `*-CB01`** phải có `XN-DUONG` và `SA-BUNG`. **`GAM-CB01`** thiếu ít nhất một hạng mục mà `ALP-CB01` có, để test so sánh có hàng `False`.

- [ ] **Step 1: Viết test thất bại `tests/test_seed.py`**

```python
@pytest.mark.parametrize("raw,slug", [("Hà Nội", "ha-noi"), ("HÀ NỘI", "ha-noi"),
    ("ha noi", "ha-noi"), ("TP. Hồ Chí Minh", "tp-ho-chi-minh"), ("Đà Nẵng", "da-nang")])
def test_slug_vi(raw, slug):
    assert slug_vi(raw) == slug

def test_seed_catalog_is_idempotent(db):
    seed_catalog(db, DATA_DIR); seed_catalog(db, DATA_DIR)
    assert db.scalar(select(func.count(Hospital.id))) == 3
    assert db.scalar(select(func.count(Package.id))) == 15
    pkg = db.scalar(select(Package).where(Package.code == "GAM-TIM"))
    assert pkg.price_vnd == 4_600_000 and pkg.hospital.code == "GAM" and pkg.age_min == 40

def test_seed_slots_local_time_and_weekdays(db):
    seed_catalog(db, DATA_DIR)
    monday = date(2026, 11, 23)  # Thứ 2
    seed_slots(db, monday, days=7); seed_slots(db, monday, days=7)
    slots = db.scalars(select(TimeSlot)).all()
    assert len(slots) == 3 * 6 * 4          # 3 BV × T2–T7 × 4 khung
    local = [s.start_at.astimezone(VN_TZ) for s in slots]
    assert {t.hour for t in local} == {7, 8, 9, 10}
    assert all(t.weekday() < 6 for t in local)
```

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `uv run pytest tests/test_seed.py -v`
Expected: FAIL (`slug_vi`, `seed_catalog` chưa có).

- [ ] **Step 3: Viết `textnorm.py`, YAML, `seed_catalog`, `seed_slots`, CLI**

`VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")` đặt trong `app/textnorm.py`, mọi task import từ đó. Trên Windows, `zoneinfo` cần gói `tzdata`: chạy `uv add tzdata`.

- [ ] **Step 4: Chạy test và seed DB dev**

Run: `uv run pytest tests/test_seed.py -v; uv run python scripts/seed.py`
Expected: test PASS; script seed chạy xong không lỗi trên DB dev.

- [ ] **Step 5: Commit**

```powershell
git add backend
git commit -m "feat(backend): dữ liệu mô phỏng 3 bệnh viện, 16 gói, khung giờ và script seed"
```

---

### Task 4: Danh mục — service + API bệnh viện/gói/so sánh

**Files:**
- Modify: `backend/app/services/catalog.py`, `backend/app/api/hospitals.py`, `backend/app/api/packages.py`, `backend/app/schemas.py`, `backend/app/main.py`
- Test: `backend/tests/test_catalog.py`

**Interfaces:**
- Consumes: `seed_catalog`, `slug_vi`, models.
- Produces (`app.services.catalog`):
  - `list_hospitals(db, city: str | None = None) -> list[Hospital]`. Lọc theo `city_slug == slug_vi(city)`, chỉ `active`, sắp theo tên.
  - `get_hospital(db, code: str) -> Hospital | None`.
  - `search_packages(db, *, hospital_code: str | None = None, city: str | None = None, tag: str | None = None, gender: Literal["male","female"] | None = None, age: int | None = None, price_max: int | None = None) -> list[Package]`. Quy tắc:
    - chỉ gói và bệnh viện `active`;
    - `gender` → `gender_scope IN ('any', gender)`;
    - `age` → `age_min <= age AND (age_max IS NULL OR age_max >= age)`;
    - `tag` → `tag = ANY(tags)`;
    - `price_max` → `price_vnd <= price_max`;
    - sắp theo `price_vnd` tăng dần, rồi theo `code`.
  - `get_package(db, code: str) -> Package | None`: chỉ gói active, nạp sẵn `hospital` và `items`.
  - `compare_packages(db, codes: list[str]) -> CompareOut`. Ném `CatalogError("compare_count")` nếu số mã không nằm trong 2–3, hoặc `CatalogError("package_not_found", code)`.
  - `class CatalogError(Exception)`, có thuộc tính `.code: str`.
- Produces (`app.schemas`):
  - `HospitalOut(code, name, city, address, phone, description)`
  - `HospitalDetailOut(HospitalOut + packages: list[PackageSummary])`
  - `PackageSummary(code, name, hospital_code, hospital_name, city, price_vnd, gender_scope, age_min, age_max, tags)`
  - `ItemOut(code, name, category, prep_instruction, fasting_hours)`
  - `PackageDetailOut(PackageSummary + description, items: list[ItemOut])`
  - `CompareRow(item_code, item_name, category, included: list[bool])`
  - `CompareOut(packages: list[PackageSummary], rows: list[CompareRow])`. `rows` là hợp các hạng mục của mọi gói, sắp theo `(category, item_name)`. `included[i]` ứng với `packages[i]`, giữ đúng thứ tự `codes` người dùng gửi.
- Produces (API, đều công khai):
  - `GET /api/hospitals?city=` → `list[HospitalOut]`
  - `GET /api/hospitals/{code}` → `HospitalDetailOut` / 404
  - `GET /api/packages?hospital=&city=&tag=&gender=&age=&price_max=` → `list[PackageSummary]` (`age`, `price_max` có `ge=0`)
  - `GET /api/packages/compare?codes=A,B[,C]` → `CompareOut`; 400 `{"detail": "Chỉ so sánh được 2–3 gói"}`; 404 nếu có mã không tồn tại. **Khai báo trước** route `/{code}`.
  - `GET /api/packages/{code}` → `PackageDetailOut` / 404 `{"detail": "Không tìm thấy gói khám"}`

- [ ] **Step 1: Viết test thất bại `tests/test_catalog.py`**

Fixture `catalog` gọi `seed_catalog(db, DATA_DIR)`.
```python
def test_filter_male_35(client, catalog):
    codes = {p["code"] for p in client.get("/api/packages", params={"gender": "male", "age": 35}).json()}
    assert {"ALP-TQNAM", "BET-TQNAM", "ALP-CB01"} <= codes
    assert not codes & {"ALP-TQNU", "BET-UTNU", "ALP-CAOTUOI", "ALP-TIM"}

@pytest.mark.parametrize("city", ["Hà Nội", "ha noi", "HÀ NỘI"])
def test_city_filter_ignores_accents_and_case(client, catalog, city):          # Review Focus 1
    res = client.get("/api/packages", params={"city": city}).json()
    assert res and all(p["code"].startswith("ALP-") for p in res)

def test_tag_and_price(client, catalog):
    res = client.get("/api/packages", params={"tag": "tim-mach", "price_max": 5_000_000}).json()
    assert [p["code"] for p in res] == ["GAM-TIM"]

def test_sorted_by_price(client, catalog):
    prices = [p["price_vnd"] for p in client.get("/api/packages").json()]
    assert prices == sorted(prices)

def test_inactive_package_hidden(client, catalog, db):
    db.execute(update(Package).where(Package.code == "ALP-CB01").values(active=False)); db.commit()
    assert "ALP-CB01" not in {p["code"] for p in client.get("/api/packages").json()}
    assert client.get("/api/packages/ALP-CB01").status_code == 404

def test_compare_union_and_order(client, catalog):
    out = client.get("/api/packages/compare", params={"codes": "GAM-CB01,ALP-CB01"}).json()
    assert [p["code"] for p in out["packages"]] == ["GAM-CB01", "ALP-CB01"]
    assert any(r["included"] == [False, True] for r in out["rows"])
    assert all(len(r["included"]) == 2 for r in out["rows"])

@pytest.mark.parametrize("codes,status", [("ALP-CB01", 400),
    ("ALP-CB01,BET-CB01,GAM-CB01,ALP-TIM", 400), ("ALP-CB01,KHONG-CO", 404)])
def test_compare_errors(client, catalog, codes, status):
    assert client.get("/api/packages/compare", params={"codes": codes}).status_code == status

def test_hospital_detail(client, catalog):
    h = client.get("/api/hospitals/GAM").json()
    assert h["name"].endswith("(mô phỏng)") and all(p["code"].startswith("GAM-") for p in h["packages"])
    assert client.get("/api/hospitals/XYZ").status_code == 404

def test_package_detail_has_items_with_prep(client, catalog):
    d = client.get("/api/packages/ALP-CB01").json()
    assert any(i["code"] == "XN-DUONG" and i["fasting_hours"] == 8 for i in d["items"])

def test_negative_age_rejected(client, catalog):
    assert client.get("/api/packages", params={"age": -1}).status_code == 422
```

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `uv run pytest tests/test_catalog.py -v`
Expected: FAIL (404 vì chưa có route).

- [ ] **Step 3: Viết service, schema, router và gắn router vào `main.py`**

Router bắt `CatalogError` rồi đổi sang `HTTPException`, thông báo lỗi bằng tiếng Việt.

- [ ] **Step 4: Chạy test**

Run: `uv run pytest -v`
Expected: toàn bộ PASS.

- [ ] **Step 5: Commit**

```powershell
git add backend
git commit -m "feat(backend): API danh mục bệnh viện, lọc gói, chi tiết và so sánh gói"
```

---

### Task 5: Đăng nhập 2 vai trò

**Files:**
- Modify: `backend/app/auth.py`, `backend/app/api/auth.py`, `backend/app/schemas.py`, `backend/app/main.py`, `backend/scripts/seed.py` (thêm `seed_users`)
- Test: `backend/tests/test_auth.py`

**Interfaces:**
- Consumes: `User`, `get_db`, `get_settings`.
- Produces (`app.auth`):
  - `hash_password(plain: str) -> str` và `verify_password(plain: str, hashed: str) -> bool`, dùng `pwdlib.PasswordHash.recommended()`.
  - `create_access_token(user_id: int) -> str`: JWT HS256, `sub=str(user_id)`, `exp` = bây giờ + `jwt_expire_minutes`.
  - `COOKIE_NAME = "access_token"`. `set_auth_cookie(response, token)` (httpOnly, `samesite="lax"`, `secure=settings.cookie_secure`, `max_age`) và `clear_auth_cookie(response)`.
  - Dependency `current_user(request, db) -> User`: đọc cookie; thiếu, sai hoặc hết hạn → 401 `"Vui lòng đăng nhập"`.
  - Dependency `optional_user(request, db) -> User | None`.
  - `require_role(role: Literal["customer","consultant"])`: trả về dependency; sai role → 403 `"Không có quyền truy cập"`.
- Produces (`app.schemas`):
  - `RegisterIn(email: EmailStr, password: str (min 8), full_name: str (1–100), birth_date: date, gender: Literal["male","female"], phone: str)`. Email luôn được chuẩn hóa về chữ thường. `EmailStr` cần chạy `uv add "pydantic[email]"`.
  - `LoginIn(email, password)`.
  - `UserOut(id, email, full_name, role, birth_date, gender, phone)`.
- Produces (API):
  - `POST /api/auth/register` → 201 `UserOut` + cookie; email đã có → 409 `"Email đã được đăng ký"`.
  - `POST /api/auth/login` → 200 `UserOut` + cookie; sai → 401 `"Email hoặc mật khẩu không đúng"`.
  - `POST /api/auth/logout` → 204, xóa cookie.
  - `GET /api/auth/me` → `UserOut` / 401.
  - Đăng ký công khai luôn tạo role `customer`. Tài khoản tư vấn viên chỉ tạo bằng `seed_users`.
- Chuyển hội thoại khách vãng lai sang tài khoản khi đăng nhập: **để Kế hoạch 4** (lúc đó mới có bảng `conversations`).

- [ ] **Step 1: Viết test thất bại `tests/test_auth.py`**

```python
NEW = {"email": "An@Mail.test", "password": "matkhau123", "full_name": "Nguyễn An",
       "birth_date": "1991-05-02", "gender": "male", "phone": "0900000001"}

def test_register_sets_httponly_cookie_and_customer_role(client, db):
    r = client.post("/api/auth/register", json=NEW)
    assert r.status_code == 201 and r.json()["role"] == "customer"
    assert "httponly" in r.headers["set-cookie"].lower()
    assert client.get("/api/auth/me").json()["email"] == "an@mail.test"
    u = db.scalar(select(User))
    assert u.password_hash != NEW["password"] and verify_password(NEW["password"], u.password_hash)

def test_email_case_insensitive(client):                                       # Review Focus 5
    client.post("/api/auth/register", json=NEW)
    assert client.post("/api/auth/register", json={**NEW, "email": "an@mail.test"}).status_code == 409
    client.post("/api/auth/logout")
    assert client.post("/api/auth/login", json={"email": "AN@MAIL.TEST", "password": "matkhau123"}).status_code == 200

def test_wrong_password_401(client):
    client.post("/api/auth/register", json=NEW); client.post("/api/auth/logout")
    assert client.post("/api/auth/login", json={"email": NEW["email"], "password": "sai12345"}).status_code == 401

def test_short_password_422(client):
    assert client.post("/api/auth/register", json={**NEW, "password": "123"}).status_code == 422

def test_logout_then_me_401(client):
    client.post("/api/auth/register", json=NEW); client.post("/api/auth/logout")
    assert client.get("/api/auth/me").status_code == 401

def test_tampered_token_401(client):
    client.cookies.set("access_token", "khong.phai.jwt")
    assert client.get("/api/auth/me").status_code == 401

def test_seed_users_creates_consultant(db, settings_with_seed_passwords):
    seed_users(db, settings_with_seed_passwords); seed_users(db, settings_with_seed_passwords)
    roles = sorted(db.scalars(select(User.role)).all())
    assert roles == ["consultant", "customer"]
```
`settings_with_seed_passwords` là một fixture trong `conftest.py`: `Settings` với mật khẩu seed là giá trị test đặt ngay trong fixture.

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `uv run pytest tests/test_auth.py -v`
Expected: FAIL.

- [ ] **Step 3: Viết `auth.py`, router auth, schema, `seed_users`**

- [ ] **Step 4: Chạy test**

Run: `uv run pytest -v`
Expected: toàn bộ PASS.

- [ ] **Step 5: Commit**

```powershell
git add backend
git commit -m "feat(backend): đăng ký/đăng nhập bằng cookie JWT, phân quyền customer/consultant"
```

---

### Task 6: Khung giờ, đặt/hủy lịch, checklist chuẩn bị, trang tư vấn viên

**Files:**
- Modify: `backend/app/services/booking.py`, `backend/app/services/prep.py`, `backend/app/api/packages.py` (route slots), `backend/app/api/bookings.py`, `backend/app/api/consultant.py`, `backend/app/schemas.py`, `backend/app/main.py`
- Test: `backend/tests/test_booking.py`

**Interfaces:**
- Consumes: `catalog.get_package`, `current_user`, `require_role`, `VN_TZ`, các hàm seed.
- Produces (`app.services.booking`):
  - `class BookingError(Exception)` có `.code`, nhận một trong các giá trị: `package_not_found`, `slot_not_found`, `slot_wrong_hospital`, `slot_in_past`, `slot_full`, `duplicate_booking`, `booking_not_found`, `already_cancelled`.
  - `list_available_slots(db, package_code: str, date_from: date, days: int = 14) -> list[TimeSlot]`:
    - Chỉ lấy khung của bệnh viện có gói đó, còn chỗ (`booked_count < capacity`), và `start_at` lớn hơn bây giờ.
    - Khoảng thời gian: `start_at >= date_from 00:00 giờ VN` và `< (date_from + days) 00:00 giờ VN`.
    - Sắp theo `start_at`.
  - `create_booking(db, *, user_id: int, package_code: str, slot_id: int, channel: Literal["web","assistant"] = "web") -> Booking`:
    - Khóa khung bằng `SELECT ... FOR UPDATE`, rồi kiểm tra theo thứ tự: gói tồn tại và active → khung tồn tại → khung đúng bệnh viện → khung chưa qua → không trùng lịch `booked` (cùng user, gói, khung) → còn chỗ.
    - Hợp lệ thì `booked_count += 1`, `price_snapshot_vnd = package.price_vnd`, rồi commit.
  - `cancel_booking(db, *, booking_id: int, actor: User) -> Booking`:
    - Khách hàng chỉ hủy được lịch của mình; lịch của người khác trả `booking_not_found` để không lộ là lịch đó có tồn tại.
    - Tư vấn viên hủy được mọi lịch.
    - Lịch đã hủy → `already_cancelled`. Khung đã qua → `slot_in_past`.
    - Hợp lệ thì `booked_count -= 1`.
  - `list_bookings(db, *, user_id: int | None = None, hospital_code: str | None = None, status: str | None = None, on_date: date | None = None) -> list[Booking]`, sắp theo `slot.start_at`.
- Produces (`app.services.prep`):
  - `prep_checklist(package: Package) -> list[ChecklistItem]`. Thứ tự các dòng:
    1. Nếu `max(fasting_hours) > 0`: `"Nhịn ăn ít nhất {n} tiếng trước giờ khám (được uống nước lọc)"`, kèm tên các hạng mục cần nhịn.
    2. Mỗi `prep_instruction` khác rỗng, gộp các hạng mục có cùng câu hướng dẫn, giữ thứ tự xuất hiện.
    3. Hai dòng cố định ở cuối: `"Mang theo CCCD hoặc giấy tờ tùy thân"` và `"Đến trước giờ hẹn 15 phút để làm thủ tục"`.
- Produces (`app.schemas`):
  - `SlotOut(id, start_at, remaining)`
  - `BookingIn(package_code, slot_id)`
  - `BookingOut(id, status, channel, package_code, package_name, hospital_code, hospital_name, start_at, price_snapshot_vnd, created_at)`
  - `ConsultantBookingOut(BookingOut + customer_name, customer_phone, customer_email)`
  - `ChecklistItem(text: str, items: list[str])`
- Produces (API). Lỗi đổi sang mã HTTP như sau:
  - 404: `*_not_found`
  - 400: `slot_wrong_hospital`, `slot_in_past`
  - 409: `slot_full`, `duplicate_booking`, `already_cancelled`
  - Các route:
    - `GET /api/packages/{code}/slots?date_from=YYYY-MM-DD` (công khai; mặc định là hôm nay theo giờ VN) → `list[SlotOut]`
    - `POST /api/bookings` (customer) → 201 `BookingOut`
    - `GET /api/bookings` (customer, chỉ lịch của mình)
    - `POST /api/bookings/{id}/cancel` (customer)
    - `GET /api/bookings/{id}/checklist` (customer, chỉ lịch của mình) → `list[ChecklistItem]`
    - `GET /api/consultant/bookings?hospital=&status=&date=` (consultant) → `list[ConsultantBookingOut]`
    - `POST /api/consultant/bookings/{id}/cancel` (consultant)

- [ ] **Step 1: Viết test thất bại `tests/test_booking.py`**

Fixtures:
- `catalog`: seed danh mục.
- `slots`: `seed_slots` từ ngày mai theo giờ VN, 7 ngày.
- `customer_client` / `other_client` / `consultant_client`: mỗi fixture có cookie riêng (tạo user bằng `hash_password`, set cookie bằng `create_access_token`).
- `make_slot(hospital_code, local_dt, capacity=5)`: tạo khung tùy ý.

```python
def first_slot(client, code="ALP-CB01"):
    return client.get(f"/api/packages/{code}/slots").json()[0]

def test_slots_only_from_package_hospital(client, catalog, slots, db):
    ids = [s["id"] for s in client.get("/api/packages/GAM-CB01/slots").json()]
    assert ids and {db.get(TimeSlot, i).hospital.code for i in ids} == {"GAM"}

def test_date_from_is_vietnam_local_day(client, catalog, make_slot):           # Review Focus 2
    d = date.today() + timedelta(days=3)
    early = make_slot("ALP", datetime.combine(d, time(6, 30), VN_TZ))       # 23:30 UTC hôm trước
    prev_night = make_slot("ALP", datetime.combine(d - timedelta(days=1), time(23, 30), VN_TZ))
    ids = [s["id"] for s in client.get("/api/packages/ALP-CB01/slots",
           params={"date_from": d.isoformat()}).json()]
    assert early.id in ids and prev_night.id not in ids

def test_book_and_price_snapshot(customer_client, catalog, slots, db):
    s = first_slot(customer_client)
    r = customer_client.post("/api/bookings", json={"package_code": "ALP-CB01", "slot_id": s["id"]})
    assert r.status_code == 201 and r.json()["price_snapshot_vnd"] == 1_200_000
    assert r.json()["channel"] == "web" and db.get(TimeSlot, s["id"]).booked_count == 1

def test_double_confirm_rejected(customer_client, catalog, slots):              # Review Focus 3
    body = {"package_code": "ALP-CB01", "slot_id": first_slot(customer_client)["id"]}
    assert customer_client.post("/api/bookings", json=body).status_code == 201
    assert customer_client.post("/api/bookings", json=body).status_code == 409

@pytest.mark.parametrize("case,status", [("full", 409), ("wrong_hospital", 400), ("past", 400), ("inactive", 404)])
def test_booking_rejections(customer_client, catalog, make_slot, db, case, status): ...
    # Tạo đúng tình huống theo case:
    #   full: khung capacity=1, đã có 1 chỗ được đặt
    #   wrong_hospital: khung GAM, gói ALP-CB01
    #   past: khung hôm qua
    #   inactive: gói active=False
    # Assert mã trạng thái = status.

def test_last_spot_concurrency(catalog, make_slot, engine, two_customer_ids):
    slot = make_slot("ALP", tomorrow_at(7), capacity=1)
    # Hai thread, mỗi thread một Session riêng từ engine test.
    # Cả hai gọi create_booking(..., slot_id=slot.id) cùng lúc, dùng threading.Barrier(2).
    # Assert: đúng 1 thành công, 1 ném BookingError("slot_full"); booked_count == 1.

def test_cancel_rules(customer_client, other_client, consultant_client, catalog, slots, db):
    bid = book(customer_client)
    assert other_client.post(f"/api/bookings/{bid}/cancel").status_code == 404
    assert customer_client.post(f"/api/bookings/{bid}/cancel").json()["status"] == "cancelled"
    assert customer_client.post(f"/api/bookings/{bid}/cancel").status_code == 409
    bid2 = book(customer_client)
    assert consultant_client.post(f"/api/consultant/bookings/{bid2}/cancel").status_code == 200

def test_cannot_cancel_past_booking(customer_client, catalog, past_booking_id, db):   # Review Focus 4
    before = db.get(Booking, past_booking_id).slot.booked_count
    assert customer_client.post(f"/api/bookings/{past_booking_id}/cancel").status_code == 400
    db.expire_all(); assert db.get(Booking, past_booking_id).slot.booked_count == before

def test_lists_are_scoped(customer_client, other_client, consultant_client, catalog, slots):
    book(customer_client); book(other_client, "GAM-CB01")
    assert len(customer_client.get("/api/bookings").json()) == 1
    rows = consultant_client.get("/api/consultant/bookings").json()
    assert len(rows) == 2 and all(r["customer_phone"] for r in rows)
    assert len(consultant_client.get("/api/consultant/bookings", params={"hospital": "GAM"}).json()) == 1

def test_checklist(customer_client, other_client, catalog, slots):
    bid = book(customer_client)
    items = customer_client.get(f"/api/bookings/{bid}/checklist").json()
    assert items[0]["text"].startswith("Nhịn ăn ít nhất 8 tiếng")
    assert items[-1]["text"] == "Đến trước giờ hẹn 15 phút để làm thủ tục"
    assert other_client.get(f"/api/bookings/{bid}/checklist").status_code == 404

def test_role_guards(client, customer_client, catalog, slots):
    assert client.post("/api/bookings", json={"package_code": "ALP-CB01", "slot_id": 1}).status_code == 401
    assert customer_client.get("/api/consultant/bookings").status_code == 403
```
Các hàm trợ giúp và fixture còn lại, đặt trong file test:
- `book(client, code="ALP-CB01") -> int`: đặt khung đầu tiên còn chỗ, trả id lịch hẹn.
- `tomorrow_at(hour) -> datetime`: giờ VN.
- `two_customer_ids`: tạo 2 user customer trong DB, trả về 2 id.
- `past_booking_id`: chèn trực tiếp một `TimeSlot` hôm qua (`booked_count=1`) và một `Booking` `booked` của khách trong `customer_client`. Bỏ qua `create_booking` vì hàm này chặn khung đã qua.

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `uv run pytest tests/test_booking.py -v`
Expected: FAIL.

- [ ] **Step 3: Viết service booking/prep, schema, router; gắn router vào `main.py`**

Thêm `/api/packages/{code}/slots` vào `api/packages.py`. Đặt route này trước hoặc sau `/{code}` đều được, vì path khác nhau.

- [ ] **Step 4: Chạy toàn bộ test + kiểm tra tay trên Swagger**

Run: `uv run pytest -v; uv run ruff check .`
Expected: toàn bộ PASS, ruff không báo lỗi.

Kiểm tra tay trên DB dev:
1. Chạy `uv run uvicorn app.main:app --reload` và mở `http://localhost:8000/docs`.
2. Đăng nhập bằng tài khoản khách mẫu, đặt một gói, xem checklist.
3. Đăng nhập tư vấn viên, xem thấy lịch vừa đặt.

- [ ] **Step 5: Commit**

```powershell
git add backend
git commit -m "feat(backend): khung giờ, đặt/hủy lịch có khóa hàng, checklist chuẩn bị, API tư vấn viên"
```

---

### Task 7: Chạy thử Gemini (cần API key của bạn)

Đây là bước thử nhanh (spike): không viết test, không đưa vào code chính. Kết quả quyết định thiết kế agent ở Kế hoạch 4.

**Files:**
- Modify: `backend/scripts/spike_llm.py`
- Modify: `docs/superpowers/specs/2026-11-21-mediflow-ai-design.md` (ghi kết quả vào mục 17)

**Interfaces:**
- Consumes: `Settings.llm_provider`, `llm_model`, `google_api_key`, `embedding_model`.
- Produces: tên model chat và model embedding đã chốt, `EMBEDDING_DIM`, kết luận Flash-Lite có đủ tốt cho agent hay không.

- [ ] **Step 1: Người dùng tạo key Gemini trên Google AI Studio và tự dán vào `backend/.env` (`GOOGLE_API_KEY=`)**

Kiểm tra tên model chính xác trong AI Studio, cập nhật `LLM_MODEL`.

- [ ] **Step 2: Viết `spike_llm.py`**

Script làm 3 việc:
1. **Gọi tool bằng tiếng Việt.** Khởi tạo model bằng `init_chat_model(settings.llm_model, model_provider=settings.llm_provider)` và `bind_tools` với 2 tool giả: `search_packages(gender, age, purpose, budget_max, city)` và `get_available_slots(package_code, date_from)`. Chạy 5 câu:
   1. "Tôi nam 35 tuổi muốn khám tổng quát ở Hà Nội"
   2. "Gói tim mạch dưới 5 triệu ở Đà Nẵng"
   3. "Đặt cho mẹ tôi 62 tuổi một gói người cao tuổi"
   4. "Gói ALP-CB01 còn lịch sáng thứ 7 không?"
   5. "Chào bạn" (câu này không được gọi tool)

   In tên tool và tham số model gọi cho từng câu.
2. **Rút JSON.** Gọi `with_structured_output` với model Pydantic `Intake(age: int | None, gender: str | None, purpose: str | None, budget_max: int | None)` cho câu "mình 28t, nữ, muốn tầm soát ung thư, tầm 4 củ". In kết quả.
3. **Embedding.** Gọi `GoogleGenerativeAIEmbeddings(model=settings.embedding_model).embed_query("nhịn ăn trước khi lấy máu")`. In độ dài vector.

- [ ] **Step 3: Chạy và đánh giá**

Run: `uv run python scripts/spike_llm.py`

Đạt khi:
- Câu 1–4 gọi đúng tool với tham số hợp lý, ví dụ `age=35`, `gender="male"`, `city` là Hà Nội, `budget_max=5000000`.
- Câu 5 không gọi tool.
- JSON ra đúng `age=28`, `gender` là nữ, `budget_max=4000000`.
- Có độ dài vector embedding.

- [ ] **Step 4: Ghi kết quả vào mục 17 của spec**

Ghi: model chat, model embedding, `EMBEDDING_DIM`, và quyết định.
- Đạt thì giữ Flash-Lite.
- Sai từ 2/5 câu trở lên thì Kế hoạch 4 dùng 3.8 Flash cho node agent, hoặc chuyển sang luồng nhiều bước cố định.

Báo người dùng kết quả.

- [ ] **Step 5: Commit**

```powershell
git add backend/scripts/spike_llm.py docs/superpowers/specs
git commit -m "chore: thử Gemini (gọi tool tiếng Việt, JSON, embedding) và ghi kết quả"
```
