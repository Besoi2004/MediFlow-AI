# Kế hoạch 3: Giao diện đặt khám (chưa có trợ lý)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** App đặt khám dùng được hoàn chỉnh mà **không cần agent**:
- trang chủ, danh sách và chi tiết bệnh viện;
- danh sách gói có bộ lọc, chi tiết gói, so sánh gói;
- đặt lịch qua form, lịch hẹn của tôi kèm checklist và nút hủy;
- đăng nhập/đăng ký;
- trang tư vấn viên xem và hủy lịch hẹn.

Kế hoạch này cũng sửa các lỗi nhỏ của backend còn để lại từ review Kế hoạch 1.

**Architecture:**
- **Next.js 16 App Router.** Mỗi `page.tsx` là server component chỉ bọc một client component `*View` trong `<Suspense>`.
- **Gọi dữ liệu:** client component gọi backend qua `/api/*` (Next rewrites sang FastAPI, cùng origin nên cookie đăng nhập đi kèm tự động). Mọi request đi qua `lib/api.ts`.
- **Định dạng:** tiền và giờ định dạng ở `lib/format.ts`, luôn theo giờ `Asia/Ho_Chi_Minh` bất kể múi giờ của trình duyệt.
- **Phân quyền:** `proxy.ts` chặn trang cần đăng nhập. Phân quyền thật nằm ở backend.

**Tech Stack:** Next.js 16.4, React 19, Tailwind 4, shadcn/ui (đã cài: button input card table tabs badge select dialog sheet calendar), Vitest (thêm mới, chỉ để test hàm trong `lib/`), backend FastAPI có sẵn.

**Spec:** `docs/superpowers/specs/2026-11-21-mediflow-ai-design.md` (mục 9 API, mục 10 Giao diện, mục 17 quyết định 4 và 6)

**Điều kiện:** Kế hoạch 1 và 2 đã xong.

## Global Constraints

- **Đọc tài liệu Next đúng phiên bản trước khi viết code Next:** đọc `frontend/AGENTS.md` và `frontend/node_modules/next/dist/docs/` (proxy, useSearchParams, Suspense, next/font). Next 16 đổi `middleware.ts` thành `proxy.ts` (`export function proxy(request)` + `export const config = { matcher }`).
- **Mẫu trang:** mỗi `app/**/page.tsx` là server component: `export default function Page() { return <Suspense fallback={<PageSkeleton/>}><XxxView/></Suspense>; }`. `XxxView` có `"use client"` và dùng `useParams` / `useSearchParams` khi cần.
- **Gọi API:** không gọi `fetch` trực tiếp trong component, luôn qua `api()` trong `lib/api.ts`.
- **Hiển thị tiền và giờ:** tiền luôn qua `formatVnd`, giờ luôn qua `formatDateTimeVN` hoặc `formatDayVN`.
- **Chữ và nhãn:** mọi chữ hiển thị bằng tiếng Việt có dấu. Tên bệnh viện đã có sẵn "(mô phỏng)".
- **Màn hình hẹp:** dùng được ở bề rộng 375px, không có thanh cuộn ngang.
- **Thư viện:** không thêm thư viện UI khác ngoài shadcn. Được `npx shadcn@latest add label skeleton separator` nếu cần.
- **Backend:** `cd backend; uv run pytest` và `uv run ruff check .` phải sạch.
- **Frontend:** `cd frontend; npm test`, `npm run lint`, `npm run build` phải sạch.
- **Commit:** message một dòng tiếng Việt, không có Co-Authored-By.

## Review Focus

1. **Backend tắt hoặc lỗi mạng:** trang hiện thông báo tiếng Việt ("Không kết nối được máy chủ…") kèm nút thử lại, không ra trang trắng. → test `api()` ở Task 2 + kiểm tra tay ở Task 4.
2. **Cookie hết hạn khi đang ở trang cần đăng nhập** (API trả 401): chuyển về `/login?next=<trang hiện tại>`, đăng nhập xong quay lại đúng trang. → test `safeNext` ở Task 3 + kiểm tra tay ở Task 5.
3. **Khung giờ vừa bị người khác lấy hết giữa lúc xem và lúc bấm xác nhận** (409): hiện "Khung giờ đã hết chỗ", tải lại danh sách giờ, không bỏ dở trạng thái. → kiểm tra tay ở Task 5.
4. **Trình duyệt đặt múi giờ khác:** giờ khám vẫn hiện theo giờ Việt Nam, chữ có dấu không lỗi font. → test `formatDateTimeVN` với `TZ=UTC` ở Task 2.
5. **Thông báo lỗi nhập liệu (422) bằng tiếng Việt, hiện đúng dưới ô bị sai.** → test backend ở Task 1 + test `api()` ở Task 2.

---

## Cấu trúc file

```
backend/app/main.py                 # + handler RequestValidationError tiếng Việt
backend/app/textnorm.py             # + today_vn()
backend/app/api/packages.py         # + giới hạn date_from
backend/app/api/consultant.py       # + giới hạn date
backend/app/schemas.py              # birth_date >= 1900-01-01 và < today_vn()
backend/app/services/booking.py     # chỉ đổi IntegrityError của uq_bookings_active
backend/tests/test_api_polish.py
.env.example                        # bỏ BACKEND_URL (chuyển sang frontend)
frontend/.env.example               # BACKEND_URL
frontend/package.json               # + vitest, script "test"
frontend/proxy.ts
frontend/lib/format.ts · format.test.ts
frontend/lib/api.ts · api.test.ts   # ApiError, api(), kiểu dữ liệu
frontend/lib/nav.ts · nav.test.ts   # safeNext()
frontend/lib/constants.ts           # DISCLAIMER, TAG_LABEL, CITY_OPTIONS
frontend/components/auth/AuthProvider.tsx
frontend/components/SiteHeader.tsx
frontend/components/PageState.tsx   # PageSkeleton, ErrorState (có nút thử lại), EmptyState
frontend/components/Disclaimer.tsx
frontend/components/catalog/{HospitalCard,PackageCard,PackageFilters,CompareBar,CompareTable}.tsx
frontend/components/booking/{SlotPicker,BookingSummary,PrepChecklist,BookingCard}.tsx
frontend/app/layout.tsx · page.tsx
frontend/app/{login,register,hospitals,hospitals/[code],packages,packages/[code],compare,book/[code],bookings,consultant}/page.tsx
frontend/app/**/_view.tsx           # client component của từng trang (tên file builder tự chọn, cùng thư mục)
```

---

### Task 1: Hoàn thiện API cho giao diện (lỗi tồn từ review Kế hoạch 1)

**Files:**
- Modify: `backend/app/main.py`, `backend/app/textnorm.py`, `backend/app/api/packages.py`, `backend/app/api/consultant.py`, `backend/app/schemas.py`, `backend/app/services/booking.py`, `.env.example`
- Create: `frontend/.env.example`
- Test: `backend/tests/test_api_polish.py`

**Interfaces:**
- Produces:
  - `app.textnorm.today_vn() -> date`, tức `datetime.now(VN_TZ).date()`. Thay các chỗ đang tự viết biểu thức này (route slots, `scripts/seed.py` main).
  - Định dạng 422 mới cho **mọi** lỗi validate, đúng dạng sau:
    ```json
    {"detail": "Dữ liệu không hợp lệ", "errors": [{"field": "password", "message": "Cần ít nhất 8 ký tự"}]}
    ```
    - `field` = phần tử cuối của `loc` (bỏ `body`/`query`/`path`).
    - Bảng đổi theo `type`:

      | `type` | `message` |
      |---|---|
      | `missing` | "Bắt buộc" |
      | `string_too_short` | "Cần ít nhất {min_length} ký tự" |
      | `string_too_long` | "Tối đa {max_length} ký tự" |
      | `string_pattern_mismatch` | "Sai định dạng" |
      | `value_error` | lấy `str(ctx["error"])` (các ValueError trong schemas đã viết tiếng Việt) |
      | `greater_than_equal` | "Phải từ {ge} trở lên" |
      | `less_than_equal` | "Không được lớn hơn {le}" |
      | loại khác | "Giá trị không hợp lệ" |

  - **Giới hạn ngày:** `date_from` (route slots) và `date` (route consultant) phải nằm trong `[today_vn() - 366 ngày, today_vn() + 366 ngày]`. Ngoài khoảng → 422 với cùng định dạng: `{"detail": "Dữ liệu không hợp lệ", "errors": [{"field": "date_from" | "date", "message": "Ngày ngoài phạm vi cho phép"}]}`.
  - **`RegisterIn.birth_date`:** phải `>= 1900-01-01` và `< today_vn()`. Sai thì báo "Ngày sinh không hợp lệ".
  - **`create_booking`:** chỉ đổi `IntegrityError` thành `BookingError("duplicate_booking")` khi `e.orig.diag.constraint_name == "uq_bookings_active"`. Lỗi khác thì rollback rồi raise lại nguyên gốc.
  - **`BACKEND_URL`:** chuyển từ `.env.example` gốc sang `frontend/.env.example`, kèm comment "copy thành frontend/.env.local".

- [ ] **Step 1: Viết test thất bại `tests/test_api_polish.py`**

```python
def test_422_is_vietnamese_with_field(client):
    r = client.post("/api/auth/register", json={"email": "x@y.test", "password": "123", "full_name": "A",
                                                "birth_date": "1990-01-01", "gender": "male", "phone": "0900000001"})
    body = r.json()
    assert r.status_code == 422 and body["detail"] == "Dữ liệu không hợp lệ"
    assert {"field": "password", "message": "Cần ít nhất 8 ký tự"} in body["errors"]

def test_422_missing_field(client):
    errors = client.post("/api/auth/login", json={"email": "a@b.test"}).json()["errors"]
    assert {"field": "password", "message": "Bắt buộc"} in errors

def test_422_value_error_message_kept(client):
    errors = client.post("/api/auth/login", json={"email": "sai", "password": "x"}).json()["errors"]
    assert {"field": "email", "message": "Email không hợp lệ"} in errors

@pytest.mark.parametrize("path,param", [("/api/packages/ALP-CB01/slots", "date_from")])
def test_far_dates_rejected(client, catalog, path, param):
    r = client.get(path, params={param: "9999-12-31"})
    assert r.status_code == 422 and r.json()["errors"][0]["field"] == param

def test_consultant_far_date_rejected(consultant_client):        # fixture chuyển từ test_booking sang conftest
    assert consultant_client.get("/api/consultant/bookings", params={"date": "9999-12-31"}).status_code == 422

def test_birth_date_too_old_rejected(client):
    r = client.post("/api/auth/register", json={"email": "o@y.test", "password": "matkhau123", "full_name": "A",
                                                "birth_date": "1800-01-01", "gender": "male", "phone": "0900000001"})
    assert {"field": "birth_date", "message": "Ngày sinh không hợp lệ"} in r.json()["errors"]

def test_non_duplicate_integrity_error_not_masked(db, catalog, make_slot):
    slot = make_slot("ALP", tomorrow_at(7))
    with pytest.raises(IntegrityError):
        create_booking(db, user_id=999_999, package_code="ALP-CB01", slot_id=slot.id)  # khóa ngoại sai

def test_date_from_window_end_is_vn_local(client, catalog, make_slot):     # lỗ hổng test từ review
    d = today_vn() + timedelta(days=2)
    last_in = make_slot("ALP", datetime.combine(d + timedelta(days=13), time(23, 30), VN_TZ))
    first_out = make_slot("ALP", datetime.combine(d + timedelta(days=14), time(6, 30), VN_TZ))
    ids = [s["id"] for s in client.get("/api/packages/ALP-CB01/slots", params={"date_from": d.isoformat()}).json()]
    assert last_in.id in ids and first_out.id not in ids

def test_consultant_date_filter_at_0630_vn(customer_client, consultant_client, catalog, make_slot, db):
    d = today_vn() + timedelta(days=3)
    slot = make_slot("ALP", datetime.combine(d, time(6, 30), VN_TZ))   # 23:30 UTC ngày hôm trước
    customer_client.post("/api/bookings", json={"package_code": "ALP-CB01", "slot_id": slot.id})
    rows = consultant_client.get("/api/consultant/bookings", params={"date": d.isoformat()}).json()
    assert len(rows) == 1
```
Chuyển các fixture `make_slot`, `customer`, `customer_client`, `other_client`, `consultant_client`, `two_customer_ids` và các hàm `today_vn`, `tomorrow_at` từ `tests/test_booking.py` sang `tests/conftest.py` để hai file test dùng chung. `today_vn` dùng bản trong `app.textnorm`.

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `uv run pytest tests/test_api_polish.py -q`
Expected: FAIL (422 còn dạng của FastAPI, ngày xa ra 500, IntegrityError bị nuốt).

- [ ] **Step 3: Viết handler, `today_vn`, giới hạn ngày, validator birth_date, kiểm tra tên constraint; chuyển BACKEND_URL**

Giới hạn ngày: viết thành validator của Pydantic gắn vào tham số query, `Annotated[date | None, Query(alias=...), AfterValidator(_within_a_year)]`, trong đó validator raise `ValueError("Ngày ngoài phạm vi cho phép")`. Lỗi sẽ đi qua handler 422 như mọi lỗi khác, ra đúng `field` và `message`. Đặt `_within_a_year` trong `app/textnorm.py` cạnh `today_vn()` để hai router dùng chung.

- [ ] **Step 4: Chạy test**

Run: `uv run pytest -q; uv run ruff check .`
Expected: toàn bộ PASS. Riêng các test cũ đang kiểm tra 422 thì chỉ cần còn đúng mã trạng thái.

- [ ] **Step 5: Commit**

```powershell
git add backend .env.example frontend/.env.example
git commit -m "fix: lỗi nhập liệu tiếng việt, giới hạn ngày, chuyển backend_url"
```

---

### Task 2: Nền frontend (font, format, api, đăng nhập, header, proxy)

**Files:**
- Modify: `frontend/app/layout.tsx`, `frontend/package.json`
- Create: `frontend/lib/format.ts`, `frontend/lib/format.test.ts`, `frontend/lib/api.ts`, `frontend/lib/api.test.ts`, `frontend/lib/constants.ts`, `frontend/components/auth/AuthProvider.tsx`, `frontend/components/SiteHeader.tsx`, `frontend/components/PageState.tsx`, `frontend/components/Disclaimer.tsx`, `frontend/proxy.ts`

**Interfaces:**
- Produces (`lib/format.ts`, không import gì ngoài chuẩn JS):
  - `formatVnd(n: number): string` → `"1.200.000đ"`.
  - `formatDateTimeVN(iso: string): string` → `"07:00 · Thứ Hai, 23/11/2026"`. Dùng `Intl.DateTimeFormat("vi-VN", { timeZone: "Asia/Ho_Chi_Minh" })`. Tên thứ viết hoa chữ đầu.
  - `dayKeyVN(iso: string): string` → `"2026-11-23"` (ngày theo giờ VN).
  - `formatDayVN(dayKey: string): string` → `"Thứ Hai, 23/11/2026"`.
  - `groupSlotsByDay<T extends { start_at: string }>(slots: T[]): { day: string; slots: T[] }[]`: theo thứ tự thời gian.
  - `toggleCode(codes: string[], code: string, max = 3): string[]`: có rồi thì bỏ ra; chưa có và chưa đủ `max` thì thêm vào cuối; đủ `max` thì giữ nguyên.
  - `maxFastingHours(items: { fasting_hours: number }[]): number`.
- Produces (`lib/constants.ts`):
  - `DISCLAIMER`: đúng nguyên văn `output_guard.DISCLAIMER` ở backend.
  - `TAG_LABEL: Record<string, string>`: `tong-quat` Tổng quát, `tim-mach` Tim mạch, `ung-thu` Tầm soát ung thư, `cao-tuoi` Người cao tuổi, `tien-hon-nhan` Tiền hôn nhân, `doanh-nghiep` Doanh nghiệp.
  - `CITY_OPTIONS = ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng"]`, `GENDER_LABEL`.
- Produces (`lib/api.ts`):
  - `class ApiError extends Error { status: number; fieldErrors: Record<string, string> }`.
  - `api<T>(path: string, opts?: { method?: string; json?: unknown; signal?: AbortSignal }): Promise<T>`:
    - `fetch("/api" + path)`; khi có `json` thì gửi kèm header `Content-Type: application/json`.
    - 204 → `undefined`.
    - Lỗi HTTP → `ApiError(status, detail ?? "Có lỗi xảy ra")`, với `fieldErrors` lấy từ `errors[]` của 422.
    - Lỗi mạng → `ApiError(0, "Không kết nối được máy chủ, vui lòng thử lại")`.
  - Kiểu dữ liệu, khớp đúng schema backend: `User`, `Hospital`, `HospitalDetail`, `PackageSummary`, `PackageItem`, `PackageDetail`, `CompareData`, `Slot`, `Booking`, `ConsultantBooking`, `ChecklistItem`.
- Produces (`components/auth/AuthProvider.tsx`):
  - `AuthProvider` và `useAuth(): { user: User | null; loading: boolean; refresh(): Promise<void>; logout(): Promise<void> }`.
  - Gọi `/auth/me` khi mount; 401 → `user = null`.
- Produces (`components/PageState.tsx`): `PageSkeleton`, `ErrorState({ message, onRetry })`, `EmptyState({ message })`.
- Produces (`proxy.ts`): matcher `["/bookings", "/book/:path*", "/consultant/:path*"]`. Không có cookie `access_token` → redirect `/login?next=<pathname+search>`.
- `layout.tsx`:
  - Font `Be_Vietnam_Pro` (next/font/google, `subsets: ["vietnamese", "latin"]`, `weight: ["400", "500", "600", "700"]`) thay Geist.
  - Bọc `AuthProvider` + `SiteHeader` + `<main className="mx-auto max-w-6xl px-4 py-6">`.
- `SiteHeader`:
  - Link "MediFlow", "Bệnh viện", "Gói khám".
  - Customer thấy thêm "Lịch của tôi"; consultant thấy "Tư vấn viên".
  - Bên phải: nút "Đăng nhập" hoặc tên người dùng + "Đăng xuất".
  - Trên màn hình hẹp, menu thu vào `Sheet`.

- [ ] **Step 1: Cài Vitest, viết test thất bại `lib/format.test.ts` và `lib/api.test.ts`**

```powershell
cd frontend
npm i -D vitest
```
Thêm `"test": "vitest run"` vào `scripts`.
```ts
// lib/format.test.ts
import { describe, expect, it } from "vitest";
import { dayKeyVN, formatDateTimeVN, formatVnd, groupSlotsByDay, maxFastingHours, toggleCode } from "./format";

describe("format", () => {
  it("formats VND", () => { expect(formatVnd(1200000)).toBe("1.200.000đ"); expect(formatVnd(990000)).toBe("990.000đ"); });
  it("shows Vietnam time whatever the runtime TZ", () => {          // Review Focus 4 (chạy với TZ=UTC)
    expect(formatDateTimeVN("2026-11-23T00:00:00Z")).toBe("07:00 · Thứ Hai, 23/11/2026");
    expect(dayKeyVN("2026-11-22T23:30:00Z")).toBe("2026-11-23");
  });
  it("groups slots by VN day in order", () => {
    const g = groupSlotsByDay([{ start_at: "2026-11-24T01:00:00Z" }, { start_at: "2026-11-22T23:30:00Z" }, { start_at: "2026-11-23T02:00:00Z" }]);
    expect(g.map((x) => x.day)).toEqual(["2026-11-23", "2026-11-24"]);
    expect(g[0].slots).toHaveLength(2);
  });
  it("toggles compare codes up to 3", () => {
    expect(toggleCode(["A"], "B")).toEqual(["A", "B"]);
    expect(toggleCode(["A", "B"], "A")).toEqual(["B"]);
    expect(toggleCode(["A", "B", "C"], "D")).toEqual(["A", "B", "C"]);
  });
  it("max fasting hours", () => { expect(maxFastingHours([{ fasting_hours: 0 }, { fasting_hours: 8 }, { fasting_hours: 6 }])).toBe(8); expect(maxFastingHours([])).toBe(0); });
});
```
```ts
// lib/api.test.ts
import { afterEach, describe, expect, it, vi } from "vitest";
import { api, ApiError } from "./api";

const reply = (status: number, body?: unknown) =>
  vi.stubGlobal("fetch", vi.fn(async () => new Response(body === undefined ? null : JSON.stringify(body), { status })));
afterEach(() => vi.unstubAllGlobals());

describe("api", () => {
  it("returns JSON", async () => { reply(200, [{ code: "ALP" }]); expect(await api("/hospitals")).toEqual([{ code: "ALP" }]); });
  it("maps 422 field errors", async () => {                           // Review Focus 5
    reply(422, { detail: "Dữ liệu không hợp lệ", errors: [{ field: "password", message: "Cần ít nhất 8 ký tự" }] });
    const e = await api("/auth/register", { method: "POST", json: {} }).catch((x) => x);
    expect(e).toBeInstanceOf(ApiError);
    expect(e.status).toBe(422);
    expect(e.fieldErrors).toEqual({ password: "Cần ít nhất 8 ký tự" });
  });
  it("uses backend detail for other errors", async () => {
    reply(409, { detail: "Khung giờ đã hết chỗ" });
    await expect(api("/bookings", { method: "POST", json: {} })).rejects.toMatchObject({ status: 409, message: "Khung giờ đã hết chỗ" });
  });
  it("turns network failure into a Vietnamese error", async () => {   // Review Focus 1
    vi.stubGlobal("fetch", vi.fn(async () => { throw new TypeError("Failed to fetch"); }));
    await expect(api("/packages")).rejects.toMatchObject({ status: 0, message: "Không kết nối được máy chủ, vui lòng thử lại" });
  });
  it("returns undefined on 204", async () => { reply(204); expect(await api("/auth/logout", { method: "POST" })).toBeUndefined(); });
});
```
Chạy test với `TZ=UTC`. Trên PowerShell: `$env:TZ="UTC"; npm test`.

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `npm test`
Expected: FAIL (module `./format`, `./api` chưa có).

- [ ] **Step 3: Viết `lib/*`, `AuthProvider`, `SiteHeader`, `PageState`, `Disclaimer`, `proxy.ts`, sửa `layout.tsx`**

- [ ] **Step 4: Kiểm tra**

Run: `npm test; npm run lint; npm run build`
Expected: test PASS, lint sạch, build xong. Build liệt kê `Proxy` và đủ các route.

Kiểm tra tay: chạy backend (`uv run uvicorn app.main:app --reload`) và `npm run dev`.
- Header hiện đúng chữ tiếng Việt có dấu.
- Vào `/bookings` khi chưa đăng nhập → chuyển sang `/login?next=%2Fbookings`.

- [ ] **Step 5: Commit**

```powershell
git add frontend
git commit -m "feat: nền frontend: font, định dạng, api, header, proxy"
```

---

### Task 3: Đăng nhập và đăng ký

**Files:**
- Create: `frontend/lib/nav.ts`, `frontend/lib/nav.test.ts`, view của `app/login` và `app/register`
- Modify: `frontend/app/login/page.tsx`, `frontend/app/register/page.tsx`

**Interfaces:**
- Consumes: `api`, `ApiError`, `useAuth().refresh`.
- Produces: `safeNext(next: string | null, fallback = "/"): string`. Chỉ nhận đường dẫn bắt đầu bằng `/` nhưng không bắt đầu bằng `//` hoặc `/\`; còn lại trả `fallback`.
- **Đăng nhập** (`/login`): form email + mật khẩu.
  - Thành công thì gọi `refresh()`, rồi chuyển tới `safeNext(next)`. Riêng consultant, khi `next` trống thì về `/consultant`.
  - 401 hiện thông báo của backend.
- **Đăng ký** (`/register`): form có các ô họ tên, email, mật khẩu, ngày sinh (input date), giới tính (Select Nam/Nữ), số điện thoại.
  - Lỗi 422 hiện dưới đúng ô, lấy từ `fieldErrors`. 409 hiện thông báo chung.
  - Thành công thì như đăng nhập.
- Có link qua lại giữa hai trang, giữ nguyên `next`.

- [ ] **Step 1: Viết test thất bại `lib/nav.test.ts`**

```ts
import { describe, expect, it } from "vitest";
import { safeNext } from "./nav";
describe("safeNext", () => {                                           // Review Focus 2
  it("keeps internal paths", () => { expect(safeNext("/bookings")).toBe("/bookings"); expect(safeNext("/book/ALP-CB01?x=1")).toBe("/book/ALP-CB01?x=1"); });
  it("rejects external or empty", () => {
    for (const bad of [null, "", "https://evil.test", "//evil.test", "/\\evil.test", "bookings"]) expect(safeNext(bad)).toBe("/");
  });
});
```

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `npm test`
Expected: FAIL (`./nav` chưa có).

- [ ] **Step 3: Viết `safeNext` và hai trang**

- [ ] **Step 4: Kiểm tra**

Run: `npm test; npm run lint; npm run build`
Expected: sạch.

Kiểm tra tay:
1. Đăng ký tài khoản mới với mật khẩu "123": lỗi hiện dưới ô mật khẩu.
2. Đăng ký đúng: header hiện tên.
3. Đăng xuất rồi đăng nhập lại bằng email viết hoa: được.
4. Đăng nhập tài khoản tư vấn viên mẫu: tới `/consultant`.

- [ ] **Step 5: Commit**

```powershell
git add frontend
git commit -m "feat: trang đăng nhập và đăng ký"
```

---

### Task 4: Danh mục: trang chủ, bệnh viện, gói, chi tiết gói, so sánh

**Files:**
- Create: `frontend/components/catalog/{HospitalCard,PackageCard,PackageFilters,CompareBar,CompareTable}.tsx`, view của các trang dưới đây
- Modify: `frontend/app/page.tsx`, `app/hospitals/page.tsx`, `app/hospitals/[code]/page.tsx`, `app/packages/page.tsx`, `app/packages/[code]/page.tsx`, `app/compare/page.tsx`

**Interfaces:**
- Consumes: `api` + các kiểu dữ liệu, `formatVnd`, `toggleCode`, `maxFastingHours`, `TAG_LABEL`, `CITY_OPTIONS`, `DISCLAIMER`, `PageState`.
- Produces (component, Kế hoạch 5 dùng lại trong khung chat):
  - `PackageCard({ pkg: PackageSummary; compareSelected?: boolean; onToggleCompare?: () => void; compact?: boolean })`:
    - hiện mã, tên, bệnh viện, giá, nhãn tag;
    - nút "Chi tiết" (link `/packages/{code}`) và "Đặt lịch" (link `/book/{code}`);
    - nút "So sánh" chỉ hiện khi có `onToggleCompare`;
    - `compact` dùng cho khung chat.
  - `CompareTable({ data: CompareData })`:
    - một cột cho mỗi gói (tên, bệnh viện, giá);
    - một hàng cho mỗi hạng mục, ô ghi ✓ hoặc —;
    - trên màn hình hẹp thì cuộn ngang **trong** bảng, không cuộn cả trang.
  - `HospitalCard({ hospital: Hospital })`.
- **Trang chủ `/`:**
  - Tiêu đề + mô tả ngắn.
  - Các nút loại gói (`TAG_LABEL`) dẫn tới `/packages?tag=...`.
  - Danh sách bệnh viện (`/hospitals`).
  - Ô "Hỏi trợ lý" chưa làm, để Kế hoạch 5.
- **`/hospitals`:** Select tỉnh/thành → `?city=`; danh sách `HospitalCard`.
- **`/hospitals/[code]`:** thông tin bệnh viện + `PackageCard` các gói.
- **`/packages`:** `PackageFilters` đọc và ghi query string.
  - Các tham số lọc: `city`, `tag`, `gender`, `age`, `price_max`, cộng thêm `compare` = danh sách mã cách nhau dấu phẩy.
  - Danh sách `PackageCard` có nút So sánh dùng `toggleCode`.
  - `CompareBar` dính dưới màn hình khi có ≥ 1 mã: "So sánh (n)", dẫn tới `/compare?codes=...` khi n ≥ 2.
- **`/packages/[code]`:**
  - Tên, bệnh viện, giá, đối tượng (giới, tuổi).
  - Bảng hạng mục theo `category`.
  - Khối "Chuẩn bị trước khám": nếu `maxFastingHours > 0` thì dòng đầu là "Nhịn ăn ít nhất N tiếng trước giờ khám (được uống nước lọc)", sau đó các `prep_instruction` khác rỗng (bỏ trùng).
  - Nút "Đặt lịch", `Disclaimer`.
- **`/compare?codes=A,B[,C]`:** `CompareTable`. Lỗi 400/404 thì hiện thông báo của backend + link về `/packages`.

- [ ] **Step 1: Viết các component và trang**

Phần logic có thể test (lọc, so sánh, giờ nhịn ăn) đã có test ở Task 2; bước này chỉ ghép giao diện.

- [ ] **Step 2: Kiểm tra**

Run: `npm test; npm run lint; npm run build`
Expected: sạch.

Kiểm tra tay, chạy cả backend lẫn frontend, ở bề rộng 1280px và 375px:
1. Lọc "Hà Nội + Tổng quát + Nam + 35": chỉ còn gói ALP phù hợp.
2. Chọn so sánh `GAM-CB01` và `ALP-CB01`: bảng có hàng `XN-NUOCTIEU` với — / ✓.
3. Chi tiết `ALP-CB01`: dòng đầu là nhịn ăn 8 tiếng, không lặp.
4. Tắt backend rồi tải lại `/packages`: hiện `ErrorState` tiếng Việt, có nút thử lại (Review Focus 1).
5. Ở 375px không có thanh cuộn ngang của cả trang.

- [ ] **Step 3: Commit**

```powershell
git add frontend
git commit -m "feat: trang bệnh viện, gói khám, chi tiết và so sánh"
```

---

### Task 5: Đặt lịch và lịch hẹn của tôi

**Files:**
- Create: `frontend/components/booking/{SlotPicker,BookingSummary,PrepChecklist,BookingCard}.tsx`, view của `app/book/[code]` và `app/bookings`
- Modify: `frontend/app/book/[code]/page.tsx`, `frontend/app/bookings/page.tsx`

**Interfaces:**
- Consumes: `api`, `groupSlotsByDay`, `formatDateTimeVN`, `formatDayVN`, `formatVnd`, `safeNext`, `useAuth`.
- Produces (Kế hoạch 5 dùng lại):
  - `SlotPicker({ slots: Slot[]; selectedId?: number; onSelect(slot: Slot): void })`: nhóm theo ngày VN; mỗi giờ là một nút, kèm "còn N chỗ".
  - `BookingSummary({ hospitalName, packageName, startAt, priceVnd })`.
  - `PrepChecklist({ items: ChecklistItem[] })`: mỗi dòng là chữ, kèm tên các hạng mục liên quan (chữ nhỏ).
  - `BookingCard({ booking: Booking; onCancel?: () => void })`.
- **`/book/[code]`:**
  - Tải chi tiết gói và `/packages/{code}/slots`, chọn giờ bằng `SlotPicker`, hiện `BookingSummary`.
  - Nút "Xác nhận đặt lịch" bị khóa trong lúc gửi request. Gửi `POST /bookings` rồi chuyển tới `/bookings?new={id}`.
  - Xử lý lỗi:
    - 409 → hiện thông báo, tải lại giờ, bỏ chọn giờ cũ (Review Focus 3).
    - 401 → `/login?next=/book/{code}` (Review Focus 2).
    - 403 (tài khoản tư vấn viên) → "Tài khoản tư vấn viên không đặt lịch được".
- **`/bookings`:**
  - Danh sách `BookingCard`; lịch sắp tới lên trước, lịch đã hủy mờ đi; lịch có id trùng `new` được tô nổi.
  - Mỗi lịch có nút "Xem chuẩn bị" (tải `/bookings/{id}/checklist` → `PrepChecklist`) và nút "Hủy".
  - Nút "Hủy" mở `Dialog` xác nhận → `POST /bookings/{id}/cancel`. 400 "Khung giờ đã qua" thì hiện thông báo.

- [ ] **Step 1: Viết component và hai trang**

- [ ] **Step 2: Kiểm tra**

Run: `npm test; npm run lint; npm run build`
Expected: sạch.

Kiểm tra tay:
1. Khách mẫu đặt `ALP-TQNAM`: tới `/bookings` thấy lịch được tô nổi, xem checklist có dòng nhịn ăn.
2. Mở hai trình duyệt cùng chọn một khung giờ chỉ còn 1 chỗ (đặt `capacity=1` bằng SQL trên DB dev), người thứ hai bấm xác nhận: thấy "Khung giờ đã hết chỗ", danh sách giờ tải lại.
3. Xóa cookie `access_token` rồi bấm xác nhận: về trang đăng nhập, đăng nhập xong quay lại `/book/ALP-TQNAM`.
4. Hủy lịch: trạng thái thành "Đã hủy".

- [ ] **Step 3: Commit**

```powershell
git add frontend
git commit -m "feat: đặt lịch qua form và trang lịch hẹn của tôi"
```

---

### Task 6: Trang tư vấn viên: lịch hẹn

**Files:**
- Modify: `frontend/app/consultant/page.tsx` (+ view)

**Interfaces:**
- Consumes: `GET /consultant/bookings?hospital=&status=&date=`, `POST /consultant/bookings/{id}/cancel`, `GET /hospitals`, `useAuth`.
- Produces:
  - Trang `/consultant`, chỉ hiện nội dung khi `user.role === "consultant"`. Role khác hiện "Trang này chỉ dành cho tư vấn viên".
  - Bộ lọc: Select bệnh viện, input ngày, Select trạng thái (Tất cả / Đã đặt / Đã hủy), lưu trên query string.
  - Bảng cột: Giờ khám (VN), Khách (tên, SĐT, email), Gói, Bệnh viện, Giá, Kênh (web/trợ lý), Trạng thái, nút Hủy (có Dialog xác nhận).
  - Màn hình hẹp: bảng cuộn ngang trong khung.
  - Để chừa chỗ cho tab "Cảnh báo cờ đỏ" mà Kế hoạch 5 sẽ thêm, bọc nội dung trong `Tabs` chỉ có một tab "Lịch hẹn".

- [ ] **Step 1: Viết trang**

- [ ] **Step 2: Kiểm tra**

Run: `npm test; npm run lint; npm run build`
Expected: sạch.

Kiểm tra tay:
- Tư vấn viên mẫu thấy lịch vừa đặt ở Task 5, lọc theo GAM thì không thấy lịch đó, hủy được.
- Khách đăng nhập vào `/consultant` thấy thông báo không có quyền.

- [ ] **Step 3: Commit + cập nhật trạng thái**

Sửa bảng trong `CLAUDE.md`: Kế hoạch 3 → "xong".
```powershell
git add frontend CLAUDE.md
git commit -m "feat: trang tư vấn viên xem và hủy lịch hẹn"
```
