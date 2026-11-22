# Graph Report - MediFlow-AI  (2026-11-23)

## Corpus Check
- 99 files · ~50,986 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 16 file(s) not represented in the graph (top: (none) 10, .example 1, .ini 1)

## Summary
- 1098 nodes · 2822 edges · 61 communities (52 shown, 9 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 447 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- API đặt lịch của khách
- API bệnh viện và gói khám
- Kế hoạch 6: deploy
- Guard đầu ra: mã gói và số tiền
- Phát hiện cờ đỏ
- Seed dữ liệu mô phỏng
- Hạ tầng test Postgres
- Models dữ liệu
- API đăng nhập
- Kế hoạch 5: trợ lý giao diện
- API chat (kế hoạch 4)
- Luật cờ đỏ YAML hai lớp
- Guard đầu ra: câu cấm
- Cấu hình shadcn
- Cấu hình ESLint và devDependencies
- Test cờ đỏ
- Khung dự án và trang Next.js
- Cấu hình, JWT và Alembic env
- Chuẩn hóa chữ và che tên
- Thử Gemini (spike)
- Thư viện api.ts và assistant.ts
- LLM và đồ thị agent
- Cấu hình TypeScript
- Node và prompt của agent
- Kế hoạch 3: proxy và Next config
- Bộ câu mẫu cờ đỏ
- Spec và quy tắc dự án
- UI: Dialog, Button, Calendar
- Tools của agent
- Phân quyền theo vai trò
- Layout gốc và script npm
- UI: Badge, Tabs, Input
- Che PII
- Nguyên tắc thiết kế agent
- Mức cờ đỏ và evaluate_codes
- Khối giao diện trong chat
- Dependencies frontend
- UI: Select
- Trang danh mục
- Settings và khách chưa đăng nhập
- Kế hoạch 4: checkpointer và eval
- UI: Card
- UI: Sheet
- Giai đoạn 0 và dữ liệu mẫu
- Hội thoại trợ lý (spec)
- Hạ tầng deploy và RAG
- Định dạng giờ VN và tiền
- So sánh gói
- Cảnh báo cờ đỏ cho tư vấn viên
- RAG tài liệu chuẩn bị
- Cú pháp cụm trong red_flags.yaml
- Docker Postgres và chạy local
- Disclaimer
- Icon file.svg
- Icon globe.svg
- Logo Next.js
- Logo Vercel
- Icon window.svg

## God Nodes (most connected - your core abstractions)
1. `Package` - 33 edges
2. `detect()` - 32 edges
3. `User` - 30 edges
4. `check()` - 30 edges
5. `create_booking()` - 29 edges
6. `Task 6: Khung giờ, đặt/hủy lịch, checklist chuẩn bị, trang tư vấn viên` - 28 edges
7. `Task 1: Khung dự án (thư mục, Docker, uv, Next.js)` - 27 edges
8. `Booking` - 26 edges
9. `TimeSlot` - 25 edges
10. `normalize_vi()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Tool search_packages` --semantically_similar_to--> `search_packages()`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-11-21-plan-4-agent.md → backend/app/api/packages.py
- `proxy.ts` --semantically_similar_to--> `require_role()`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-11-21-plan-3-giao-dien-dat-kham.md → backend/app/auth.py
- `today_vn()` --semantically_similar_to--> `today_vn()`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-11-21-plan-4-agent.md → backend/tests/test_booking.py
- `Tool create_booking` --semantically_similar_to--> `book()`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-11-21-plan-4-agent.md → backend/app/api/bookings.py
- `Tool compare_packages` --semantically_similar_to--> `compare_packages()`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-11-21-plan-4-agent.md → backend/app/api/packages.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Bộ 9 tools của agent gọi vào services/ dùng chung** — docs_superpowers_specs_2026_11_21_mediflow_ai_design_do_thi_agent, docs_superpowers_specs_2026_11_21_mediflow_ai_design_search_packages, docs_superpowers_specs_2026_11_21_mediflow_ai_design_list_hospitals, docs_superpowers_specs_2026_11_21_mediflow_ai_design_get_package_details, docs_superpowers_specs_2026_11_21_mediflow_ai_design_compare_packages, docs_superpowers_specs_2026_11_21_mediflow_ai_design_get_available_slots, docs_superpowers_specs_2026_11_21_mediflow_ai_design_create_booking, docs_superpowers_specs_2026_11_21_mediflow_ai_design_get_prep_checklist, docs_superpowers_specs_2026_11_21_mediflow_ai_design_search_prep_docs, docs_superpowers_specs_2026_11_21_mediflow_ai_design_check_symptoms [EXTRACTED 1.00]
- **Luồng đặt lịch qua trợ lý có xác nhận (interrupt → đăng nhập → confirm → booking.create)** — docs_superpowers_specs_2026_11_21_mediflow_ai_design_create_booking, docs_superpowers_specs_2026_11_21_mediflow_ai_design_xac_nhan_truoc_khi_dat, docs_superpowers_specs_2026_11_21_mediflow_ai_design_checkpointer, docs_superpowers_specs_2026_11_21_mediflow_ai_design_api_hoi_thoai, docs_superpowers_specs_2026_11_21_mediflow_ai_design_khach_chua_dang_nhap, backend_app_services_booking_create_booking [INFERRED 0.85]
- **Luồng xử lý cờ đỏ (lớp 1, lớp 2, mức độ, trả lời cấp cứu, alert)** — docs_superpowers_specs_2026_11_21_mediflow_ai_design_safety_check, docs_superpowers_specs_2026_11_21_mediflow_ai_design_check_symptoms, docs_superpowers_specs_2026_11_21_mediflow_ai_design_muc_co_do, docs_superpowers_specs_2026_11_21_mediflow_ai_design_urgent_response, docs_superpowers_specs_2026_11_21_mediflow_ai_design_bang_alerts, backend_app_safety_red_flags_detect, backend_app_safety_red_flags_evaluate_codes [INFERRED 0.85]
- **create_booking joins Package, TimeSlot and Booking under a row lock** — backend_app_services_booking_create_booking, backend_app_services_catalog_get_package, backend_app_services_booking_lock, backend_app_models_package, backend_app_models_timeslot, backend_app_models_booking [EXTRACTED 1.00]
- **Lỗi nghiệp vụ có .code, router đổi sang HTTPException với thông báo tiếng Việt** — backend_app_services_catalog_catalogerror, backend_app_services_booking_bookingerror, backend_app_api_bookings_raise_http, backend_app_api_packages, docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_ma_loi_dat_lich_sang_http [INFERRED 0.85]
- **5 điểm Review Focus của Kế hoạch 1** — docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_rf1_loc_tinh_thanh_khong_dau, docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_rf2_date_from_gio_viet_nam, docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_rf3_chong_dat_trung, docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_rf4_khong_huy_lich_da_qua, docs_superpowers_plans_2026_11_21_plan_1_khoi_tao_va_backend_rf5_email_khong_phan_biet_hoa_thuong [EXTRACTED 1.00]
- **Fixture dùng chung chuyển từ test_booking.py sang conftest.py** — docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_chuyen_fixture_sang_conftest, backend_tests_test_booking_make_slot, backend_tests_test_booking_customer, backend_tests_test_booking_customer_client, backend_tests_test_booking_other_client, backend_tests_test_booking_consultant_client, backend_tests_test_booking_two_customer_ids, backend_tests_test_booking_today_vn, backend_tests_test_booking_tomorrow_at [EXTRACTED 1.00]
- **Các trang App Router theo mẫu Suspense + *View** — docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_mau_trang_suspense_view, frontend_app_page, frontend_app_login_page, frontend_app_register_page, frontend_app_hospitals_page, frontend_app_hospitals_code_page, frontend_app_packages_page, frontend_app_packages_code_page, frontend_app_compare_page, frontend_app_book_code_page, frontend_app_bookings_page, frontend_app_consultant_page [EXTRACTED 1.00]
- **Luồng đăng nhập và quay lại đúng trang (cookie hết hạn → /login?next=)** — docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_proxy_ts, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_authprovider, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_safenext, frontend_app_login_page, frontend_app_register_page, backend_app_api_auth_me, backend_app_api_auth_login [INFERRED 0.85]
- **Đồ thị LangGraph safety_check → agent ⇄ tools → output_guard** — docs_superpowers_plans_2026_11_21_plan_4_agent_graph_build_graph, docs_superpowers_plans_2026_11_21_plan_4_agent_node_safety_check, docs_superpowers_plans_2026_11_21_plan_4_agent_node_urgent_response, docs_superpowers_plans_2026_11_21_plan_4_agent_node_agent, docs_superpowers_plans_2026_11_21_plan_4_agent_node_tools, docs_superpowers_plans_2026_11_21_plan_4_agent_node_output_guard [EXTRACTED 1.00]
- **Luồng đặt lịch có xác nhận: interrupt → /confirm → resume** — docs_superpowers_plans_2026_11_21_plan_4_agent_tool_create_booking, docs_superpowers_plans_2026_11_21_plan_4_agent_bước_dừng_chờ_xác_nhận_đặt_lịch, docs_superpowers_plans_2026_11_21_plan_4_agent_services_chat_send_message, docs_superpowers_plans_2026_11_21_plan_4_agent_services_chat_confirm, docs_superpowers_plans_2026_11_21_plan_4_agent_post_api_conversations_id_confirm, backend_app_services_booking_create_booking, docs_superpowers_plans_2026_11_21_plan_4_agent_schemas_turnout [EXTRACTED 1.00]
- **Khách chưa đăng nhập: cookie khách → chuyển hội thoại khi đăng nhập** — docs_superpowers_plans_2026_11_21_plan_4_agent_guest_ensure_guest, docs_superpowers_plans_2026_11_21_plan_4_agent_guest_read_guest, docs_superpowers_plans_2026_11_21_plan_4_agent_guest_parse_guest, docs_superpowers_plans_2026_11_21_plan_4_agent_services_chat_get_conversation, docs_superpowers_plans_2026_11_21_plan_4_agent_services_chat_claim_guest_conversations, backend_app_api_auth_register, backend_app_api_auth_login [EXTRACTED 1.00]
- **Khung chat trợ lý hiện khối dữ liệu** — docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_assistantwidget, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_messagelist, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_blockview, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_packagecard, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_comparetable, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_slotpicker, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_prepchecklist, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_urgentalert, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_disclaimer [EXTRACTED 1.00]
- **Đặt lịch qua trợ lý có thẻ xác nhận và đăng nhập trong chat** — docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_bookingconfirm, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_inlinelogin, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_loginform, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_registerform, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_pendingbooking, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_assistantprovider [EXTRACTED 1.00]
- **Kiến trúc deploy Neon + Render + Vercel** — docs_superpowers_plans_2026_11_21_plan_6_deploy_neon, docs_superpowers_plans_2026_11_21_plan_6_deploy_render, docs_superpowers_plans_2026_11_21_plan_6_deploy_vercel, docs_superpowers_plans_2026_11_21_plan_6_deploy_next_rewrites, docs_superpowers_plans_2026_11_21_plan_6_deploy_dockerfile, docs_superpowers_plans_2026_11_21_plan_6_deploy_database_url_neon [EXTRACTED 1.00]

## Communities (61 total, 9 thin omitted)

### Community 0 - "API đặt lịch của khách"
Cohesion: 0.06
Nodes (62): book(), cancel(), checklist(), my_bookings(), raise_http(), all_bookings(), cancel(), Booking (+54 more)

### Community 1 - "API bệnh viện và gói khám"
Cohesion: 0.05
Nodes (45): hospital_detail(), list_hospitals(), compare_packages(), package_detail(), package_slots(), search_packages(), Package, CompareOut (+37 more)

### Community 2 - "Kế hoạch 6: deploy"
Cohesion: 0.07
Nodes (28): health(), environment, healthcheck, ports, volumes, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER (+20 more)

### Community 3 - "Guard đầu ra: mã gói và số tiền"
Cohesion: 0.13
Nodes (27): check(), find_amounts(), find_package_codes(), _seed_guard_args(), test_allowed_medical_wording(), test_code_check_needs_brackets_or_known_hospital(), test_compound_amounts(), test_find_amounts() (+19 more)

### Community 4 - "Phát hiện cờ đỏ"
Cohesion: 0.11
Nodes (18): _clause_before(), Grammar, _grammar(), single_words(), _list_goes_on(), _load(), _negated(), Pattern (+10 more)

### Community 5 - "Seed dữ liệu mô phỏng"
Cohesion: 0.14
Nodes (16): city_key(), slug_vi(), _load(), main(), seed_catalog(), seed_slots(), seed_users(), _upsert() (+8 more)

### Community 6 - "Hạ tầng test Postgres"
Cohesion: 0.12
Nodes (12): get_db(), catalog(), check_test_url(), client(), db(), engine(), settings_with_seed_passwords(), _test_url() (+4 more)

### Community 7 - "Models dữ liệu"
Cohesion: 0.14
Nodes (16): downgrade(), upgrade(), Base, _enum(), Hospital, _pk(), ServiceItem, User (+8 more)

### Community 8 - "API đăng nhập"
Cohesion: 0.14
Nodes (13): login(), logout(), register(), clear_auth_cookie(), hash_password(), verify_password(), test_logout_then_me_401(), test_register_sets_httponly_cookie_and_customer_role() (+5 more)

### Community 9 - "Kế hoạch 5: trợ lý giao diện"
Cohesion: 0.12
Nodes (21): SiteHeader, Kế hoạch 5: Trợ lý AI trên giao diện, AssistantProvider, AssistantWidget, BookingConfirm, BookingSummary, InlineLogin, LoginForm (+13 more)

### Community 10 - "API chat (kế hoạch 4)"
Cohesion: 0.15
Nodes (22): GET /api/consultant/conversations/{id}, GET /api/conversations/{id}, models.ChatMessage, POST /api/conversations, POST /api/conversations/{id}/confirm, POST /api/conversations/{id}/messages, schemas.ConfirmIn, schemas.ConversationOut (+14 more)

### Community 11 - "Luật cờ đỏ YAML hai lớp"
Cohesion: 0.11
Nodes (21): accented_negations, exact, except, phrases, connectors, coordinators, negations, not_negations (+13 more)

### Community 12 - "Guard đầu ra: câu cấm"
Cohesion: 0.14
Nodes (12): _after_last_connector(), _amount_patterns(), _contains(), _decimal(), _forbidden_sentences(), _Grammar, _hospital_mentions(), _is_forbidden() (+4 more)

### Community 13 - "Cấu hình shadcn"
Cohesion: 0.09
Nodes (22): shadcn/ui: button, input, card, table, tabs, badge, select, dialog, sheet, calendar, aliases, components, hooks, lib, ui, utils, iconLibrary (+14 more)

### Community 14 - "Cấu hình ESLint và devDependencies"
Cohesion: 0.12
Nodes (21): eslintConfig, devDependencies, eslint@^9, eslint-config-next@16.4.6, tailwindcss@4.3.3, @tailwindcss/turbopack@4.3.3, @types/node@^20, @types/react@^19 (+13 more)

### Community 15 - "Test cờ đỏ"
Cohesion: 0.20
Nodes (16): detect(), _strip_marks(), test_corpus_detected(), test_corpus_no_false_alarm(), test_corpus_unaccented(), test_emergency_detected(), test_every_yaml_phrase_matches_itself(), test_long_message_is_fast() (+8 more)

### Community 16 - "Khung dự án và trang Next.js"
Cohesion: 0.18
Nodes (10): Task 1: Khung dự án (thư mục, Docker, uv, Next.js), AuthProvider / useAuth(), BookingCard, maxFastingHours(), PackageCard, PrepChecklist, proxy.ts, safeNext() (+2 more)

### Community 17 - "Cấu hình, JWT và Alembic env"
Cohesion: 0.15
Nodes (7): run_migrations_offline(), run_migrations_online(), _url(), create_access_token(), optional_user(), set_auth_cookie(), get_settings()

### Community 18 - "Chuẩn hóa chữ và che tên"
Cohesion: 0.15
Nodes (10): _grammar(), alt(), form(), _flags(), _marks_optional(), _name_end(), _redact_names(), normalize_vi() (+2 more)

### Community 19 - "Thử Gemini (spike)"
Cohesion: 0.13
Nodes (6): get_available_slots(), Intake, main(), search_packages(), Task 7: Chạy thử Gemini (cần API key của bạn), get_available_slots (tool agent: khung giờ còn chỗ)

### Community 20 - "Thư viện api.ts và assistant.ts"
Cohesion: 0.13
Nodes (17): ApiError, AlertItem, ApiError, Block (union theo type), ChatMessage, Conversation, isKnownBlock(), lib/assistant.ts (+9 more)

### Community 21 - "LLM và đồ thị agent"
Cohesion: 0.15
Nodes (12): checkpoint.get_checkpointer(), fakes.FakeToolModel, Google Gemini, graph.get_agent(), graph.turn_input(), llm.get_chat_model(), llm.get_embeddings(), llm.message_text() (+4 more)

### Community 22 - "Cấu hình TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 23 - "Node và prompt của agent"
Cohesion: 0.21
Nodes (13): graph.build_graph(), Node agent, Node output_guard, Node tools, Node urgent_response, output_guard.DISCLAIMER, output_guard.SAFE_FALLBACK, prompts.system_prompt() (+5 more)

### Community 24 - "Kế hoạch 3: proxy và Next config"
Cohesion: 0.14
Nodes (10): me(), Kế hoạch 3: Giao diện đặt khám (chưa có trợ lý), api(), BACKEND_URL chuyển sang frontend/.env.example, PageState (PageSkeleton, ErrorState, EmptyState), proxy.ts (middleware.ts trước Next.js 16) chặn route cần đăng nhập, frontend/AGENTS.md (nextjs-agent-rules), nextConfig (+2 more)

### Community 25 - "Bộ câu mẫu cờ đỏ"
Cohesion: 0.12
Nodes (16): co_giat, dau_bung_du_doi, dau_keo_dai, dau_nguc, dot_quy, ho_keo_dai, kho_tho, khoi_u (+8 more)

### Community 26 - "Spec và quy tắc dự án"
Cohesion: 0.17
Nodes (14): MediFlow-AI — ghi chú cho Claude (CLAUDE.md), Đồ thị tri thức graphify-out (GRAPH_REPORT.md, /graphify --update sau mỗi kế hoạch), Kế hoạch 2: lõi an toàn (xong), Kế hoạch 3: giao diện đặt khám (chưa làm), Kế hoạch 4: agent (chưa làm), Kế hoạch 5: trợ lý trên giao diện (chưa làm), MediFlow-AI — Thiết kế (phần Cơ bản của đề VMEC-15), Giai đoạn 3: giao diện đặt khám (+6 more)

### Community 27 - "UI: Dialog, Button, Calendar"
Cohesion: 0.21
Nodes (9): Khởi tạo frontend: create-next-app + shadcn/ui, Button(), buttonVariants, Calendar(), CalendarDayButton(), DialogContent(), DialogFooter(), DialogOverlay() (+1 more)

### Community 28 - "Tools của agent"
Cohesion: 0.17
Nodes (11): state.AgentContext, test_graph.test_tool_rounds_capped(), test_tools.test_tools_hide_ctx_from_llm(), Tool get_package_details, Tool get_prep_checklist, Tool list_hospitals, Tool search_packages, Tool search_prep_docs (+3 more)

### Community 29 - "Phân quyền theo vai trò"
Cohesion: 0.18
Nodes (8): current_user(), require_role(), test_register_ignores_role_field(), test_lists_are_scoped(), test_role_guards(), Kế hoạch 1: Khởi tạo dự án + nền backend, create_booking (tool agent: interrupt chờ xác nhận), Giai đoạn 1: nền backend

### Community 30 - "Layout gốc và script npm"
Cohesion: 0.15
Nodes (13): Font Be Vietnam Pro, Vitest, geistMono, geistSans, metadata, scripts, build, dev (+5 more)

### Community 31 - "UI: Badge, Tabs, Input"
Cohesion: 0.18
Nodes (8): Badge(), badgeVariants, TabsList(), tabsListVariants, class-variance-authority@^0.7.1, @base-ui/react, class-variance-authority, cn

### Community 32 - "Che PII"
Cohesion: 0.26
Nodes (7): redact(), test_decomposed_accents_are_redacted(), test_keeps_non_pii(), test_long_text_is_fast(), test_redact_never_hides_red_flags(), test_redacts(), test_redacts_several_in_one_message()

### Community 33 - "Nguyên tắc thiết kế agent"
Cohesion: 0.29
Nodes (5): Checkpointer PostgresSaver (langgraph-checkpoint-postgres), Đồ thị LangGraph: safety_check → agent ⇄ tools → output_guard, Giai đoạn 4: agent (tools, graph, checkpointer, RAG, API chat, khách chưa đăng nhập), System prompt của agent, test_graph.py: test đồ thị agent bằng chat model giả

### Community 34 - "Mức cờ đỏ và evaluate_codes"
Cohesion: 0.22
Nodes (11): evaluate_codes(), Hit, worst(), test_evaluate_codes_and_symptom_codes(), test_messages_are_fixed_vietnamese(), test_worst_accepts_severities(), EMERGENCY_MESSAGE, SEE_DOCTOR_NOTE (+3 more)

### Community 35 - "Khối giao diện trong chat"
Cohesion: 0.15
Nodes (12): BlockView, BookingCard, CompareTable, Disclaimer, HospitalCard, MessageList, PackageCard compact, PrepChecklist (+4 more)

### Community 36 - "Dependencies frontend"
Cohesion: 0.15
Nodes (13): dependencies, @base-ui/react@^1.9.0, cn@^0.5.2, date-fns@^4.4.0, react-day-picker@^10.0.2, react-dom@19.3.0, shadcn@^4.23.0, tw-animate-css@^1.4.0 (+5 more)

### Community 37 - "UI: Select"
Cohesion: 0.20
Nodes (5): SelectContent(), SelectScrollDownButton(), SelectScrollUpButton(), lucide-react@^1.77.0, lucide-react

### Community 38 - "Trang danh mục"
Cohesion: 0.20
Nodes (5): CITY_OPTIONS, HospitalCard, PackageFilters, TAG_LABEL, Home()

### Community 39 - "Settings và khách chưa đăng nhập"
Cohesion: 0.27
Nodes (7): Settings, .env.example: biến môi trường mẫu, mật khẩu seed để trống, guest.ensure_guest(), guest.parse_guest(), guest.read_guest(), guest.sign_guest(), Biến môi trường chính (.env.example)

### Community 40 - "Kế hoạch 4: checkpointer và eval"
Cohesion: 0.31
Nodes (7): Kế hoạch 4: Trợ lý AI ở backend (LangGraph + Gemini), Bộ hội thoại mẫu conversations.yaml, checkpoint.make_checkpointer(), LangGraph, test_graph.test_postgres_checkpointer_resumes_in_new_graph(), test_graph.test_symptom_tool_escalates(), Tool check_symptoms

### Community 42 - "UI: Sheet"
Cohesion: 0.24
Nodes (3): SheetContent(), SheetOverlay(), SheetPortal()

### Community 43 - "Giai đoạn 0 và dữ liệu mẫu"
Cohesion: 0.33
Nodes (7): Kế hoạch 1: khởi tạo và backend (xong), State của agent (messages, user_context, page_context, red_flag, turn_blocks), Bệnh viện mẫu ALP/BET/GAM và gói mẫu (mã có tiền tố bệnh viện), Bộ hội thoại mẫu tests/eval/conversations.yaml (chạy bằng run_eval.py), Gemini 3.5 Flash-Lite (LLM miễn phí), Giai đoạn 0: khởi tạo và chạy thử Gemini (spike_llm.py), search_packages (tool agent: lọc gói bằng SQL)

### Community 44 - "Hội thoại trợ lý (spec)"
Cohesion: 0.42
Nodes (6): API hội thoại trợ lý /conversations (tạo, đọc, gửi tin, confirm), Trợ lý nổi AssistantWidget (panel chat trên mọi trang), Bảng chat_messages (text đã che PII, blocks, page_context), Bảng conversations (id = thread_id LangGraph, user_id hoặc guest_id), Giai đoạn 5: trợ lý trên giao diện, Trợ lý AI tích hợp

### Community 46 - "Hạ tầng deploy và RAG"
Cohesion: 0.29
Nodes (7): Kế hoạch 6: deploy (chưa làm), image, Bảng prep_chunks (embedding vector cho RAG), Embedding qua API Gemini (gemini-embedding-2, 768 chiều), Giai đoạn 6: deploy (Dockerfile, Neon vector, Render alembic, Vercel BACKEND_URL), Hạ tầng deploy: Vercel + Render (Docker) + Neon (Postgres pgvector), search_prep_docs (tool agent: RAG trên prep_chunks)

### Community 47 - "Định dạng giờ VN và tiền"
Cohesion: 0.32
Nodes (7): BookingSummary, dayKeyVN(), formatDateTimeVN(), formatDayVN(), formatVnd(), groupSlotsByDay(), SlotPicker

### Community 48 - "So sánh gói"
Cohesion: 0.29
Nodes (3): CompareBar, CompareTable, compare_packages (tool agent: bảng so sánh)

### Community 49 - "Cảnh báo cờ đỏ cho tư vấn viên"
Cohesion: 0.48
Nodes (6): GET /api/consultant/alerts, models.Alert, POST /api/consultant/alerts/{id}/resolve, schemas.AlertOut, test_chat_api.test_emergency_creates_alert(), test_consultant_alerts.test_consultant_sees_and_resolves_alerts()

### Community 50 - "RAG tài liệu chuẩn bị"
Cohesion: 0.38
Nodes (6): Migration agent_tables, models.PrepChunk, pgvector, rag.search_prep_docs(), rag.seed_prep_docs(), Tài liệu chuẩn bị prep_docs

### Community 51 - "Cú pháp cụm trong red_flags.yaml"
Cohesion: 0.33
Nodes (6): exact, except, not_after, phrases, still_if, any_of

### Community 52 - "Docker Postgres và chạy local"
Cohesion: 0.50
Nodes (4): Chạy và test backend: docker compose up -d, uv sync, alembic upgrade head, seed, pytest, volumes, pgdata, Chạy local: Postgres + pgvector, backend (uv, alembic, seed, uvicorn), frontend (npm run dev)

### Community 53 - "Disclaimer"
Cohesion: 0.67
Nodes (3): DISCLAIMER (output_guard), Disclaimer (components/Disclaimer.tsx), DISCLAIMER (lib/constants.ts)

## Knowledge Gaps
- **17 isolated node(s):** `list_hospitals (tool agent)`, `get_package_details (tool agent)`, `Đồ thị tri thức graphify-out (GRAPH_REPORT.md, /graphify --update sau mỗi kế hoạch)`, `Tài liệu chuẩn bị prep_docs`, `ApiError` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 278 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Task 1: Khung dự án (thư mục, Docker, uv, Next.js)` connect `Khung dự án và trang Next.js` to `Kế hoạch 6: deploy`, `Trang danh mục`, `Settings và khách chưa đăng nhập`, `API chat (kế hoạch 4)`, `Cấu hình shadcn`, `Cấu hình ESLint và devDependencies`, `So sánh gói`, `Docker Postgres và chạy local`, `LLM và đồ thị agent`, `Thư viện api.ts và assistant.ts`, `Node và prompt của agent`, `Kế hoạch 3: proxy và Next config`, `Tools của agent`, `Phân quyền theo vai trò`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Package` (e.g. with `Mã bệnh viện 3 chữ viết hoa (ALP, BET, GAM), mã gói dạng {MÃ_BV}-{LOẠI} (ALP-CB01)` and `Tiền là số nguyên VND (int)`) actually correct?**
  _`Package` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `list_hospitals (tool agent)`, `get_package_details (tool agent)`, `Đồ thị tri thức graphify-out (GRAPH_REPORT.md, /graphify --update sau mỗi kế hoạch)` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `API đặt lịch của khách` be split into smaller, more focused modules?**
  _Cohesion score 0.055270920664493094 - nodes in this community are weakly interconnected._
- **Why does `Kế hoạch 1: Khởi tạo dự án + nền backend` connect `Phân quyền theo vai trò` to `API đặt lịch của khách`, `API bệnh viện và gói khám`, `Kế hoạch 6: deploy`, `Seed dữ liệu mô phỏng`, `Hạ tầng test Postgres`, `Models dữ liệu`, `API đăng nhập`, `Khung dự án và trang Next.js`, `Chuẩn hóa chữ và che tên`, `Thử Gemini (spike)`, `Kế hoạch 3: proxy và Next config`, `Spec và quy tắc dự án`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `detect()` (e.g. with `Tab 'Cảnh báo cờ đỏ' chừa cho Kế hoạch 5` and `Tab Cảnh báo cờ đỏ của tư vấn viên`) actually correct?**
  _`detect()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `API bệnh viện và gói khám` be split into smaller, more focused modules?**
  _Cohesion score 0.05467856325783574 - nodes in this community are weakly interconnected._