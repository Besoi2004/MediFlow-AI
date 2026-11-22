# Graph Report - MediFlow-AI  (2026-11-22)

## Corpus Check
- 2 files · ~46,971 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 811 nodes · 1540 edges · 63 communities (33 shown, 30 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Che PII
- Fixture test (conftest)
- Service đặt lịch và test
- API đăng nhập
- Guard đầu ra
- API đặt lịch của khách
- Spec và quy tắc dự án
- API gói khám
- Models dữ liệu
- Cấu hình ESLint và devDependencies
- Cấu hình shadcn
- Cấu trúc red_flags.yaml
- UI: Dialog
- Cấu hình TypeScript
- Docker Postgres
- UI: Badge và Tabs
- Service danh mục
- Chuẩn hóa chữ tiếng Việt
- Kế hoạch 5: trợ lý giao diện
- Test danh mục
- Kế hoạch 3: giao diện đặt khám
- Dependencies frontend
- Kế hoạch 4: bảng và tools agent
- UI: Sheet
- API bệnh viện
- Kế hoạch 6: deploy
- Layout gốc Next.js
- UI: Card
- UI: Select
- Kế hoạch 4: state và node agent
- Trang danh mục (UI)
- Các kế hoạch triển khai
- Icon mẫu Next.js
- Script npm frontend
- Lỗi danh mục
- Lịch hẹn và checklist (UI)
- Giới hạn ngày giờ VN
- Mẫu trang Next.js
- Stack và deploy
- pyproject backend

## God Nodes (most connected - your core abstractions)
1. `Package` - 27 edges
2. `User` - 24 edges
3. `check()` - 22 edges
4. `TimeSlot` - 21 edges
5. `Booking` - 20 edges
6. `create_booking()` - 20 edges
7. `detect()` - 20 edges
8. `seed_catalog()` - 18 edges
9. `Hospital` - 17 edges
10. `get_settings()` - 17 edges

## Surprising Connections (you probably didn't know these)
- `list_available_slots()` --references--> `VN_TZ`  [EXTRACTED]
  backend/app/services/booking.py → docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md
- `Package as the single shared ORM record for price, eligibility, tags and items` --rationale_for--> `Package`  [EXTRACTED]
  graphify-out/memory/query_20261121_134958_edf6de8f_why_does_package_connect_the_catalog_models_commun.md → backend/app/models.py
- `Query: how create_booking connects Package, TimeSlot and Booking` --references--> `Package`  [EXTRACTED]
  graphify-out/memory/query_20261121_135555_6d5ba0b5_how_does_create_booking_connect_package__timeslot.md → backend/app/models.py
- `Query: why Package bridges catalog and booking communities` --references--> `PackageDetailOut`  [EXTRACTED]
  graphify-out/memory/query_20261121_134958_edf6de8f_why_does_package_connect_the_catalog_models_commun.md → backend/app/schemas.py
- `Query: why Package bridges catalog and booking communities` --references--> `PackageSummary`  [EXTRACTED]
  graphify-out/memory/query_20261121_134958_edf6de8f_why_does_package_connect_the_catalog_models_commun.md → backend/app/schemas.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Assistant safety pipeline (safety_check, check_symptoms, output_guard, PII masking)** — docs_superpowers_specs_2026_11_21_mediflow_ai_design_safety_check, docs_superpowers_specs_2026_11_21_mediflow_ai_design_check_symptoms, docs_superpowers_specs_2026_11_21_mediflow_ai_design_output_guard, docs_superpowers_specs_2026_11_21_mediflow_ai_design_pii_masking [EXTRACTED 0.95]
- **Cụm giao diện trợ lý nổi** — docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_assistantprovider, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_assistantwidget, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_blockview, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_usepagecontext [EXTRACTED 1.00]
- **Kiến trúc deploy Neon + Render + Vercel** — docs_superpowers_plans_2026_11_21_plan_6_deploy_neon, docs_superpowers_plans_2026_11_21_plan_6_deploy_render, docs_superpowers_plans_2026_11_21_plan_6_deploy_vercel [EXTRACTED 1.00]
- **Luồng đặt/hủy lịch** — backend_app_services_booking_list_available_slots, backend_app_services_booking_create_booking, backend_app_services_booking_cancel_booking, backend_app_services_prep_prep_checklist [EXTRACTED 1.00]
- **Pipeline seed dữ liệu mô phỏng** — backend_scripts_seed_seed_catalog, backend_scripts_seed_seed_slots, backend_scripts_seed_seed_users [EXTRACTED 1.00]
- **Ba module lõi an toàn (cờ đỏ, PII, kiểm tra đầu ra)** — backend_app_safety_red_flags_detect, backend_app_safety_pii_redact, backend_app_safety_output_guard_check [EXTRACTED 1.00]
- **Pipeline trợ lý LangGraph an toàn** — docs_superpowers_plans_2026_11_21_plan_4_agent_langgraph_graph, docs_superpowers_plans_2026_11_21_plan_4_agent_red_flag_two_layer, docs_superpowers_plans_2026_11_21_plan_4_agent_output_guard_node, docs_superpowers_plans_2026_11_21_plan_4_agent_agent_tools [EXTRACTED 1.00]
- **Starter template SVG assets in frontend/public** — frontend_public_file, frontend_public_globe, frontend_public_next, frontend_public_vercel, frontend_public_window [INFERRED 0.75]
- **Luồng xử lý lỗi giao diện (api, 422, safeNext, ErrorState)** — docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_lib_api, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_vi_422_handler, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_lib_nav, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_pagestate [INFERRED 0.85]

## Communities (63 total, 30 thin omitted)

### Community 0 - "Che PII"
Cohesion: 0.06
Nodes (43): _flags(), _name_end(), redact(), _redact_names(), _clause_before(), detect(), evaluate_codes(), Grammar (+35 more)

### Community 1 - "Fixture test (conftest)"
Cohesion: 0.05
Nodes (23): run_migrations_offline(), run_migrations_online(), _url(), downgrade(), upgrade(), get_settings(), Settings, get_db() (+15 more)

### Community 2 - "Service đặt lịch và test"
Cohesion: 0.09
Nodes (42): Booking, TimeSlot, BookingError, cancel_booking(), create_booking(), list_available_slots(), list_bookings(), _local_day_start() (+34 more)

### Community 3 - "API đăng nhập"
Cohesion: 0.07
Nodes (18): login(), logout(), me(), register(), clear_auth_cookie(), create_access_token(), current_user(), hash_password() (+10 more)

### Community 4 - "Guard đầu ra"
Cohesion: 0.08
Nodes (34): _after_last_connector(), _amount_patterns(), check(), _contains(), _decimal(), find_amounts(), find_package_codes(), _forbidden_sentences() (+26 more)

### Community 5 - "API đặt lịch của khách"
Cohesion: 0.10
Nodes (12): book(), cancel(), checklist(), my_bookings(), raise_http(), all_bookings(), cancel(), health() (+4 more)

### Community 6 - "Spec và quy tắc dự án"
Cohesion: 0.06
Nodes (33): CLAUDE.md project notes, User rules (simple Vietnamese commit messages, no Claude attribution, never print .env), MediFlow-AI Design Spec, Agent tools (search_packages, compare_packages, get_available_slots, prep tools), FastAPI REST API under /api, Floating AI assistant (LangGraph agent), Booking concurrency rule (SELECT FOR UPDATE), check_symptoms tool (red-flag layer 2) (+25 more)

### Community 7 - "API gói khám"
Cohesion: 0.13
Nodes (14): compare_packages(), package_detail(), package_slots(), search_packages(), BookingIn, CompareOut, CompareRow, ItemOut (+6 more)

### Community 8 - "Models dữ liệu"
Cohesion: 0.15
Nodes (11): _pk(), ServiceItem, city_key(), VN_TZ, _load(), main(), seed_catalog(), seed_slots() (+3 more)

### Community 9 - "Cấu hình ESLint và devDependencies"
Cohesion: 0.12
Nodes (21): eslintConfig, devDependencies, eslint@^9, eslint-config-next@16.4.6, tailwindcss@4.3.3, @tailwindcss/turbopack@4.3.3, @types/node@^20, @types/react@^19 (+13 more)

### Community 10 - "Cấu hình shadcn"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 11 - "Cấu trúc red_flags.yaml"
Cohesion: 0.11
Nodes (18): accented_negations, exact, except, phrases, connectors, coordinators, negations, not_negations (+10 more)

### Community 12 - "UI: Dialog"
Cohesion: 0.18
Nodes (10): Button(), buttonVariants, Calendar(), CalendarDayButton(), DialogContent(), DialogFooter(), DialogOverlay(), DialogPortal() (+2 more)

### Community 13 - "Cấu hình TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 14 - "Docker Postgres"
Cohesion: 0.12
Nodes (16): environment, healthcheck, image, ports, volumes, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER (+8 more)

### Community 15 - "UI: Badge và Tabs"
Cohesion: 0.15
Nodes (9): Badge(), badgeVariants, TabsList(), tabsListVariants, @base-ui/react@^1.9.0, class-variance-authority@^0.7.1, @base-ui/react, class-variance-authority (+1 more)

### Community 16 - "Service danh mục"
Cohesion: 0.30
Nodes (10): Base, Hospital, Package, _active_packages(), get_hospital(), get_package(), list_hospitals(), search_packages() (+2 more)

### Community 17 - "Chuẩn hóa chữ tiếng Việt"
Cohesion: 0.19
Nodes (5): has_vi_marks(), normalize_vi(), slug_vi(), words_vi(), test_slug_vi()

### Community 18 - "Kế hoạch 5: trợ lý giao diện"
Cohesion: 0.14
Nodes (12): lib/assistant.ts (pure logic), AssistantProvider (React context), AssistantWidget, BlockView, BookingConfirm, Tab Cảnh báo cờ đỏ của tư vấn viên, InlineLogin (LoginForm/RegisterForm compact), resolveConversation (+4 more)

### Community 19 - "Test danh mục"
Cohesion: 0.16
Nodes (4): test_city_filter_common_spellings(), test_city_filter_ignores_accents_and_case(), test_compare_errors(), test_inactive_package_hidden()

### Community 20 - "Kế hoạch 3: giao diện đặt khám"
Cohesion: 0.17
Nodes (11): Kế hoạch 3: Giao diện đặt khám, AuthProvider / useAuth, Trang đặt lịch /book/[code], Trang tư vấn viên /consultant, lib/api.ts (api(), ApiError), lib/nav.ts safeNext, Trang đăng nhập và đăng ký, Review Focus kế hoạch 3 (lỗi mạng, 401, 409, múi giờ, 422) (+3 more)

### Community 21 - "Dependencies frontend"
Cohesion: 0.17
Nodes (12): dependencies, cn@^0.5.2, date-fns@^4.4.0, react-day-picker@^10.0.2, react-dom@19.3.0, shadcn@^4.23.0, tw-animate-css@^1.4.0, date-fns (+4 more)

### Community 22 - "Kế hoạch 4: bảng và tools agent"
Cohesion: 0.18
Nodes (10): Bảng Conversation, ChatMessage, Alert, PrepChunk, Tools của agent (search_packages, create_booking...), Quota chat (user, guest, all guests), services/chat.py (send_message, confirm, quota, claim), API cảnh báo và đọc hội thoại cho tư vấn viên, create_booking tool với interrupt() chờ xác nhận, execute_tool_call, LLM factory (init_chat_model, embeddings) (+2 more)

### Community 23 - "UI: Sheet"
Cohesion: 0.22
Nodes (3): SheetContent(), SheetOverlay(), SheetPortal()

### Community 24 - "API bệnh viện"
Cohesion: 0.31
Nodes (4): hospital_detail(), list_hospitals(), HospitalDetailOut, HospitalOut

### Community 25 - "Kế hoạch 6: deploy"
Cohesion: 0.27
Nodes (7): Kế hoạch 5: Trợ lý AI trên giao diện, Kế hoạch 6: Deploy lên cloud, backend/Dockerfile, Neon Postgres + pgvector, Render Web Service (Docker backend), scripts/smoke.py, Vercel (Next.js frontend)

### Community 26 - "Layout gốc Next.js"
Cohesion: 0.20
Nodes (6): geistMono, geistSans, metadata, nextConfig, next@16.4.6, next

### Community 28 - "UI: Select"
Cohesion: 0.24
Nodes (3): SelectContent(), SelectScrollDownButton(), SelectScrollUpButton()

### Community 29 - "Kế hoạch 4: state và node agent"
Cohesion: 0.22
Nodes (7): AgentState và AgentContext, FakeToolModel (test), Đồ thị LangGraph safety_check→agent⇄tools→output_guard, PostgresSaver checkpointer, Cờ đỏ hai lớp (safety_check + tool check_symptoms), scripts/run_eval.py và conversations.yaml (16 kịch bản), system_prompt (ngày hôm nay, page context)

### Community 31 - "Trang danh mục (UI)"
Cohesion: 0.29
Nodes (7): Trang danh mục (home, hospitals, packages, compare), CompareTable, lib/format.ts (formatVnd, formatDateTimeVN, toggleCode...), PackageCard, proxy.ts (Next 16 route guard), API /api/conversations, Cookie khách ký HMAC (guest.py)

### Community 32 - "Các kế hoạch triển khai"
Cohesion: 0.40
Nodes (5): Implementation plans 1-6 status table (plans 1-2 done), Kế hoạch 1: Khởi tạo dự án + nền backend, Monorepo backend FastAPI + frontend Next.js, Kế hoạch 2: Lõi an toàn, Kế hoạch 4: Trợ lý AI ở backend

### Community 33 - "Icon mẫu Next.js"
Cohesion: 0.40
Nodes (6): Default create-next-app starter assets, File icon (document page outline, grey), Globe icon (circle with meridians), Next.js wordmark logo (black), Vercel triangle logo (white), Browser window icon (grey)

### Community 34 - "Script npm frontend"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

## Knowledge Gaps
- **43 isolated node(s):** `mediflow-backend`, `CompareTable`, `Trang tư vấn viên /consultant`, `lib/format.ts (formatVnd, formatDateTimeVN, toggleCode...)`, `SiteHeader` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 341 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Đồ thị LangGraph safety_check→agent⇄tools→output_guard` connect `Kế hoạch 4: state và node agent` to `Các kế hoạch triển khai`, `Che PII`, `Guard đầu ra`, `Kế hoạch 4: bảng và tools agent`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Package` (e.g. with `PackageDetailOut` and `PackageSummary`) actually correct?**
  _`Package` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `mediflow-backend`, `CompareTable`, `Trang tư vấn viên /consultant` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Che PII` be split into smaller, more focused modules?**
  _Cohesion score 0.06105834464043419 - nodes in this community are weakly interconnected._
- **Why does `Implementation plans 1-6 status table (plans 1-2 done)` connect `Các kế hoạch triển khai` to `Kế hoạch 6: deploy`, `Kế hoạch 3: giao diện đặt khám`, `Spec và quy tắc dự án`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `User` (e.g. with `login()` and `current_user()`) actually correct?**
  _`User` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `Fixture test (conftest)` be split into smaller, more focused modules?**
  _Cohesion score 0.05081585081585081 - nodes in this community are weakly interconnected._