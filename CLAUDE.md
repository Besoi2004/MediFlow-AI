# MediFlow-AI — ghi chú cho Claude

Dự án tự học theo đề VMEC-15: nền tảng đặt lịch gói khám định kỳ của nhiều bệnh viện (mô phỏng) có trợ lý AI. Chỉ làm phần **Cơ bản**; danh sách phần Nâng cao đang hoãn nằm ở mục 2 của spec.

- Spec (nguồn quyết định): `docs/superpowers/specs/2026-11-21-mediflow-ai-design.md`
- Kế hoạch, làm theo thứ tự, mỗi kế hoạch dùng skill `superpowers:executing-plans`:

| # | File | Trạng thái |
|---|---|---|
| 1 | `docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md` | xong |
| 2 | `docs/superpowers/plans/2026-11-21-plan-2-loi-an-toan.md` | chưa làm |
| 3 | `docs/superpowers/plans/2026-11-21-plan-3-giao-dien-dat-kham.md` | chưa làm |
| 4 | `docs/superpowers/plans/2026-11-21-plan-4-agent.md` | chưa làm |
| 5 | `docs/superpowers/plans/2026-11-21-plan-5-tro-ly-tren-giao-dien.md` | chưa làm |
| 6 | `docs/superpowers/plans/2026-11-21-plan-6-deploy.md` | chưa làm |

Làm xong một kế hoạch thì sửa cột trạng thái ở bảng này trong cùng commit cuối.

## Quy tắc của người dùng

- **Commit message: một dòng ngắn, đơn giản, tiếng Việt có dấu** (ví dụ `feat: api danh mục gói khám`). **Không** thêm `Co-Authored-By: Claude` hay bất kỳ dấu hiệu Claude nào, kể cả trong mô tả PR.
- Trả lời người dùng bằng tiếng Việt. Chữ hiển thị trong app bằng tiếng Việt.
- Không bao giờ in hay commit nội dung `backend/.env` (có JWT secret, mật khẩu seed, API key Gemini).

## Chạy và test

- Cần Docker Desktop đang chạy (`docker compose up -d` ở gốc repo). Trên Windows, Docker Desktop có thể không tự bật sau khi khởi động lại máy.
- Backend: `cd backend; uv sync; uv run alembic upgrade head; uv run python -m scripts.seed; uv run pytest`.
- URL database phải dùng `127.0.0.1`, **không** dùng `localhost`: Postgres chỉ nghe IPv4, `localhost` trên Windows thử IPv6 trước và treo khoảng 20 giây mỗi kết nối.
- Frontend (Next.js 16): đọc `frontend/AGENTS.md` trước khi viết code Next.js; tài liệu đúng phiên bản nằm ở `frontend/node_modules/next/dist/docs/`.
- Máy mới: xem mục "Chạy trên máy khác" trong `README.md`.
