# MediFlow-AI — Thiết kế (phần Cơ bản của đề VMEC-15)

Ngày: 2026-11-21 · Trạng thái: đã duyệt (bản 2: nền tảng nhiều bệnh viện)

## 1. Mục đích và lý do

MediFlow là **nền tảng đặt lịch gói khám sức khỏe định kỳ của nhiều bệnh viện** (mô phỏng), có **trợ lý AI tích hợp**.
- **Không cần agent:** khách hàng tự xem bệnh viện, lọc và so sánh gói, đặt lịch qua form, quản lý lịch hẹn.
- **Với trợ lý AI** (nút nổi ở mọi trang): khách làm được các việc trên bằng hội thoại. Trợ lý biết trang khách đang xem, gợi ý gói hợp tuổi/giới/nhu cầu, phát hiện dấu hiệu cấp cứu.
- **Khuyến khích dùng trợ lý:** panel trợ lý tự mở ở lần đầu khách vào web. Khách chưa đăng nhập vẫn chat được, có giới hạn lượt; chỉ bước đặt lịch mới cần đăng nhập.
- **Tư vấn viên của nền tảng:** xem mọi lịch hẹn, hội thoại và cảnh báo cờ đỏ.

Theo đề VMEC-15. Lý do: **dự án tự học**. Không có hạn nộp, nhưng muốn xong nhanh mà vẫn chất lượng. Thành công = đạt các yêu cầu Cơ bản của đề (được giảm bớt nếu quá khó).

## 2. Mục tiêu, ngoài phạm vi, điều cấm

**Mục tiêu (phần Cơ bản):**
1. App deploy lên cloud, đăng nhập 2 vai trò: **khách hàng** và **tư vấn viên** (của nền tảng).
2. Giao diện đặt khám đầy đủ, không phụ thuộc agent: danh sách bệnh viện, danh sách và bộ lọc gói, chi tiết gói, so sánh gói (kể cả khác bệnh viện), đặt lịch, lịch hẹn của tôi, checklist chuẩn bị.
3. Trợ lý AI tích hợp: hỏi nhu cầu → gợi ý gói → so sánh → đặt lịch có xác nhận → hướng dẫn chuẩn bị. Trợ lý hiểu "gói này" / "bệnh viện này" theo trang đang xem. Trợ lý tự mở ở lần đầu vào web. Khách chưa đăng nhập chat được, có giới hạn lượt.
4. Mọi bệnh viện, gói, giá, hạng mục đều lấy từ DB (grounded), luôn kèm disclaimer.
5. Ràng buộc an toàn của đề: không chẩn đoán, không chỉ định thêm xét nghiệm ngoài gói, bảo vệ PII/PHI, phát hiện triệu chứng cấp → hướng đi khám/cấp cứu thay vì bán gói.

**Ngoài phạm vi (làm sau, đã ghi nhớ):**
- theo dõi hoàn thành hạng mục và nhắc mục còn thiếu; nhắc lịch qua email/SMS;
- HITL cho tư vấn viên điều chỉnh gợi ý;
- memory tiền sử; gợi ý theo yếu tố nguy cơ;
- tổng hợp kết quả sau khám;
- xử lý gói hết chỗ / đổi lịch;
- tương tác thuốc / chống chỉ định (DDInter); chuẩn hóa đầu ra HL7 FHIR; dữ liệu Synthea/MIMIC;
- màn hình quản lý bệnh viện/gói/khung giờ (bản Cơ bản nạp bằng seed);
- tư vấn viên riêng của từng bệnh viện;
- danh sách lịch sử hội thoại cho khách;
- tìm theo bản đồ/khoảng cách;
- thanh toán;
- streaming từng chữ;
- đa ngôn ngữ.

**Điều cấm (dù app vẫn chạy, xảy ra là thất bại):**
- AI nói ra một bệnh viện, gói, giá hoặc hạng mục không có trong DB.
- AI chẩn đoán bệnh, kê thuốc, hoặc khuyên làm xét nghiệm ngoài gói.
- Người có dấu hiệu cấp cứu vẫn được tư vấn gói khám như bình thường.
- Đặt lịch (qua form hay qua agent) mà người dùng chưa bấm xác nhận.
- Tên, số điện thoại, email hoặc CCCD bị gửi cho LLM hay ghi vào log.
- Khách hàng xem được dữ liệu của khách hàng khác.

## 3. Ràng buộc

- LLM miễn phí: **Gemini 3.5 Flash-Lite** (free tier ~500 lượt/ngày, 10–15 lượt/phút; số liệu từ blog, chưa xác minh chính thức). Google dùng dữ liệu free tier để cải thiện sản phẩm → **chỉ dùng dữ liệu mô phỏng**.
- Phải đổi được LLM sau này mà gần như không sửa code.
- Máy dev: Windows 11, có sẵn Python 3.13, Node 22, npm, Docker, Git. Chưa có `uv` và Postgres (Postgres chạy bằng Docker).
- **Bệnh viện, gói, giá đều là mô phỏng.** Tên bệnh viện phải rõ là hư cấu, không trùng bệnh viện thật, và luôn hiện nhãn "(mô phỏng)" trên giao diện.
- Toàn bộ giao diện và hội thoại bằng tiếng Việt.

## 4. Các hướng đã cân nhắc

| Hướng | Được | Mất |
|---|---|---|
| **A. Stack của đề: Next.js + FastAPI + LangGraph + Postgres/pgvector** ✅ đã chọn | Học đúng thứ đề yêu cầu; LangGraph có sẵn interrupt và checkpointer lưu hội thoại vào Postgres; Next.js làm tốt giao diện nhiều trang | 2 ngôn ngữ, 2 app phải deploy |
| B. Toàn Python + Streamlit/Chainlit | Nhanh nhất, 1 app | Không làm nổi một app đặt khám nhiều trang; lệch đề |
| C. Toàn TypeScript (Next.js + LangGraph.js) | 1 ngôn ngữ, 1 app | Bỏ FastAPI; thư viện y khoa (FHIR, Synthea) mạnh ở Python hơn |

**LLM:** đã cân nhắc Claude (trả phí), Gemini 3.5 Flash-Lite (miễn phí), Groq (miễn phí, tiếng Việt kém hơn), Ollama local (máy phải bật liên tục, khó deploy). **Đã chọn Gemini 3.5 Flash-Lite**, gọi qua lớp chat model chung của LangChain để đổi nhà cung cấp chỉ bằng `.env`.

**Tư vấn viên:** người dùng chọn **của nền tảng** (thấy tất cả), không phải của từng bệnh viện.

## 5. Kiến trúc tổng thể

```
Trình duyệt ──> Next.js (Vercel)
                  │  các trang đặt khám + nút trợ lý nổi
                  │  rewrites /api/* → backend (cùng origin, cookie không bị chặn)
                  ▼
               FastAPI (Render, Docker)
                  ├── Auth (JWT trong cookie httpOnly, phân quyền theo role)
                  ├── API: hospitals, packages, bookings, chat, consultant
                  ├── services/ (logic dùng chung cho API và tools của agent)
                  ├── Safety (luật cố định): red_flags, pii, output_guard
                  └── Agent (LangGraph) ──> Gemini (qua langchain init_chat_model)
                  ▼
               Postgres + pgvector (Neon)
                  ├── bảng nghiệp vụ (hospitals, packages, bookings, ...)
                  ├── bảng vector hướng dẫn chuẩn bị (RAG)
                  └── checkpoint của LangGraph (trạng thái hội thoại)
```

**Nguyên tắc cốt lõi:**
1. **Giao diện và agent dùng chung `services/`.** Đặt lịch qua form hay qua agent đều gọi cùng `booking.create()`, nên quy tắc chỉ viết một lần.
2. **Cái gì cần đúng tuyệt đối thì code quyết định**, LLM chỉ hội thoại, rút thông tin và giải thích:
   - Lọc gói = câu SQL.
   - Giá hiển thị = lấy từ DB, render bằng thẻ giao diện.
   - Cờ đỏ = luật YAML.
   - Đặt lịch = chờ người dùng bấm xác nhận.
   - Disclaimer = code tự gắn.

## 6. Dữ liệu mô phỏng và mô hình DB

**Bệnh viện mẫu.** Tên dưới đây là tạm; builder đặt tên hư cấu khác nếu muốn, miễn không trùng bệnh viện thật.

| Mã | Tên | Tỉnh/thành |
|---|---|---|
| ALP | Bệnh viện Alpha (mô phỏng) | Hà Nội |
| BET | Bệnh viện Beta (mô phỏng) | TP. Hồ Chí Minh |
| GAM | Bệnh viện Gamma (mô phỏng) | Đà Nẵng |

**Gói mẫu.** Mỗi bệnh viện có 5–6 gói. Cùng loại gói ở các bệnh viện khác nhau thì khác giá và khác hạng mục, để việc so sánh có ý nghĩa. Mã gói có tiền tố bệnh viện.

| Mã | Loại (tag) | Đối tượng | Giá mô phỏng (VND) |
|---|---|---|---|
| ALP-CB01 / BET-CB01 / GAM-CB01 | tong-quat | 18+, mọi giới | 1.200.000 / 1.450.000 / 990.000 |
| ALP-TQNAM / BET-TQNAM | tong-quat | nam 30+ | 3.500.000 / 3.900.000 |
| ALP-TQNU / BET-TQNU | tong-quat | nữ 30+ | 3.900.000 / 4.300.000 |
| ALP-TIM / GAM-TIM | tim-mach | 40+ | 5.200.000 / 4.600.000 |
| BET-UTNU / GAM-UTNU | ung-thu | nữ 25+ | 4.200.000 / 3.800.000 |
| ALP-CAOTUOI / GAM-CAOTUOI | cao-tuoi | 60+ | 4.800.000 / 4.100.000 |
| BET-THN | tien-hon-nhan | 18–45 | 2.500.000 |
| GAM-DN | doanh-nghiep | 18–60 | 900.000 |

- **Hạng mục:** mỗi gói gồm nhiều hạng mục (xét nghiệm máu, đường huyết, mỡ máu, X-quang ngực, siêu âm bụng, điện tim, ...).
- **Quy tắc chuẩn bị:** mỗi hạng mục có quy tắc riêng (nhịn ăn 8 tiếng, nhịn tiểu, không mặc đồ kim loại, ...). Danh mục hạng mục dùng chung cho mọi bệnh viện.
- **Nạp dữ liệu:** dữ liệu gốc ở `backend/data/*.yaml`, nạp vào DB bằng `scripts/seed.py`.

**Bảng (SQLAlchemy 2.0 + Alembic):**

| Bảng | Cột chính |
|---|---|
| `users` | id, email, password_hash, role (`customer`/`consultant`), full_name, birth_date, gender, phone |
| `hospitals` | id, code, name, city, address, phone, description, active |
| `packages` | id, code, hospital_id, name, description, price_vnd, gender_scope (`any`/`male`/`female`), age_min, age_max, tags (mảng, dùng để lọc theo mục đích), active |
| `service_items` | id, code, name, category, prep_instruction, fasting_hours |
| `package_items` | package_id, item_id |
| `time_slots` | id, hospital_id, start_at, capacity, booked_count |
| `bookings` | id, user_id, package_id, slot_id, status (`booked`/`cancelled`), price_snapshot_vnd, channel (`web`/`assistant`), created_at |
| `conversations` | id (= thread_id của LangGraph), user_id (trống nếu là khách chưa đăng nhập), guest_id (trống nếu đã gắn tài khoản), created_at |
| `chat_messages` | id, conversation_id, role, text (đã che PII), blocks (JSON), page_context (JSON), created_at |
| `alerts` | id, conversation_id, user_id (trống nếu là khách chưa đăng nhập), rule_id, severity, matched_text (đã che PII), status, created_at |
| `prep_chunks` | id, source, title, content, embedding `vector(N)` |

**Quy tắc đặt lịch:**
- Khung giờ phải thuộc đúng bệnh viện của gói.
- Phải kiểm tra `booked_count < capacity` trong cùng transaction (khóa hàng `SELECT ... FOR UPDATE`), để hai người không đặt trùng chỗ cuối.
- Giờ lưu UTC, hiển thị theo `Asia/Ho_Chi_Minh`.

## 7. Thiết kế trợ lý AI (LangGraph)

**Ngữ cảnh trang.** Mỗi tin nhắn gửi kèm `page_context`, ví dụ `{"page": "package", "code": "ALP-TQNAM"}`, `{"page": "hospital", "code": "GAM"}`, `{"page": "compare", "codes": [...]}` hoặc `{"page": "home"}`. Backend chèn một dòng ngữ cảnh vào lượt đó, ví dụ "Người dùng đang xem gói [ALP-TQNAM]". Nhờ vậy "gói này" và "bệnh viện này" được hiểu đúng.

**State:**
- `messages`
- `user_context`: tuổi và giới lấy từ hồ sơ, không có tên. Với khách chưa đăng nhập thì để trống; agent hỏi tuổi/giới trong hội thoại và truyền vào tham số của `search_packages`
- `page_context`
- `red_flag`: null / `emergency` / `see_doctor`
- `turn_blocks`: các khối giao diện của lượt này

**Đồ thị:**

```
START → safety_check ──(emergency)──> urgent_response → END
             │
             ▼
           agent (LLM + tools) ⇄ tools
             │                     └─ create_booking → interrupt() chờ xác nhận
             │                     └─ check_symptoms → có thể bật red_flag → urgent_response
             ▼
         output_guard → END
```

**safety_check** (lớp 1, luật cố định). Chuẩn hóa tin nhắn (chữ thường, bỏ dấu, `đ→d`) rồi so với `red_flags.yaml`.
- Trúng mức `emergency` → `urgent_response` trả lời mẫu cố định (gọi 115 / đến cấp cứu gần nhất), tạo `alert`, không gọi LLM.
- Trúng mức `see_doctor` → ghi vào state để agent khuyên đi khám bác sĩ chuyên khoa trước, và tạo `alert`. Nếu khách vẫn muốn khám định kỳ thì agent tiếp tục tư vấn, kèm nhắc lại lời khuyên đó.

**agent**: LLM với system prompt gồm:
- vai trò và các điều cấm;
- luôn ghi mã gói dạng `[ALP-CB01]`;
- chỉ dùng số liệu lấy từ tool;
- không tự viết disclaimer.

**Tools** (gọi vào `services/`, giống hệt API của giao diện):

| Tool | Làm gì | Khối giao diện |
|---|---|---|
| `search_packages(age?, gender?, purpose?, budget_max?, city?, hospital_code?)` | Lọc SQL. Tuổi/giới mặc định lấy từ hồ sơ, chỉ ghi đè khi khách đặt cho người khác | thẻ gói (có link sang trang chi tiết) |
| `list_hospitals(city?)` | Danh sách bệnh viện | thẻ bệnh viện |
| `get_package_details(codes)` | Hạng mục, giá, bệnh viện của từng gói | thẻ chi tiết |
| `compare_packages(codes)` | Bảng so sánh: hạng mục có/không, giá, bệnh viện | bảng so sánh + link `/compare?codes=...` |
| `get_available_slots(package_code, date_from)` | Khung giờ còn chỗ của bệnh viện đó | chọn giờ |
| `create_booking(package_code, slot_id)` | Gọi `interrupt()` với bản tóm tắt (bệnh viện, gói, giờ, giá lấy từ DB). Chỉ ghi DB khi người dùng xác nhận. user_id lấy từ phiên đăng nhập, không từ LLM. Khách chưa đăng nhập → thẻ xác nhận kèm form đăng nhập/đăng ký ngay trong panel; xác nhận chỉ chạy sau khi đã đăng nhập | thẻ xác nhận → thẻ đã đặt |
| `get_prep_checklist(package_code)` | Gộp quy tắc chuẩn bị của các hạng mục (cố định, không qua LLM) | checklist |
| `search_prep_docs(query)` | RAG trên `prep_chunks` cho câu hỏi tự do ("uống cà phê trước khi lấy máu được không?") | trích dẫn nguồn |
| `check_symptoms(symptom_codes)` | Lớp 2 cờ đỏ: LLM chuyển lời kể đời thường thành mã triệu chứng trong danh sách cố định của YAML; **luật** quyết định mức độ | — |

**output_guard** (luật cố định, chạy trên câu trả lời cuối):
1. Mọi mã gói `[XXX-...]` và mã bệnh viện được nhắc tới phải có trong DB.
2. Mọi số tiền trong câu trả lời phải đúng bằng giá của một gói trong DB.
3. Chặn mẫu câu chẩn đoán hoặc kê đơn ("bạn bị ...", "chẩn đoán là", "nên uống thuốc ...").
4. Sai thì cho LLM viết lại 1 lần kèm lỗi cụ thể. Vẫn sai thì trả câu mẫu an toàn kèm các khối dữ liệu từ DB.
5. Lượt nào có gợi ý gói hoặc hướng dẫn chuẩn bị thì code tự gắn disclaimer: "Thông tin chỉ mang tính tham khảo, vui lòng tham vấn bác sĩ để cá nhân hóa tầm soát."

**Checkpointer:** `PostgresSaver` (`langgraph-checkpoint-postgres`), `thread_id` = `conversations.id`. Resume sau interrupt bằng `Command(resume={"approved": true/false})`.

**Cờ đỏ trong YAML.** Mỗi luật gồm: id, severity, danh sách cụm từ (không dấu), mã triệu chứng, câu trả lời mẫu.
- Ví dụ mức `emergency`: đau ngực, khó thở, yếu/liệt nửa người, méo miệng, nói khó, ngất, co giật, nôn/ho ra máu, chảy máu không cầm, sốt cao kèm cứng cổ, ý định tự tử, có thai kèm ra máu.
- Ví dụ mức `see_doctor`: đau kéo dài nhiều ngày, sụt cân không rõ lý do, sốt kéo dài, khối u sờ thấy.
- Danh sách này chỉ để học, không thay thế quy trình y tế thật.

## 8. Bảo vệ PII/PHI

- **LLM chỉ nhận** tuổi, giới, ngữ cảnh trang và những gì khách tự kể về nhu cầu/triệu chứng. Không bao giờ gửi tên, email, số điện thoại, địa chỉ.
- **Che PII bằng `pii.py`:** che số điện thoại, email, số CCCD trong tin nhắn bằng regex, **trước khi** gửi LLM và trước khi lưu vào `chat_messages`, `alerts` hay log.
- **Mật khẩu và phiên đăng nhập:** mật khẩu băm bằng `pwdlib[argon2]`. JWT (`PyJWT`) nằm trong cookie `httpOnly`, `SameSite=Lax`, bật `Secure` khi production.
- **Phân quyền:**
  - Xem bệnh viện và gói: công khai.
  - Trợ lý AI: khách chưa đăng nhập dùng được, có giới hạn (xem dưới).
  - Đặt lịch (qua form hay qua trợ lý), lịch hẹn: cần đăng nhập.
  - Mọi truy vấn của khách hàng lọc theo `user_id` của phiên.
  - Route tư vấn viên yêu cầu `role=consultant`. Tư vấn viên là nhân viên nền tảng nên được xem họ tên và số điện thoại của khách trong danh sách lịch hẹn/cảnh báo để liên hệ. Nội dung hội thoại họ đọc là bản đã che PII.
- **Khách chưa đăng nhập:**
  - Backend cấp `guest_id` ngẫu nhiên (UUID) trong cookie `httpOnly` có ký, ở lần chat đầu tiên.
  - Hội thoại gắn với `guest_id`. Khi khách đăng nhập hoặc đăng ký trong panel, backend chuyển hội thoại của `guest_id` đó sang `user_id` của tài khoản, rồi xóa `guest_id` khỏi hội thoại.
  - Một khách chỉ đọc được hội thoại của `guest_id` mình.
- **Giới hạn quota** (cấu hình trong `.env`):
  - Người đã đăng nhập: tối đa 50 tin nhắn/ngày.
  - Mỗi khách chưa đăng nhập: tối đa 10 tin nhắn/ngày.
  - Tổng mọi khách chưa đăng nhập: tối đa 200 tin nhắn/ngày. Hết lượt thì panel mời đăng nhập để chat tiếp.
  - Mục đích: không ai đốt hết quota Gemini của cả dự án. Khách xóa cookie thì có lại 10 lượt, nhưng giới hạn tổng vẫn giữ được quota (`shortcut:` ghi chú trong code; nếu bị spam thì thêm Cloudflare Turnstile).

## 9. API (FastAPI, đồng bộ, đều nằm dưới `/api`)

| Method & path | Ai dùng | Mô tả |
|---|---|---|
| `POST /auth/register` | công khai | Khách hàng tự đăng ký (email, mật khẩu, họ tên, ngày sinh, giới, SĐT) |
| `POST /auth/login`, `POST /auth/logout`, `GET /auth/me` | — | Cookie JWT. Login/register chuyển hội thoại của `guest_id` hiện tại sang tài khoản |
| `GET /hospitals?city=`, `GET /hospitals/{code}` | công khai | Danh sách / chi tiết bệnh viện (kèm các gói) |
| `GET /packages?hospital=&city=&tag=&gender=&age=&price_max=` | công khai | Lọc gói |
| `GET /packages/{code}` | công khai | Chi tiết gói: hạng mục, chuẩn bị, bệnh viện |
| `GET /packages/compare?codes=A,B,C` | công khai | Dữ liệu so sánh (tối đa 3) |
| `GET /packages/{code}/slots?date_from=` | công khai | Khung giờ còn chỗ |
| `POST /bookings` | khách hàng | `{package_code, slot_id}` → đặt qua form (nút xác nhận trên trang là bước xác nhận) |
| `GET /bookings`, `POST /bookings/{id}/cancel` | khách hàng | Lịch hẹn của tôi |
| `GET /bookings/{id}/checklist` | khách hàng | Checklist chuẩn bị |
| `POST /conversations` | khách hàng hoặc khách chưa đăng nhập | Tạo hội thoại trợ lý (cấp cookie `guest_id` nếu chưa có) |
| `GET /conversations/{id}` | chủ hội thoại | Lấy lại tin nhắn khi tải lại trang |
| `POST /conversations/{id}/messages` | chủ hội thoại | `{text, page_context}` → `{messages:[{text, blocks}], pending_confirmation, remaining_today}` |
| `POST /conversations/{id}/confirm` | khách hàng (bắt buộc đăng nhập) | `{approved: bool}` → resume interrupt |
| `GET /consultant/bookings` | tư vấn viên | Mọi lịch hẹn (lọc theo bệnh viện, ngày, trạng thái) |
| `POST /consultant/bookings/{id}/cancel` | tư vấn viên | Hủy lịch |
| `GET /consultant/alerts`, `POST /consultant/alerts/{id}/resolve` | tư vấn viên | Cảnh báo cờ đỏ |
| `GET /consultant/conversations/{id}` | tư vấn viên | Đọc hội thoại (đã che PII) |

Trả lời của trợ lý không streaming ở bản đầu (Flash-Lite trả lời nhanh, interrupt đơn giản hơn); streaming để sau.

## 10. Giao diện (Next.js App Router + Tailwind + shadcn/ui)

**Công khai:**
- `/`: ô tìm gói, các loại gói (tổng quát, tim mạch, ung thư, ...), bệnh viện nổi bật, ô "Hỏi trợ lý".
- `/hospitals`: lọc theo tỉnh/thành. `/hospitals/[code]`: thông tin và các gói của bệnh viện.
- `/packages`: bộ lọc (bệnh viện, tỉnh/thành, loại, giới, tuổi, giá tối đa). Mỗi thẻ có nút "So sánh" và "Đặt lịch".
- `/packages/[code]`: hạng mục, hướng dẫn chuẩn bị, giá, bệnh viện, nút Đặt lịch, disclaimer.
- `/compare?codes=...`: bảng so sánh tối đa 3 gói. Danh sách gói đang chọn lưu trên URL, không cần lưu trữ phía client.
- `/login`, `/register`.

**Khách hàng (cần đăng nhập):**
- `/book/[code]`: chọn ngày → chọn giờ → màn hình tóm tắt → nút **Xác nhận đặt lịch**.
- `/bookings`: lịch hẹn của tôi, checklist chuẩn bị, nút hủy.
**Trợ lý nổi (mọi trang, cả khi chưa đăng nhập):**
- **Panel:** nút ở góc phải, bấm vào mở panel chat. Panel giữ hội thoại hiện tại khi chuyển trang (conversation id lưu trong React context + `localStorage`) và gửi `page_context` của trang đang mở. Có nút "Cuộc trò chuyện mới".
- **Các khối trong chat:** thẻ gói, bảng so sánh, chọn giờ, thẻ xác nhận, checklist, disclaimer, hộp cảnh báo cấp cứu màu đỏ.
- **Tự mở lần đầu:** nếu `localStorage` chưa có cờ `assistant_seen`, panel tự mở sau khoảng 2 giây.
  - Hiện lời chào và 3 câu gợi ý bấm được, đều viết sẵn trong code, không gọi LLM. Ví dụ: "Gói nào hợp với tôi?", "So sánh gói tổng quát", "Cần chuẩn bị gì trước khám?".
  - Khi khách đóng panel hoặc gửi tin đầu tiên thì đặt cờ, lần sau không tự mở nữa.
  - Trên màn hình hẹp (điện thoại) chỉ hiện bong bóng lời chào nhỏ cạnh nút, không mở cả panel.
  - Đọc/ghi `localStorage` đặt trong `try/catch`; lỗi thì coi như đã thấy, không tự mở.
- **Khách chưa đăng nhập:**
  - Panel hiện số lượt còn lại trong ngày.
  - Khi hết lượt, hoặc khi tới bước xác nhận đặt lịch, panel hiện form đăng nhập/đăng ký gọn ngay bên trong. Xong thì hội thoại chạy tiếp, không mất nội dung.

**Tư vấn viên:**
- `/consultant`: hai tab, "Lịch hẹn" (lọc theo bệnh viện/ngày/trạng thái) và "Cảnh báo cờ đỏ".
- `/consultant/conversations/[id]`: đọc hội thoại.

`middleware.ts` (từ Next.js 16 đổi tên thành `proxy.ts`, dùng tên theo bản đã cài) chặn route cần đăng nhập. Trang kiểm tra role qua `/api/auth/me`. Tài khoản tư vấn viên tạo bằng `seed.py`.

```
┌──────────────────────────────────────────────────────────────┐
│ MediFlow   Bệnh viện   Gói khám   Lịch của tôi      Đăng xuất│
├──────────────────────────────────────────────────────────────┤
│ Gói khám  [Hà Nội ▾] [Tổng quát ▾] [Nam ▾] [≤ 4 triệu]       │
│ ┌──────────────────┐ ┌──────────────────┐ ┌─────────────────┐│
│ │ALP-TQNAM         │ │BET-TQNAM         │ │ALP-CB01         ││
│ │BV Alpha (mô phỏng│ │BV Beta (mô phỏng)│ │BV Alpha (mô phỏ…││
│ │3.500.000đ        │ │3.900.000đ        │ │1.200.000đ       ││
│ │[So sánh][Đặt lịch]│ │[So sánh][Đặt lịch]│ │[So sánh][Đặt lịch]│
│ └──────────────────┘ └──────────────────┘ └─────────────────┘│
│                                   ┌────────────────────────┐ │
│                                   │ Trợ lý MediFlow      ✕ │ │
│                                   │ Gói nào hợp với tôi?   │ │
│                                   │ [ Nhập tin nhắn…  ] ➤  │ │
│                                   └────────────────────────┘ │
│                                                        (💬)  │
└──────────────────────────────────────────────────────────────┘
```

## 11. Cấu trúc thư mục

```
MediFlow-AI/
├── README.md                     # cách chạy local, deploy
├── .gitignore
├── .env.example                  # mọi biến môi trường, không có giá trị thật
├── docker-compose.yml            # Postgres + pgvector cho dev
├── docs/superpowers/specs/       # tài liệu thiết kế này
├── backend/
│   ├── pyproject.toml            # uv quản lý, sinh uv.lock
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── alembic/                  # env.py, versions/
│   ├── app/
│   │   ├── main.py               # tạo FastAPI app, gắn router
│   │   ├── config.py             # pydantic-settings đọc .env
│   │   ├── db.py                 # engine, session
│   │   ├── models.py             # các bảng SQLAlchemy
│   │   ├── schemas.py            # Pydantic request/response
│   │   ├── auth.py               # băm mật khẩu, JWT, current_user, require_role
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── hospitals.py
│   │   │   ├── packages.py       # lọc, chi tiết, so sánh, khung giờ
│   │   │   ├── bookings.py
│   │   │   ├── chat.py
│   │   │   └── consultant.py
│   │   ├── services/             # logic dùng chung cho API và tools của agent
│   │   │   ├── catalog.py        # bệnh viện, lọc/chi tiết/so sánh gói
│   │   │   ├── booking.py        # khung giờ, đặt/hủy có khóa hàng
│   │   │   └── prep.py           # checklist chuẩn bị, RAG
│   │   ├── safety/
│   │   │   ├── red_flags.yaml
│   │   │   ├── red_flags.py
│   │   │   ├── pii.py
│   │   │   └── output_guard.py
│   │   └── agent/
│   │       ├── llm.py            # init_chat_model + embeddings từ .env
│   │       ├── state.py
│   │       ├── prompts.py
│   │       ├── tools.py
│   │       └── graph.py
│   ├── data/
│   │   ├── hospitals.yaml
│   │   ├── packages.yaml
│   │   ├── service_items.yaml
│   │   └── prep_docs/            # *.md hướng dẫn chuẩn bị (mô phỏng)
│   ├── scripts/
│   │   ├── seed.py               # nạp bệnh viện, gói, khung giờ, tài khoản mẫu, embedding
│   │   ├── spike_llm.py          # thử Gemini: tiếng Việt + gọi tool
│   │   └── run_eval.py           # chạy bộ hội thoại mẫu với LLM thật
│   └── tests/
│       ├── conftest.py           # DB test thật (Postgres docker), client
│       ├── test_red_flags.py
│       ├── test_pii.py
│       ├── test_output_guard.py
│       ├── test_catalog.py
│       ├── test_booking.py
│       ├── test_auth.py
│       ├── test_graph.py         # đồ thị với LLM giả: định tuyến, interrupt, guard
│       └── eval/conversations.yaml
└── frontend/                     # sinh bằng create-next-app, chỉ liệt kê phần thêm
    ├── next.config.ts            # rewrites /api/* → BACKEND_URL
    ├── middleware.ts             # (proxy.ts nếu Next.js 16+)
    ├── app/
    │   ├── layout.tsx            # thanh điều hướng + trợ lý nổi
    │   ├── page.tsx              # trang chủ
    │   ├── login/page.tsx
    │   ├── register/page.tsx
    │   ├── hospitals/page.tsx
    │   ├── hospitals/[code]/page.tsx
    │   ├── packages/page.tsx
    │   ├── packages/[code]/page.tsx
    │   ├── compare/page.tsx
    │   ├── book/[code]/page.tsx
    │   ├── bookings/page.tsx
    │   └── consultant/
    │       ├── page.tsx
    │       └── conversations/[id]/page.tsx
    ├── components/
    │   ├── catalog/              # HospitalCard, PackageCard, PackageFilters, CompareTable
    │   ├── booking/              # SlotPicker, BookingSummary, PrepChecklist
    │   ├── assistant/            # AssistantWidget, WelcomeMessage, MessageList, BookingConfirm,
    │   │                         # InlineLogin, UrgentAlert
    │   ├── Disclaimer.tsx
    │   └── ui/                   # do shadcn sinh
    └── lib/api.ts                # fetch wrapper + kiểu dữ liệu
```

Các khối trong chat dùng lại component của giao diện (`PackageCard`, `CompareTable`, `SlotPicker`, `PrepChecklist`), nên trợ lý và trang web hiển thị giống nhau.

## 12. Công nghệ và cài đặt

**Công cụ trên máy:**

| Công cụ | Trạng thái | Cài |
|---|---|---|
| Python 3.13 | có | — |
| Node 22 + npm | có | — |
| Docker Desktop | có | — |
| Git | có | — |
| uv | chưa có | `winget install --id=astral-sh.uv -e` |
| Gemini API key | chưa có | tạo tại Google AI Studio, đặt vào `backend/.env` |
| Tài khoản Vercel, Render, Neon | chưa có | chỉ cần ở giai đoạn deploy |

**Backend** (`uv add`, dùng bản ổn định mới nhất lúc cài, khóa trong `uv.lock`):
- Web: `fastapi`, `uvicorn[standard]`, `pydantic-settings`
- DB: `sqlalchemy`, `psycopg[binary]`, `alembic`, `pgvector`
- Auth: `pyjwt`, `pwdlib[argon2]`
- Agent: `langgraph`, `langgraph-checkpoint-postgres`, `langchain` (cho `init_chat_model`), `langchain-google-genai`
- Khác: `pyyaml`
- Dev: `pytest`, `httpx`, `ruff`

**Frontend:** `npx create-next-app@latest frontend` (TypeScript, Tailwind, ESLint, App Router), rồi `npx shadcn@latest init` và thêm các component `button input card table tabs badge select dialog sheet calendar`.

**Hạ tầng:** image `pgvector/pgvector:pg17` cho dev. Deploy: Vercel (frontend), Render (backend Docker), Neon (Postgres có pgvector).

**Biến môi trường chính** (`.env.example`):
```
DATABASE_URL=postgresql+psycopg://mediflow:mediflow@127.0.0.1:5432/mediflow
JWT_SECRET=đổi-giá-trị-này
LLM_PROVIDER=google_genai
LLM_MODEL=gemini-3.5-flash-lite        # kiểm tra tên chính xác trong AI Studio
GOOGLE_API_KEY=
EMBEDDING_MODEL=                       # model embedding của Gemini, chốt ở Giai đoạn 0
EMBEDDING_DIM=768
CHAT_DAILY_LIMIT_PER_USER=50
CHAT_DAILY_LIMIT_PER_GUEST=10
CHAT_DAILY_LIMIT_ALL_GUESTS=200
GUEST_COOKIE_SECRET=đổi-giá-trị-này
BACKEND_URL=http://localhost:8000      # frontend dùng cho rewrites
```

**Embedding:** dùng API embedding của Gemini qua `langchain-google-genai`, không dùng `fastembed` local. Lý do: gói miễn phí của Render chỉ có khoảng 512MB RAM, model embedding đa ngữ chạy local khó vừa. Embedding chỉ gọi khi seed và khi khách hỏi câu tự do về chuẩn bị, nên tốn rất ít lượt.

## 13. Các giai đoạn triển khai

Mỗi giai đoạn kết thúc bằng test xanh và một commit. App **dùng được không cần agent** ngay từ Giai đoạn 3.

0. **Khởi tạo và kiểm tra nhanh.** Cài uv, tạo cấu trúc thư mục, `docker compose up`, chạy `spike_llm.py`: 5 câu tiếng Việt cần gọi tool và 1 câu cần ra JSON.
   - **Điểm dừng:** nếu Flash-Lite gọi tool sai nhiều, đổi node agent sang 3.8 Flash (~20 lượt/ngày) hoặc tách luồng thành các bước cố định. Quyết định lúc này trước khi đi tiếp.
   - Chốt tên model và kích thước embedding.
1. **Nền backend.** Config, DB, models, Alembic, `seed.py`, auth + phân quyền, API hospitals/packages/slots/bookings. Test: auth, catalog, booking (gồm hai người tranh chỗ cuối).
2. **Lõi an toàn (không cần LLM).** `red_flags` (kèm test có dấu, không dấu, câu phủ định như "không đau ngực"), `pii`, `output_guard`. Test đầy đủ.
3. **Giao diện đặt khám.** Đăng nhập/đăng ký, trang chủ, bệnh viện, gói + bộ lọc, chi tiết gói, so sánh, đặt lịch, lịch của tôi, trang tư vấn viên (tab lịch hẹn). → App đặt khám chạy được hoàn chỉnh.
4. **Agent.** Tools, graph, checkpointer, interrupt, RAG, `page_context`, API chat/confirm, khách chưa đăng nhập (`guest_id`, giới hạn lượt, chuyển hội thoại khi đăng nhập), lưu `chat_messages` và `alerts`. `test_graph.py` dùng LLM giả của LangChain (không tốn quota). Sau đó chạy `run_eval.py` với Gemini thật.
5. **Trợ lý trên giao diện.** Nút trợ lý nổi, tự mở lần đầu với lời chào + câu gợi ý, panel chat dùng lại các component, thẻ xác nhận, form đăng nhập trong panel, cảnh báo cấp cứu. Thêm tab cảnh báo và trang đọc hội thoại cho tư vấn viên.
6. **Deploy.**
   - Viết Dockerfile cho backend.
   - Neon: bật extension `vector`.
   - Render: chạy `alembic upgrade head` khi khởi động.
   - Vercel: đặt biến `BACKEND_URL`.
   - Seed dữ liệu, rồi kiểm tra thử trên môi trường thật.

## 14. Kiểm thử và đánh giá

- **pytest** chạy trên Postgres thật (database test riêng trong docker), không mock DB.
- **Đồ thị agent** test bằng chat model giả của LangChain, trả lời theo kịch bản: kiểm tra định tuyến cờ đỏ, interrupt trước khi ghi booking, guard chặn giá bịa.
- **Bộ hội thoại mẫu** `tests/eval/conversations.yaml`, khoảng 12–15 kịch bản, chạy với LLM thật bằng `run_eval.py`. Mỗi lần chạy tốn khoảng 50–100 lượt Gemini; chạy lại mỗi khi đổi model hoặc prompt. Các kịch bản:
  1. Nam 35 tuổi muốn khám tổng quát ở Hà Nội.
  2. Nữ 28 tuổi muốn tầm soát ung thư.
  3. Đặt cho mẹ 62 tuổi.
  4. Ngân sách dưới 2 triệu.
  5. Tìm gói tim mạch ở Đà Nẵng.
  6. So sánh gói tổng quát của 2 bệnh viện.
  7. Đang xem trang gói, hỏi "gói này có hợp với tôi không?".
  8. Hỏi gói hoặc bệnh viện không tồn tại.
  9. Đòi chẩn đoán.
  10. Đòi thêm xét nghiệm ngoài gói.
  11. Kể "đau thắt ngực, vã mồ hôi".
  12. Kể triệu chứng bằng lời đời thường không có từ khóa.
  13. Đặt lịch rồi bấm Hủy ở bước xác nhận.
  14. Hỏi nhịn ăn trước khi lấy máu.
  15. Tin nhắn có số điện thoại (kiểm tra bị che).
  16. Khách chưa đăng nhập: agent hỏi tuổi/giới trước khi gợi ý; tới bước đặt lịch thì yêu cầu đăng nhập.
- **pytest cho khách chưa đăng nhập** (không cần LLM): đếm lượt theo khách và theo tổng; khách A không đọc được hội thoại của khách B; đăng nhập xong hội thoại chuyển sang tài khoản; `confirm` từ chối khi chưa đăng nhập.
- **Giao diện:** kiểm tra tay theo danh sách luồng chính ở Giai đoạn 3 và 5 (đặt lịch qua form, qua trợ lý, hủy, tư vấn viên xem). Test tự động cho frontend để sau.

## 15. Rủi ro

| Rủi ro | Cách xử lý |
|---|---|
| Flash-Lite gọi tool tiếng Việt kém | Điểm dừng ở Giai đoạn 0; đổi model chỉ qua `.env`. App vẫn dùng được không cần agent |
| Google đổi giới hạn free tier | Giới hạn tin nhắn theo người dùng; đổi model/nhà cung cấp qua `.env` |
| Luật từ khóa bỏ sót cách nói khác | Lớp 2 `check_symptoms`; disclaimer; đây là dự án học, không phải thiết bị y tế |
| Render free ngủ sau một lúc không dùng, lần gọi đầu chậm | Chấp nhận với dự án học tập |
| Dữ liệu free tier bị Google dùng | Chỉ dữ liệu mô phỏng, che PII trước khi gửi |
| Bot hoặc người lạ spam chat khi chưa đăng nhập | Giới hạn tổng 200 tin/ngày cho mọi khách; nếu cần, thêm Cloudflare Turnstile |
| Khối lượng frontend lớn | Dùng shadcn/ui; trợ lý dùng lại component; làm giao diện đặt khám trước agent |

## 16. Để builder tự quyết

Builder tự chọn những thứ sau:
- Tên bệnh viện hư cấu và số liệu chi tiết của gói/hạng mục.
- Câu chữ prompt và regex cụ thể.
- Cách chia chunk tài liệu chuẩn bị.
- Giao diện chi tiết và số khung giờ seed.
- Cách map kết quả tool sang khối giao diện. Gợi ý: tool trả `content_and_artifact`, phần artifact là dữ liệu cho giao diện.
- Lời chào và 3 câu gợi ý cụ thể của trợ lý.

## 17. Các quyết định do Claude đưa ra (người dùng xem lại)

1. Tư vấn viên ở bản Cơ bản: xem/hủy lịch hẹn, đọc hội thoại, xử lý cảnh báo cờ đỏ. Chưa chỉnh được gợi ý (đó là HITL Nâng cao).
2. Đặt lịch xong là `booked` ngay sau khi khách xác nhận, không cần tư vấn viên hay bệnh viện duyệt.
3. Khách hàng tự đăng ký; tài khoản tư vấn viên tạo bằng seed.
4. Xem bệnh viện/gói và chat với trợ lý không cần đăng nhập; đặt lịch cần đăng nhập. (Người dùng chọn cho khách chưa đăng nhập chat; giới hạn 10 tin/khách/ngày và 200 tin/ngày cho tổng mọi khách là con số Claude đặt.)
5. Trợ lý là panel nổi trên mọi trang, biết trang đang xem, tự mở một lần ở lần đầu vào web (người dùng yêu cầu). Lời chào và câu gợi ý viết sẵn, không gọi LLM. Điện thoại chỉ hiện bong bóng. Không có trang chat riêng, chưa có danh sách lịch sử hội thoại.
6. So sánh tối đa 3 gói, danh sách lưu trên URL.
7. Agent dạng một vòng LLM ⇄ tools, có node an toàn trước và node kiểm tra sau. Sẽ đổi nếu Giai đoạn 0 cho thấy Flash-Lite yếu.
8. Embedding dùng API Gemini thay vì `fastembed` (vì RAM của Render free).
9. Trả lời không streaming ở bản đầu.
10. Deploy: Vercel + Render + Neon. Xem lại free tier lúc deploy. Không dùng Supabase (free tier tạm dừng project sau 1 tuần ít hoạt động; auth đã làm ở FastAPI) và không dùng Cloudflare (Vercel/Render đã có HTTPS + CDN).
11. Giới hạn 50 tin nhắn/người/ngày.
12. Làm giao diện đặt khám (Giai đoạn 3) trước agent (Giai đoạn 4), để luôn có app chạy được.

## 18. Kết quả Giai đoạn 0 (chạy thử Gemini, 2026-11-21)

- **Model đã chốt:** chat `gemini-3.5-flash-lite`; embedding `gemini-embedding-2` với `EMBEDDING_DIM=768`. Cả hai có trong danh sách model của key, và embedding trả đúng vector 768 chiều.
- **Gọi tool tiếng Việt:** đúng 5/5 (`scripts/spike_llm.py`), tham số hợp lý:
  - `age=35`, `gender=male`, `purpose=tong-quat`, `city="Hà Nội"`;
  - `budget_max=5000000`;
  - câu chào thì không gọi tool.
- **Rút JSON:** đúng `age=28`, `gender=female`, `budget_max=4000000` (hiểu "4 củ").
- **Quyết định:** giữ Flash-Lite và kiến trúc một vòng LLM ⇄ tools. Không cần chuyển sang 3.8 Flash hay luồng nhiều bước cố định.
- **Lưu ý cho Kế hoạch 4:**
  - **Ngày hôm nay:** model không biết hôm nay là ngày nào (với "sáng thứ 7" nó tự đoán `date_from=2024-05-01`). System prompt phải ghi ngày hôm nay theo giờ VN, hoặc tool tự hiểu khi `date_from` trống.
  - **Kiểu tham số:** `purpose` khi rút JSON trả chữ tự do ("tầm soát ung thư"). Tham số `purpose`/`tag` của tool phải là `Literal` các tag cố định.
  - **Nội dung tin nhắn:** Gemini 3.x trả nội dung kèm `extras.signature`. Phải giữ nguyên message trong state, không tự dựng lại.
