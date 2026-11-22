# Graph Report - MediFlow-AI  (2026-11-23)

## Corpus Check
- 73 files · ~63,302 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1286 nodes · 3405 edges · 74 communities (60 shown, 14 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 395 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Spec và từ khóa an toàn
- Định dạng giờ Việt Nam
- Khởi động backend, Docker
- Layout trang app, shadcn
- Hạ tầng test Postgres
- Schema đăng ký, đăng nhập
- Ngữ pháp luật cờ đỏ
- Guard đầu ra: số tiền
- Test guard đầu ra
- API đăng nhập, đăng xuất
- Các page.tsx của app
- Trang lịch của tôi
- Trang bệnh viện, đăng ký
- API chat (kế hoạch 4)
- Che PII
- Giới hạn ngày, khung giờ
- Đăng nhập phía frontend
- Cấu hình shadcn/ui
- Router API backend
- Test phát hiện cờ đỏ
- API đặt lịch của khách
- Service danh mục gói
- Kế hoạch 5: khối chat
- View đặt lịch và gói
- Alembic và cấu hình
- Seed dữ liệu mô phỏng
- Chạy thử Gemini
- Xác thực cookie JWT
- Đặt/hủy lịch có khóa
- Chọn khung giờ
- Cấu hình TypeScript
- API tư vấn viên
- Đồ thị agent LangGraph
- Dữ liệu test cờ đỏ
- CLAUDE.md và kế hoạch
- API bệnh viện
- Service khung giờ
- Trang chủ taste-skill
- State agent (kế hoạch 4)
- Tools của agent
- Models dữ liệu
- Test đặt lịch
- Form đăng nhập
- API chi tiết, so sánh gói
- Test danh mục gói
- Kế hoạch 5: component
- Booking và giá chụp
- Node agent và guard
- lib/assistant (kế hoạch 5)
- Enum và PII khi gửi LLM
- So sánh gói
- AssistantProvider (kế hoạch 5)
- Migration khởi tạo
- System prompt trợ lý
- docker-compose
- Settings và .env
- Kế hoạch 3: hàm định dạng
- RAG tài liệu chuẩn bị
- Chuẩn hóa chữ Việt
- CLAUDE.md: chạy và test
- Proxy chặn trang
- README frontend
- CompareBar
- Icon file.svg
- Icon globe.svg
- Logo Next.js
- Logo Vercel
- Icon window.svg

## God Nodes (most connected - your core abstractions)
1. `PageSkeleton()` - 37 edges
2. `detect()` - 32 edges
3. `next` - 31 edges
4. `check()` - 30 edges
5. `create_booking()` - 29 edges
6. `Button()` - 29 edges
7. `react` - 29 edges
8. `Task 6: Khung giờ, đặt/hủy lịch, checklist chuẩn bị, trang tư vấn viên` - 28 edges
9. `ConsultantView()` - 25 edges
10. `normalize_vi()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Tool create_booking` --semantically_similar_to--> `book()`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-11-21-plan-4-agent.md → backend/app/api/bookings.py
- `proxy.ts` --semantically_similar_to--> `require_role()`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-11-21-plan-3-giao-dien-dat-kham.md → backend/app/auth.py
- `Tool search_packages` --semantically_similar_to--> `search_packages()`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-11-21-plan-4-agent.md → backend/app/api/packages.py
- `Tool compare_packages` --semantically_similar_to--> `compare_packages()`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-11-21-plan-4-agent.md → backend/app/api/packages.py
- `Khung giờ hết chỗ (409) giữa lúc xem và lúc xác nhận` --references--> `book()`  [INFERRED]
  docs/superpowers/plans/2026-11-21-plan-3-giao-dien-dat-kham.md → backend/app/api/bookings.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Đặt lịch qua trợ lý có thẻ xác nhận và đăng nhập trong chat** — docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_bookingconfirm, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_inlinelogin, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_loginform, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_registerform, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_pendingbooking, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_assistantprovider [EXTRACTED 1.00]
- **5 điểm Review Focus của Kế hoạch 1** — docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_rf1_loc_tinh_thanh_khong_dau, docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_rf2_date_from_gio_viet_nam, docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_rf3_chong_dat_trung, docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_rf4_khong_huy_lich_da_qua, docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_rf5_email_khong_phan_biet_hoa_thuong [EXTRACTED 1.00]
- **Fixture dùng chung chuyển từ test_booking.py sang conftest.py** — docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_chuyen_fixture_sang_conftest [EXTRACTED 1.00]
- **Các trang App Router theo mẫu Suspense + *View** — docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_mau_trang_suspense_view, frontend_app_page [EXTRACTED 1.00]
- **Luồng đặt lịch có xác nhận: interrupt → /confirm → resume** — docs_superpowers_plans_2026_11_21_plan_4_agent_tool_create_booking, docs_superpowers_plans_2026_11_21_plan_4_agent_bước_dừng_chờ_xác_nhận_đặt_lịch, docs_superpowers_plans_2026_11_21_plan_4_agent_services_chat_send_message, docs_superpowers_plans_2026_11_21_plan_4_agent_services_chat_confirm, docs_superpowers_plans_2026_11_21_plan_4_agent_post_api_conversations_id_confirm, backend_app_services_booking_create_booking, docs_superpowers_plans_2026_11_21_plan_4_agent_schemas_turnout [EXTRACTED 1.00]
- **Khách chưa đăng nhập: cookie khách → chuyển hội thoại khi đăng nhập** — docs_superpowers_plans_2026_11_21_plan_4_agent_guest_ensure_guest, docs_superpowers_plans_2026_11_21_plan_4_agent_guest_read_guest, docs_superpowers_plans_2026_11_21_plan_4_agent_guest_parse_guest, docs_superpowers_plans_2026_11_21_plan_4_agent_services_chat_get_conversation, docs_superpowers_plans_2026_11_21_plan_4_agent_services_chat_claim_guest_conversations, backend_app_api_auth_register, backend_app_api_auth_login [EXTRACTED 1.00]
- **Đồ thị LangGraph safety_check → agent ⇄ tools → output_guard** — docs_superpowers_plans_2026_11_21_plan_4_agent_graph_build_graph, docs_superpowers_plans_2026_11_21_plan_4_agent_node_safety_check, docs_superpowers_plans_2026_11_21_plan_4_agent_node_urgent_response, docs_superpowers_plans_2026_11_21_plan_4_agent_node_agent, docs_superpowers_plans_2026_11_21_plan_4_agent_node_tools, docs_superpowers_plans_2026_11_21_plan_4_agent_node_output_guard [EXTRACTED 1.00]
- **Bộ 9 tools của agent gọi vào services/ dùng chung** — docs_superpowers_specs_2026_11_21_mediflow_ai_design_do_thi_agent, docs_superpowers_specs_2026_11_21_mediflow_ai_design_search_packages, docs_superpowers_specs_2026_11_21_mediflow_ai_design_list_hospitals, docs_superpowers_specs_2026_11_21_mediflow_ai_design_get_package_details, docs_superpowers_specs_2026_11_21_mediflow_ai_design_compare_packages, docs_superpowers_specs_2026_11_21_mediflow_ai_design_get_available_slots, docs_superpowers_specs_2026_11_21_mediflow_ai_design_create_booking, docs_superpowers_specs_2026_11_21_mediflow_ai_design_get_prep_checklist, docs_superpowers_specs_2026_11_21_mediflow_ai_design_search_prep_docs, docs_superpowers_specs_2026_11_21_mediflow_ai_design_check_symptoms [EXTRACTED 1.00]
- **create_booking joins Package, TimeSlot and Booking under a row lock** — backend_app_services_booking_create_booking, backend_app_services_catalog_get_package, backend_app_services_booking_lock, backend_app_models_package, backend_app_models_timeslot, backend_app_models_booking [EXTRACTED 1.00]
- **Chuỗi sáu kế hoạch thực hiện theo thứ tự** — claude_ke_hoach_1, claude_ke_hoach_2, claude_ke_hoach_3, claude_ke_hoach_4, claude_ke_hoach_5, claude_ke_hoach_6 [EXTRACTED 1.00]
- **Kiến trúc deploy Neon + Render + Vercel** — docs_superpowers_plans_2026_11_21_plan_6_deploy_neon, docs_superpowers_plans_2026_11_21_plan_6_deploy_render, docs_superpowers_plans_2026_11_21_plan_6_deploy_vercel, docs_superpowers_plans_2026_11_21_plan_6_deploy_next_rewrites, docs_superpowers_plans_2026_11_21_plan_6_deploy_dockerfile, docs_superpowers_plans_2026_11_21_plan_6_deploy_database_url_neon [EXTRACTED 1.00]
- **Khung chat trợ lý hiện khối dữ liệu** — docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_assistantwidget, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_messagelist, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_blockview, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_packagecard, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_comparetable, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_slotpicker, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_prepchecklist, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_urgentalert, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_disclaimer [EXTRACTED 1.00]
- **Lỗi nghiệp vụ có .code, router đổi sang HTTPException với thông báo tiếng Việt** — backend_app_services_catalog_catalogerror, backend_app_services_booking_bookingerror, backend_app_api_bookings_raise_http, backend_app_api_packages, docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_ma_loi_dat_lich_sang_http [INFERRED 0.85]
- **Luồng đăng nhập và quay lại đúng trang (cookie hết hạn → /login?next=)** — docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_proxy_ts, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_authprovider, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_safenext, backend_app_api_auth_me, backend_app_api_auth_login [INFERRED 0.85]
- **Luồng xử lý cờ đỏ (lớp 1, lớp 2, mức độ, trả lời cấp cứu, alert)** — docs_superpowers_specs_2026_11_21_mediflow_ai_design_safety_check, docs_superpowers_specs_2026_11_21_mediflow_ai_design_check_symptoms, docs_superpowers_specs_2026_11_21_mediflow_ai_design_muc_co_do, docs_superpowers_specs_2026_11_21_mediflow_ai_design_urgent_response, docs_superpowers_specs_2026_11_21_mediflow_ai_design_bang_alerts, backend_app_safety_red_flags_detect, backend_app_safety_red_flags_evaluate_codes [INFERRED 0.85]
- **Luồng đặt lịch qua trợ lý có xác nhận (interrupt → đăng nhập → confirm → booking.create)** — docs_superpowers_specs_2026_11_21_mediflow_ai_design_create_booking, docs_superpowers_specs_2026_11_21_mediflow_ai_design_xac_nhan_truoc_khi_dat, docs_superpowers_specs_2026_11_21_mediflow_ai_design_checkpointer, docs_superpowers_specs_2026_11_21_mediflow_ai_design_api_hoi_thoai, docs_superpowers_specs_2026_11_21_mediflow_ai_design_khach_chua_dang_nhap, backend_app_services_booking_create_booking [INFERRED 0.85]
- **Môi trường chạy cục bộ: Docker, backend, database** — claude_docker_desktop, claude_backend, claude_postgres_127_0_0_1, claude_backend_env [INFERRED 0.85]

## Communities (74 total, 14 thin omitted)

### Community 0 - "Spec và từ khóa an toàn"
Cohesion: 0.05
Nodes (53): accented_negations, exact, except, phrases, exact, except, not_after, phrases (+45 more)

### Community 1 - "Định dạng giờ Việt Nam"
Cohesion: 0.05
Nodes (49): dayKeyVN(), formatDayVN(), groupSlotsByDay(), SlotPicker, Vitest, eslintConfig, dependencies, @base-ui/react@^1.9.0 (+41 more)

### Community 2 - "Khởi động backend, Docker"
Cohesion: 0.06
Nodes (29): health(), _message(), validation_error(), environment, healthcheck, ports, volumes, POSTGRES_DB (+21 more)

### Community 3 - "Layout trang app, shadcn"
Cohesion: 0.11
Nodes (25): Khởi tạo frontend: create-next-app + shadcn/ui, AppLayout(), PackagesView(), CompareBar(), PackageCard(), FILTER_KEYS, PackageFilters(), SiteHeader() (+17 more)

### Community 4 - "Hạ tầng test Postgres"
Cohesion: 0.10
Nodes (21): catalog(), check_test_url(), client(), _client_for(), consultant_client(), customer(), customer_client(), db() (+13 more)

### Community 5 - "Schema đăng ký, đăng nhập"
Cohesion: 0.07
Nodes (24): me(), RegisterIn, Kế hoạch 3: Giao diện đặt khám (chưa có trợ lý), api(), ApiError, AuthProvider / useAuth(), BACKEND_URL chuyển sang frontend/.env.example, Font Be Vietnam Pro (+16 more)

### Community 6 - "Ngữ pháp luật cờ đỏ"
Cohesion: 0.09
Nodes (27): _clause_before(), evaluate_codes(), Grammar, _grammar(), single_words(), Hit, _list_goes_on(), _load() (+19 more)

### Community 7 - "Guard đầu ra: số tiền"
Cohesion: 0.09
Nodes (21): _after_last_connector(), _amount_patterns(), _contains(), _decimal(), _forbidden_sentences(), _grammar(), alt(), form() (+13 more)

### Community 8 - "Test guard đầu ra"
Cohesion: 0.13
Nodes (26): check(), find_amounts(), find_package_codes(), _seed_guard_args(), test_allowed_medical_wording(), test_code_check_needs_brackets_or_known_hospital(), test_compound_amounts(), test_find_amounts() (+18 more)

### Community 9 - "API đăng nhập, đăng xuất"
Cohesion: 0.11
Nodes (20): login(), logout(), register(), hash_password(), verify_password(), User, _normalize_email(), seed_users() (+12 more)

### Community 10 - "Các page.tsx của app"
Cohesion: 0.13
Nodes (23): metadata, Page(), metadata, Page(), metadata, Page(), metadata, Page() (+15 more)

### Community 11 - "Trang lịch của tôi"
Cohesion: 0.16
Nodes (20): metadata, Page(), BookingsView(), ConsultantView(), STATUS_ITEMS, EmptyState(), Dialog(), DialogContent() (+12 more)

### Community 12 - "Trang bệnh viện, đăng ký"
Cohesion: 0.17
Nodes (18): CITY_ITEMS, HospitalsView(), FIELDS, RegisterView(), HospitalCard(), FilterSelect(), Key, PRICE_MAX (+10 more)

### Community 13 - "API chat (kế hoạch 4)"
Cohesion: 0.14
Nodes (22): GET /api/consultant/conversations/{id}, GET /api/conversations/{id}, models.ChatMessage, POST /api/conversations, POST /api/conversations/{id}/confirm, POST /api/conversations/{id}/messages, schemas.ConfirmIn, schemas.ConversationOut (+14 more)

### Community 14 - "Che PII"
Cohesion: 0.15
Nodes (12): _flags(), _name_end(), redact(), _redact_names(), has_vi_marks(), test_decomposed_accents_are_redacted(), test_keeps_non_pii(), test_long_text_is_fast() (+4 more)

### Community 15 - "Giới hạn ngày, khung giờ"
Cohesion: 0.10
Nodes (9): package_slots(), today_vn(), within_a_year(), test_consultant_date_filter_at_0630_vn(), test_date_from_window_end_is_vn_local(), test_far_dates_rejected(), past_booking_id(), slots() (+1 more)

### Community 16 - "Đăng nhập phía frontend"
Cohesion: 0.15
Nodes (16): confirm(), cancel(), onSubmit(), onSubmit(), Auth, AuthContext, AuthProvider(), fetchMe() (+8 more)

### Community 17 - "Cấu hình shadcn/ui"
Cohesion: 0.09
Nodes (22): shadcn/ui: button, input, card, table, tabs, badge, select, dialog, sheet, calendar, aliases, components, hooks, lib, ui, utils, iconLibrary (+14 more)

### Community 18 - "Router API backend"
Cohesion: 0.18
Nodes (7): ChecklistItem, CompareOut, ItemOut, LoginIn, SlotOut, UserOut, Kiểu dữ liệu TypeScript khớp schema backend (lib/api.ts)

### Community 19 - "Test phát hiện cờ đỏ"
Cohesion: 0.20
Nodes (17): detect(), _strip_marks(), test_bad_yaml_is_rejected(), test_corpus_detected(), test_corpus_no_false_alarm(), test_corpus_unaccented(), test_emergency_detected(), test_every_yaml_phrase_matches_itself() (+9 more)

### Community 20 - "API đặt lịch của khách"
Cohesion: 0.22
Nodes (9): book(), cancel(), checklist(), my_bookings(), raise_http(), BookingIn, BookingOut, ConsultantBookingOut (+1 more)

### Community 21 - "Service danh mục gói"
Cohesion: 0.17
Nodes (13): Package, _active_packages(), get_package(), list_hospitals(), search_packages(), prep_checklist(), city_key(), slug_vi() (+5 more)

### Community 22 - "Kế hoạch 5: khối chat"
Cohesion: 0.13
Nodes (16): BookingCard, PrepChecklist, Kế hoạch 5: Trợ lý AI trên giao diện, AlertItem, AssistantWidget, BookingConfirm, BookingSummary, InlineLogin (+8 more)

### Community 23 - "View đặt lịch và gói"
Cohesion: 0.26
Nodes (14): BookView(), CompareView(), PackageDetailView(), BookingSummary(), CompareTable(), Disclaimer(), ErrorState(), CompareData (+6 more)

### Community 24 - "Alembic và cấu hình"
Cohesion: 0.14
Nodes (6): run_migrations_offline(), run_migrations_online(), _url(), _pk(), dev, Chạy local: Postgres + pgvector, backend (uv, alembic, seed, uvicorn), frontend (npm run dev)

### Community 25 - "Seed dữ liệu mô phỏng"
Cohesion: 0.21
Nodes (12): TimeSlot, _load(), main(), seed_catalog(), seed_slots(), _upsert(), test_seed_catalog_is_idempotent(), test_seed_hospitals_marked_simulated() (+4 more)

### Community 26 - "Chạy thử Gemini"
Cohesion: 0.14
Nodes (6): get_available_slots(), Intake, main(), search_packages(), Task 7: Chạy thử Gemini (cần API key của bạn), get_available_slots (tool agent: khung giờ còn chỗ)

### Community 27 - "Xác thực cookie JWT"
Cohesion: 0.18
Nodes (8): clear_auth_cookie(), create_access_token(), current_user(), optional_user(), require_role(), set_auth_cookie(), get_settings(), create_booking (tool agent: interrupt chờ xác nhận)

### Community 28 - "Đặt/hủy lịch có khóa"
Cohesion: 0.27
Nodes (12): cancel_booking(), create_booking(), _lock(), tomorrow_at(), test_non_duplicate_integrity_error_not_masked(), test_booking_rejections(), test_cancel_booking_reads_fresh_status_under_lock(), test_create_booking_reads_fresh_slot_under_lock() (+4 more)

### Community 29 - "Chọn khung giờ"
Cohesion: 0.22
Nodes (15): SlotPicker(), Slot, dayKeyVN(), formatAudience(), formatDateTimeVN(), formatDayVN(), GENDER_SCOPE, groupSlotsByDay() (+7 more)

### Community 30 - "Cấu hình TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 31 - "API tư vấn viên"
Cohesion: 0.15
Nodes (6): all_bookings(), cancel(), test_role_guards(), API FastAPI đồng bộ dưới /api, API tư vấn viên: cảnh báo cờ đỏ và đọc hội thoại, Giai đoạn 1: nền backend

### Community 32 - "Đồ thị agent LangGraph"
Cohesion: 0.16
Nodes (11): checkpoint.get_checkpointer(), fakes.FakeToolModel, Google Gemini, graph.get_agent(), graph.turn_input(), llm.get_chat_model(), llm.get_embeddings(), llm.message_text() (+3 more)

### Community 33 - "Dữ liệu test cờ đỏ"
Cohesion: 0.12
Nodes (16): co_giat, dau_bung_du_doi, dau_keo_dai, dau_nguc, dot_quy, ho_keo_dai, kho_tho, khoi_u (+8 more)

### Community 34 - "CLAUDE.md và kế hoạch"
Cohesion: 0.13
Nodes (16): frontend/AGENTS.md, Frontend Next.js 16, Đồ thị tri thức graphify-out, Kế hoạch 1: khởi tạo và backend, Kế hoạch 2: lõi an toàn, Kế hoạch 3: giao diện đặt khám, Kế hoạch 4: agent, Kế hoạch 5: trợ lý trên giao diện (+8 more)

### Community 35 - "API bệnh viện"
Cohesion: 0.25
Nodes (9): hospital_detail(), list_hospitals(), HospitalDetailOut, HospitalOut, PackageDetailOut, PackageSummary, get_hospital(), Task 4: Danh mục — service + API bệnh viện/gói/so sánh (+1 more)

### Community 36 - "Service khung giờ"
Cohesion: 0.22
Nodes (6): list_available_slots(), list_bookings(), _local_day_start(), _now(), test_date_from_is_vietnam_local_day(), test_slots_only_from_package_hospital()

### Community 37 - "Trang chủ taste-skill"
Cohesion: 0.20
Nodes (12): Arrow(), Check(), css(), Home(), HOSPITALS, KIT, metadata, PRICES (+4 more)

### Community 38 - "State agent (kế hoạch 4)"
Cohesion: 0.24
Nodes (10): Kế hoạch 4: Trợ lý AI ở backend (LangGraph + Gemini), Bộ hội thoại mẫu conversations.yaml, graph.build_graph(), LangGraph, Node tools, Node urgent_response, red_flags.EMERGENCY_MESSAGE, state.AgentState (+2 more)

### Community 39 - "Tools của agent"
Cohesion: 0.21
Nodes (11): state.AgentContext, test_graph.test_tool_rounds_capped(), test_tools.test_tools_hide_ctx_from_llm(), Tool get_package_details, Tool get_prep_checklist, Tool list_hospitals, Tool search_packages, Tool search_prep_docs (+3 more)

### Community 40 - "Models dữ liệu"
Cohesion: 0.19
Nodes (10): get_db(), Base, Hospital, ServiceItem, test_package_detail_has_items_with_prep(), Kế hoạch 1: Khởi tạo dự án + nền backend, PackageItem (bảng nối package_items, khóa chính kép), Task 2: Config, DB, models, migration đầu tiên, hạ tầng test (+2 more)

### Community 41 - "Test đặt lịch"
Cohesion: 0.24
Nodes (10): book(), first_slot(), test_book_and_price_snapshot(), test_cancel_rules(), test_checklist(), test_consultant_filter_by_date_and_status(), test_double_confirm_rejected(), test_full_slot_not_listed() (+2 more)

### Community 42 - "Form đăng nhập"
Cohesion: 0.30
Nodes (9): LoginView(), Field(), invalid(), useFinishAuth(), useAuth(), Input(), User, consultantAccess() (+1 more)

### Community 43 - "API chi tiết, so sánh gói"
Cohesion: 0.21
Nodes (4): compare_packages(), package_detail(), search_packages(), Tool compare_packages

### Community 44 - "Test danh mục gói"
Cohesion: 0.24
Nodes (8): test_city_filter_common_spellings(), test_compare_errors(), test_filter_male_35(), test_hospital_detail(), test_inactive_package_hidden(), test_negative_age_rejected(), test_sorted_by_price(), test_tag_and_price()

### Community 45 - "Kế hoạch 5: component"
Cohesion: 0.18
Nodes (12): BlockView, BookingCard, CompareTable, Disclaimer, HospitalCard, isKnownBlock(), lib/assistant.test.ts, PackageCard compact (+4 more)

### Community 46 - "Booking và giá chụp"
Cohesion: 0.24
Nodes (6): Booking, BookingError, services.booking.ERROR_MESSAGES, test_graph.test_booking_interrupt_and_resume(), test_graph.test_resume_when_slot_just_filled(), Tool create_booking

### Community 47 - "Node agent và guard"
Cohesion: 0.33
Nodes (9): Node agent, Node output_guard, output_guard.DISCLAIMER, output_guard.SAFE_FALLBACK, prompts.system_prompt(), red_flags.SEE_DOCTOR_NOTE, test_graph.test_guard_rewrites_once_then_falls_back(), today_vn() (+1 more)

### Community 48 - "lib/assistant (kế hoạch 5)"
Cohesion: 0.22
Nodes (7): Block (union theo type), ChatMessage, lib/assistant.ts, safeStorage(), shouldAutoOpen(), SUGGESTIONS và WELCOME, WelcomeMessage

### Community 49 - "Enum và PII khi gửi LLM"
Cohesion: 0.33
Nodes (7): _enum(), GET /api/consultant/alerts, models.Alert, POST /api/consultant/alerts/{id}/resolve, schemas.AlertOut, test_chat_api.test_emergency_creates_alert(), test_consultant_alerts.test_consultant_sees_and_resolves_alerts()

### Community 50 - "So sánh gói"
Cohesion: 0.25
Nodes (5): CompareRow, CatalogError, compare_packages(), test_compare_union_and_order(), compare_packages (tool agent: bảng so sánh)

### Community 51 - "AssistantProvider (kế hoạch 5)"
Cohesion: 0.22
Nodes (8): ApiError, AssistantProvider, Conversation, markSeen(), PageContext, resolveConversation(), Turn, usePageContext

### Community 53 - "Migration khởi tạo"
Cohesion: 0.36
Nodes (3): downgrade(), upgrade(), test_migration_creates_business_tables()

### Community 54 - "System prompt trợ lý"
Cohesion: 0.29
Nodes (3): Task 1: Khung dự án (thư mục, Docker, uv, Next.js), nextConfig, mediflow-backend

### Community 55 - "docker-compose"
Cohesion: 0.36
Nodes (7): services, volumes, pgdata, MediFlow-AI — Thiết kế (phần Cơ bản của đề VMEC-15), MediFlow: nền tảng đặt lịch gói khám định kỳ nhiều bệnh viện (mô phỏng), Đề VMEC-15, MediFlow-AI (README)

### Community 57 - "Settings và .env"
Cohesion: 0.38
Nodes (6): Settings, .env.example: biến môi trường mẫu, mật khẩu seed để trống, guest.ensure_guest(), guest.parse_guest(), guest.read_guest(), guest.sign_guest()

### Community 58 - "Kế hoạch 3: hàm định dạng"
Cohesion: 0.29
Nodes (7): BookingSummary, CITY_OPTIONS, formatDateTimeVN(), formatVnd(), PackageCard, PackageFilters, TAG_LABEL

### Community 59 - "RAG tài liệu chuẩn bị"
Cohesion: 0.38
Nodes (6): Migration agent_tables, models.PrepChunk, pgvector, rag.search_prep_docs(), rag.seed_prep_docs(), Tài liệu chuẩn bị prep_docs

### Community 61 - "CLAUDE.md: chạy và test"
Cohesion: 0.67
Nodes (3): Backend (uv, alembic, seed, pytest), backend/.env (bí mật, không in/commit), Docker Desktop (docker compose up -d)

### Community 63 - "README frontend"
Cohesion: 0.67
Nodes (3): Frontend README (Next.js bootstrapped with create-next-app), Deploy on Vercel, next/font loading the Geist font family

## Knowledge Gaps
- **30 isolated node(s):** `get_package_details (tool agent)`, `list_hospitals (tool agent)`, `ApiError`, `Giai đoạn 3: giao diện đặt khám`, `Ngoài phạm vi: phần Nâng cao đang hoãn` (+25 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 331 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Task 1: Khung dự án (thư mục, Docker, uv, Next.js)` connect `System prompt trợ lý` to `Đồ thị agent LangGraph`, `Định dạng giờ Việt Nam`, `Khởi động backend, Docker`, `State agent (kế hoạch 4)`, `Tools của agent`, `Models dữ liệu`, `API chat (kế hoạch 4)`, `Đăng nhập phía frontend`, `Cấu hình shadcn/ui`, `docker-compose`, `Settings và .env`?**
  _High betweenness centrality (0.177) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `detect()` (e.g. with `Tab 'Cảnh báo cờ đỏ' chừa cho Kế hoạch 5` and `Tab Cảnh báo cờ đỏ của tư vấn viên`) actually correct?**
  _`detect()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `get_package_details (tool agent)`, `list_hospitals (tool agent)`, `ApiError` to the rest of the system?**
  _30 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Spec và từ khóa an toàn` be split into smaller, more focused modules?**
  _Cohesion score 0.05213089802130898 - nodes in this community are weakly interconnected._
- **Why does `Kế hoạch 1: Khởi tạo dự án + nền backend` connect `Models dữ liệu` to `Khởi động backend, Docker`, `API bệnh viện`, `Service khung giờ`, `Hạ tầng test Postgres`, `Schema đăng ký, đăng nhập`, `API đăng nhập, đăng xuất`, `Booking và giá chụp`, `Che PII`, `API đặt lịch của khách`, `System prompt trợ lý`, `docker-compose`, `Seed dữ liệu mô phỏng`, `Chạy thử Gemini`, `Xác thực cookie JWT`, `API tư vấn viên`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `check()` (e.g. with `So khớp chữ trên văn bản đã chuẩn hóa bằng normalize_vi` and `FORBIDDEN_PHRASES`) actually correct?**
  _`check()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `Định dạng giờ Việt Nam` be split into smaller, more focused modules?**
  _Cohesion score 0.05079825834542816 - nodes in this community are weakly interconnected._