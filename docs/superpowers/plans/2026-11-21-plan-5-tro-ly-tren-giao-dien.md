# Kế hoạch 5: Trợ lý AI trên giao diện

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Nút trợ lý nổi trên mọi trang.
- Tự mở ở lần đầu vào web, với lời chào và 3 câu gợi ý viết sẵn.
- Biết trang đang xem, hiện các khối dữ liệu (thẻ gói, bảng so sánh, chọn giờ, checklist, cảnh báo cấp cứu, disclaimer).
- Đặt lịch có thẻ xác nhận. Khách chưa đăng nhập thì đăng nhập/đăng ký ngay trong khung chat.
- Tư vấn viên có thêm tab "Cảnh báo cờ đỏ" và trang đọc hội thoại.

**Architecture:**
- **`AssistantProvider`** (React context ở `layout.tsx`) giữ conversation id (lưu cả vào `localStorage`), trạng thái mở/đóng và `page_context` của trang hiện tại.
- **`AssistantWidget`:**
  - màn hình rộng: panel cố định ở góc phải dưới;
  - màn hình hẹp: mở bằng `Sheet`, trước đó chỉ hiện bong bóng lời chào.
- **Khối dữ liệu:** `BlockView` render từng block bằng chính các component đã làm ở Kế hoạch 3 (`PackageCard compact`, `CompareTable`, `SlotPicker`, `PrepChecklist`, `Disclaimer`, `BookingCard`).
- **Logic test được** nằm trong `lib/assistant.ts` (hàm thuần, có test Vitest).

**Tech Stack:** Next.js 16, React 19, shadcn/ui, Vitest; API `/api/conversations*` và `/api/consultant/alerts*` từ Kế hoạch 4.

**Spec:** `docs/superpowers/specs/2026-11-21-mediflow-ai-design.md` (mục 10 "Trợ lý nổi", mục 17 quyết định 4 và 5)

**Điều kiện:** Kế hoạch 1–4 đã xong. Backend có `GOOGLE_API_KEY` để thử với Gemini thật.

## Global Constraints

- **Next.js:** giữ các quy tắc của Kế hoạch 3: mẫu `page.tsx` bọc `<Suspense>`, chỉ gọi API qua `api()`, đọc tài liệu Next trong `node_modules`, dùng được ở 375px, mọi chữ tiếng Việt.
- **Lời chào và gợi ý:** viết sẵn trong code, không gọi API.
- **`localStorage`:** mọi lần đọc/ghi đặt trong `try/catch`, qua `safeStorage()`. Lỗi thì coi như "đã thấy", không tự mở.
- **Chống bấm hai lần:** nút gửi, Xác nhận, Hủy bị khóa khi đang có request.
- **Không render HTML từ chữ của trợ lý:** hiện chữ thuần, xuống dòng bằng CSS `whitespace-pre-wrap`.
- **Kiểm tra:** `cd frontend; npm test; npm run lint; npm run build` sạch sau mỗi task.
- **Commit:** message một dòng tiếng Việt, không có Co-Authored-By.

## Review Focus

1. **`localStorage` không dùng được** (chế độ ẩn danh, bị chặn): không tự mở, nhưng bấm nút vẫn chat được. → test `shouldAutoOpen` ở Task 1.
2. **Conversation id trong `localStorage` không còn dùng được** (404: hội thoại của người khác, hoặc DB vừa reset): âm thầm tạo hội thoại mới, không hiện lỗi. → test `resolveConversation` ở Task 1.
3. **Bấm Xác nhận hai lần nhanh:** chỉ gửi một request. Request thứ hai nếu có trả 409 thì hiện thông báo nhẹ, không lặp thẻ đã đặt. → kiểm tra tay ở Task 3.
4. **Trên điện thoại:** panel không che ô nhập khi bàn phím bật, có nút đóng rõ ràng. → kiểm tra tay ở Task 2.
5. **Chuyển từ trang gói này sang gói khác khi panel đang mở:** tin nhắn tiếp theo gửi đúng `page_context` mới. → kiểm tra tay ở Task 3.

---

## Cấu trúc file

```
frontend/lib/assistant.ts · assistant.test.ts
frontend/lib/api.ts                                   # + kiểu PageContext, ChatMessage, Turn, Conversation, PendingBooking, Alert
frontend/components/auth/LoginForm.tsx · RegisterForm.tsx   # tách từ trang login/register của Kế hoạch 3
frontend/components/assistant/AssistantProvider.tsx
frontend/components/assistant/AssistantWidget.tsx
frontend/components/assistant/WelcomeMessage.tsx
frontend/components/assistant/MessageList.tsx
frontend/components/assistant/BlockView.tsx
frontend/components/assistant/BookingConfirm.tsx
frontend/components/assistant/InlineLogin.tsx
frontend/components/assistant/UrgentAlert.tsx
frontend/components/assistant/usePageContext.ts
frontend/app/layout.tsx · page.tsx
frontend/app/{packages,packages/[code],hospitals/[code],compare,bookings}/  # gọi usePageContext
frontend/app/consultant/page.tsx                      # + tab Cảnh báo cờ đỏ
frontend/app/consultant/conversations/[id]/page.tsx
```

---

### Task 1: Logic trợ lý và provider

**Files:**
- Create: `frontend/lib/assistant.ts`, `frontend/lib/assistant.test.ts`, `frontend/components/assistant/AssistantProvider.tsx`, `frontend/components/assistant/usePageContext.ts`
- Modify: `frontend/lib/api.ts`, `frontend/app/layout.tsx`

**Interfaces:**
- Consumes: `api`, `ApiError`; các API `POST /conversations`, `GET /conversations/{id}`, `POST /conversations/{id}/messages`, `POST /conversations/{id}/confirm`.
- Produces (`lib/api.ts`), kiểu khớp schema backend Kế hoạch 4:
  - `PageContext`, `ChatMessage { role; text; blocks: Block[]; created_at }`;
  - `PendingBooking` (payload `confirm_booking`);
  - `Turn { messages; pending_confirmation; remaining_today }`, `Conversation { id; messages; pending_confirmation; remaining_today }`;
  - `AlertItem` (khớp `AlertOut`).
- Produces (`lib/assistant.ts`, không phụ thuộc React):
  - `SEEN_KEY = "mediflow.assistant_seen"`, `CONV_KEY = "mediflow.conversation_id"`, `AUTO_OPEN_DELAY_MS = 2000`, `MOBILE_QUERY = "(max-width: 639px)"`.
  - `SUGGESTIONS = ["Gói nào hợp với tôi?", "So sánh gói tổng quát", "Cần chuẩn bị gì trước khám?"]`.
  - `WELCOME = "Xin chào! Mình là trợ lý MediFlow. Mình giúp bạn chọn gói khám hợp tuổi và nhu cầu, so sánh gói, đặt lịch và hướng dẫn chuẩn bị trước khám."`.
  - `type KVStore = Pick<Storage, "getItem" | "setItem" | "removeItem">`.
  - `safeStorage(): KVStore | null`: thử `window.localStorage` bằng một lần ghi/xóa khóa thử; lỗi thì trả `null`.
  - `shouldAutoOpen(s: KVStore | null): boolean`: `false` nếu `s` là `null`, nếu `getItem(SEEN_KEY) === "1"`, hoặc nếu `getItem` ném lỗi.
  - `markSeen(s)`, `loadConversationId(s)`, `saveConversationId(s, id | null)`: không bao giờ ném lỗi.
  - `type Block`: union theo `type` của Kế hoạch 4 (`packages`, `hospitals`, `package_details`, `compare`, `slots`, `checklist`, `sources`, `booked`, `error`, `urgent`, `see_doctor`, `disclaimer`).
  - `isKnownBlock(b: { type: string }): b is Block`.
  - `slotChoiceMessage(packageCode: string, slot: Slot): string` → `"Mình chọn khung giờ 07:00 · Thứ Hai, 23/11/2026 (mã khung 12) cho gói [ALP-CB01]"`.
  - `resolveConversation(savedId: string | null, fetchConv: (id) => Promise<Conversation>, createConv: () => Promise<Conversation>): Promise<Conversation>`: có `savedId` thì thử `fetchConv`; gặp `ApiError` 404 thì `createConv()`; lỗi khác thì ném tiếp; không có `savedId` thì `createConv()`.
- Produces (`AssistantProvider` + `useAssistant()`):
  - Trạng thái: `{ open; setOpen; conversation: Conversation | null; messages: ChatMessage[]; pending: PendingBooking | null; remaining: number | null; busy: boolean; error: string | null }`.
  - Hành động: `send(text)`, `confirm(approved)`, `ensureConversation()`, `pageContext`, `setPageContext(ctx)`, `reloadAfterLogin()`.
  - `send`:
    - hiện ngay tin của khách, gọi API, thay bằng `messages` của `Turn` (bản đã che PII);
    - 429 thì `error = detail`, đánh dấu `needLogin` nếu đang là khách;
    - lỗi mạng thì `error`.
  - `confirm` bị khóa khi `busy`; 409 thì `error = detail`.
  - Gửi tin đầu tiên thì gọi `markSeen`.
- Produces (`usePageContext(ctx: PageContext)`): gọi `setPageContext(ctx)` mỗi khi `ctx` đổi (so sánh bằng `JSON.stringify`). Khi unmount thì đặt về `{ page: "other" }`.
- `layout.tsx`: bọc `AssistantProvider` **bên trong** `AuthProvider`.

- [ ] **Step 1: Viết test thất bại `lib/assistant.test.ts`**

```ts
import { describe, expect, it, vi } from "vitest";
import { ApiError } from "./api";
import { isKnownBlock, markSeen, resolveConversation, shouldAutoOpen, slotChoiceMessage, SEEN_KEY } from "./assistant";

const memory = () => { const m = new Map<string, string>(); return { getItem: (k: string) => m.get(k) ?? null, setItem: (k: string, v: string) => void m.set(k, v), removeItem: (k: string) => void m.delete(k) }; };

describe("auto open", () => {
  it("opens once", () => { const s = memory(); expect(shouldAutoOpen(s)).toBe(true); markSeen(s); expect(shouldAutoOpen(s)).toBe(false); });
  it("never opens without storage", () => {                                    // Review Focus 1
    expect(shouldAutoOpen(null)).toBe(false);
    const broken = { getItem: () => { throw new Error("blocked"); }, setItem: () => { throw new Error("blocked"); }, removeItem: () => {} };
    expect(shouldAutoOpen(broken)).toBe(false);
    expect(() => markSeen(broken)).not.toThrow();
  });
});

describe("resolveConversation", () => {                                        // Review Focus 2
  const conv = (id: string) => ({ id, messages: [], pending_confirmation: null, remaining_today: 10 });
  it("reuses saved id", async () => { const create = vi.fn(); expect((await resolveConversation("a", async () => conv("a"), create)).id).toBe("a"); expect(create).not.toHaveBeenCalled(); });
  it("creates new when saved one is gone", async () => {
    const got = await resolveConversation("old", async () => { throw new ApiError(404, "Không tìm thấy cuộc trò chuyện"); }, async () => conv("new"));
    expect(got.id).toBe("new");
  });
  it("rethrows other errors", async () => {
    await expect(resolveConversation("x", async () => { throw new ApiError(0, "mạng"); }, async () => conv("n"))).rejects.toMatchObject({ status: 0 });
  });
});

describe("blocks", () => {
  it("knows block types", () => { expect(isKnownBlock({ type: "packages" })).toBe(true); expect(isKnownBlock({ type: "script" })).toBe(false); });
  it("builds slot choice message in VN time", () => {
    expect(slotChoiceMessage("ALP-CB01", { id: 12, start_at: "2026-11-23T00:00:00Z", remaining: 3 }))
      .toBe("Mình chọn khung giờ 07:00 · Thứ Hai, 23/11/2026 (mã khung 12) cho gói [ALP-CB01]");
  });
});
```

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `npm test`
Expected: FAIL (`./assistant` chưa có).

- [ ] **Step 3: Viết `lib/assistant.ts`, kiểu trong `lib/api.ts`, `AssistantProvider`, `usePageContext`; sửa `layout.tsx`**

- [ ] **Step 4: Kiểm tra**

Run: `npm test; npm run lint; npm run build`
Expected: sạch.

- [ ] **Step 5: Commit**

```powershell
git add frontend
git commit -m "feat: logic và provider của trợ lý trên giao diện"
```

---

### Task 2: Khung chat nổi, lời chào, hiện khối dữ liệu

**Files:**
- Create: `frontend/components/assistant/{AssistantWidget,WelcomeMessage,MessageList,BlockView,UrgentAlert}.tsx`
- Modify: `frontend/app/layout.tsx`, `frontend/app/page.tsx`

**Interfaces:**
- Consumes: `useAssistant`, `lib/assistant.ts`, component Kế hoạch 3 (`PackageCard compact`, `HospitalCard`, `CompareTable`, `SlotPicker`, `PrepChecklist`, `BookingCard`, `Disclaimer`).
- Produces:
  - **`AssistantWidget`:**
    - Nút tròn cố định góc phải dưới (`aria-label="Mở trợ lý MediFlow"`).
    - Khi mở:
      - màn hình rộng: panel 380×560px;
      - màn hình hẹp: `Sheet` toàn màn hình, có nút đóng `aria-label="Đóng trợ lý"`.
    - Panel gồm: header ("Trợ lý MediFlow" + nút "Cuộc trò chuyện mới" + nút đóng), `MessageList`, ô nhập + nút gửi, dòng "Còn N lượt hôm nay" khi là khách.
    - Ô nhập nằm dưới cùng, `MessageList` tự cuộn xuống tin mới.
    - Chưa có tin nào thì hiện `WelcomeMessage`.
  - **Tự mở lần đầu:** sau khi mount, `shouldAutoOpen(safeStorage())` đúng thì chờ `AUTO_OPEN_DELAY_MS`, rồi:
    - màn hình rộng (không khớp `MOBILE_QUERY`) → mở panel;
    - màn hình hẹp → bong bóng nhỏ cạnh nút với chữ `WELCOME` rút gọn và nút ✕.

    Đóng panel hoặc bóng thì `markSeen`.
  - **`WelcomeMessage`:** `WELCOME` + 3 nút `SUGGESTIONS`; bấm nút nào thì gửi đúng câu đó.
  - **`MessageList({ messages, readonly? })`:** tin khách canh phải, tin trợ lý canh trái kèm `BlockView` cho từng block.
  - **`BlockView({ block, readonly? })`** render theo `type`:
    - `packages`, `hospitals`, `package_details` → thẻ compact;
    - `compare` → `CompareTable`;
    - `slots` → `SlotPicker`; `onSelect` gửi `slotChoiceMessage` (khi `readonly` thì không chọn được);
    - `checklist` → `PrepChecklist`;
    - `sources` → danh sách "Nguồn: tiêu đề";
    - `booked` → `BookingCard`;
    - `error` → chữ đỏ nhạt;
    - `urgent` → `UrgentAlert` (khung đỏ, chữ đậm, nút `tel:115` "Gọi 115");
    - `see_doctor` → khung vàng;
    - `disclaimer` → `Disclaimer`;
    - loại lạ → bỏ qua.
  - **Trang chủ:** thêm ô "Hỏi trợ lý" (input + nút). Bấm thì `setOpen(true)` và `send(text)`.

- [ ] **Step 1: Viết component; gắn `AssistantWidget` vào `layout.tsx`; thêm ô trên trang chủ**

- [ ] **Step 2: Kiểm tra**

Run: `npm test; npm run lint; npm run build`
Expected: sạch.

Kiểm tra tay (backend chạy với Gemini thật):
1. Mở trang ở cửa sổ ẩn danh: sau khoảng 2 giây panel tự mở. Đóng rồi tải lại: không tự mở nữa.
2. Ở 375px: chỉ hiện bong bóng. Bấm nút mở thì `Sheet` toàn màn hình, có nút đóng; ô nhập không bị bàn phím che (giả lập bằng DevTools) (Review Focus 4).
3. Bấm gợi ý "Gói nào hợp với tôi?": trợ lý hỏi tuổi và giới (khách chưa đăng nhập).
4. Gõ "tôi bị khó thở dữ dội": hiện khung đỏ có nút Gọi 115.
5. Chặn `localStorage` bằng DevTools rồi tải lại: không tự mở, nhưng bấm nút vẫn chat được (Review Focus 1).

- [ ] **Step 3: Commit**

```powershell
git add frontend
git commit -m "feat: khung chat trợ lý nổi, lời chào và khối dữ liệu"
```

---

### Task 3: Xác nhận đặt lịch, đăng nhập trong khung chat, ngữ cảnh trang

**Files:**
- Create: `frontend/components/auth/LoginForm.tsx`, `frontend/components/auth/RegisterForm.tsx`, `frontend/components/assistant/BookingConfirm.tsx`, `frontend/components/assistant/InlineLogin.tsx`
- Modify: view của `app/login` và `app/register` (dùng 2 form mới), view của `app/packages`, `app/packages/[code]`, `app/hospitals/[code]`, `app/compare`, `app/bookings` (gọi `usePageContext`), `AssistantWidget.tsx`

**Interfaces:**
- Produces:
  - `LoginForm({ onSuccess(user: User): void; compact?: boolean })` và `RegisterForm({ onSuccess; compact? })`: tách nguyên logic từ hai trang của Kế hoạch 3 (lỗi dưới từng ô, gọi `refresh()` của auth). Hai trang `/login`, `/register` dùng lại, hành vi không đổi.
  - **`BookingConfirm({ pending: PendingBooking })`:**
    - Hiện `BookingSummary` (bệnh viện, gói, giờ VN, giá) cùng 2 nút "Xác nhận đặt lịch" và "Không đặt".
    - Nếu `pending.login_required` và `useAuth().user` là `null`: hiện `InlineLogin` thay cho 2 nút. Đăng nhập xong thì `reloadAfterLogin()` (tải lại hội thoại, lúc này đã thuộc tài khoản), rồi mới hiện 2 nút.
    - Hai nút bị khóa khi `busy` (Review Focus 3).
  - **`InlineLogin`:** tab "Đăng nhập" / "Đăng ký" dùng `LoginForm compact` / `RegisterForm compact`.
  - **Hết lượt (429):** `AssistantWidget` hiện `InlineLogin` khi lỗi 429 với khách.
  - **Ngữ cảnh trang:**
    - `/packages/[code]` → `{ page: "package", code }`;
    - `/hospitals/[code]` → `{ page: "hospital", code }`;
    - `/compare` → `{ page: "compare", codes }`;
    - `/packages` → `{ page: "packages" }`;
    - `/bookings` → `{ page: "bookings" }`;
    - `/` → `{ page: "home" }`;
    - các trang khác → `{ page: "other" }`.

- [ ] **Step 1: Tách form; viết `BookingConfirm` và `InlineLogin`; gắn `usePageContext` vào các trang**

- [ ] **Step 2: Kiểm tra**

Run: `npm test; npm run lint; npm run build`
Expected: sạch.

Kiểm tra tay:
1. **Khách chưa đăng nhập đặt lịch:**
   1. Hỏi trợ lý "đặt gói ALP-CB01 sáng thứ Hai", chọn giờ trong khối `slots`.
   2. Hiện thẻ xác nhận có ô đăng nhập ngay trong thẻ. Đăng ký tài khoản ngay trong thẻ.
   3. Bấm Xác nhận: thấy thẻ "đã đặt"; `/bookings` có lịch với kênh "trợ lý".
2. **Bấm Xác nhận hai lần thật nhanh:** chỉ một lịch được tạo (Review Focus 3).
3. **Ngữ cảnh trang:** mở `/packages/ALP-TQNAM`, hỏi "gói này có hợp với tôi không?": trợ lý nói về `ALP-TQNAM`. Không đóng panel, chuyển sang `/packages/BET-TQNU` rồi hỏi lại: trợ lý nói về `BET-TQNU` (Review Focus 5).
4. **Trang `/login` cũ** vẫn hoạt động như trước.

- [ ] **Step 3: Commit**

```powershell
git add frontend
git commit -m "feat: xác nhận đặt lịch và đăng nhập ngay trong khung chat"
```

---

### Task 4: Tư vấn viên: tab cảnh báo và trang đọc hội thoại

**Files:**
- Modify: `frontend/app/consultant/page.tsx` (+ view), `frontend/app/consultant/conversations/[id]/page.tsx` (+ view)

**Interfaces:**
- Consumes: `GET /consultant/alerts?status=`, `POST /consultant/alerts/{id}/resolve`, `GET /consultant/conversations/{id}`, `MessageList readonly`.
- Produces:
  - `/consultant`: `Tabs` có 2 tab, "Lịch hẹn" (đã có) và "Cảnh báo cờ đỏ". Tab đang chọn lưu ở `?tab=alerts`.
  - **Tab cảnh báo:**
    - Select trạng thái (Chưa xử lý / Đã xử lý), mặc định Chưa xử lý.
    - Danh sách: giờ (VN), badge mức độ ("Cấp cứu" đỏ / "Cần khám bác sĩ" vàng), cụm bị bắt.
    - Khách: tên + SĐT bấm gọi được (`tel:`), hoặc "Khách chưa đăng nhập".
    - Link "Xem hội thoại" và nút "Đã xử lý".
    - Header tab hiện số cảnh báo chưa xử lý.
  - **`/consultant/conversations/[id]`:** `MessageList readonly` của hội thoại (bản đã che PII), nút quay lại. Chỉ tư vấn viên xem được.

- [ ] **Step 1: Viết tab và trang**

- [ ] **Step 2: Kiểm tra**

Run: `npm test; npm run lint; npm run build`
Expected: sạch.

Kiểm tra tay:
1. Khách mẫu gõ "tôi đau ngực dữ dội, sđt 0901234567".
2. Tư vấn viên thấy cảnh báo "Cấp cứu" có tên và SĐT của khách (lấy từ hồ sơ, không phải từ tin nhắn).
3. Mở hội thoại: số trong tin nhắn đã thành `[SĐT]`.
4. Bấm "Đã xử lý": cảnh báo biến khỏi danh sách "Chưa xử lý".

- [ ] **Step 3: Commit + cập nhật trạng thái**

Sửa bảng trong `CLAUDE.md`: Kế hoạch 5 → "xong".
```powershell
git add frontend CLAUDE.md
git commit -m "feat: tab cảnh báo cờ đỏ và trang đọc hội thoại cho tư vấn viên"
```
