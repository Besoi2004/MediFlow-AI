# Graph Report - MediFlow-AI  (2026-11-21)

## Corpus Check
- Corpus is ~39,432 words - fits in a single context window. You may not need a graph.

## Summary
- 691 nodes · 1257 edges · 58 communities (23 shown, 35 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.91)
- Token cost: 499,063 input · 0 output

## Community Hubs (Navigation)
- Cấu hình và migration DB
- API đặt lịch của khách
- API bệnh viện và gói khám
- Cấu hình khung Next.js
- API đăng nhập
- Service đặt lịch và test
- Kế hoạch 3: giao diện đặt khám
- Models và danh mục
- Spec và quy tắc dự án
- Kế hoạch 5: trợ lý giao diện
- Cấu hình shadcn
- Cấu hình TypeScript
- Docker Postgres
- Test danh mục
- UI: Badge và Tabs
- UI: Select
- Kế hoạch 2: lõi an toàn
- UI: Dialog
- UI: Sheet
- UI: Button và Calendar
- UI: Input
- Icon mẫu Next.js
- Kế hoạch 1 và nền tảng
- Lịch hẹn và checklist (UI)
- Giới hạn ngày giờ VN
- Mẫu trang Next.js
- Stack và deploy
- Hàm red_flags.worst
- Quy tắc của người dùng
- pyproject backend

## God Nodes (most connected - your core abstractions)
1. `User` - 24 edges
2. `Package` - 24 edges
3. `TimeSlot` - 20 edges
4. `Booking` - 19 edges
5. `create_booking()` - 18 edges
6. `get_settings()` - 17 edges
7. `Hospital` - 17 edges
8. `seed_catalog()` - 17 edges
9. `compilerOptions` - 16 edges
10. `BookingError` - 15 edges

## Surprising Connections (you probably didn't know these)
- `output_guard.check` --conceptually_related_to--> `search_packages()`  [INFERRED]
  docs/superpowers/plans/2026-11-21-plan-2-loi-an-toan.md → backend/app/services/catalog.py
- `seed_slots()` --references--> `VN_TZ`  [EXTRACTED]
  backend/scripts/seed.py → docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md
- `list_available_slots()` --references--> `VN_TZ`  [EXTRACTED]
  backend/app/services/booking.py → docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md
- `Quy tắc múi giờ Asia/Ho_Chi_Minh, lưu UTC` --rationale_for--> `list_available_slots()`  [EXTRACTED]
  docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md → backend/app/services/booking.py
- `Chống đặt trùng và khóa hàng FOR UPDATE` --rationale_for--> `create_booking()`  [EXTRACTED]
  docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md → backend/app/services/booking.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Assistant safety pipeline (safety_check, check_symptoms, output_guard, PII masking)** — docs_superpowers_specs_2026_11_21_mediflow_ai_design_safety_check, docs_superpowers_specs_2026_11_21_mediflow_ai_design_check_symptoms, docs_superpowers_specs_2026_11_21_mediflow_ai_design_output_guard, docs_superpowers_specs_2026_11_21_mediflow_ai_design_pii_masking [EXTRACTED 0.95]
- **Project guidance docs (CLAUDE.md, README, spec)** — claude_md, readme, docs_superpowers_specs_2026_11_21_mediflow_ai_design [INFERRED 0.75]
- **Ba module lõi an toàn (cờ đỏ, PII, kiểm tra đầu ra)** — backend_app_safety_red_flags_detect, backend_app_safety_pii_redact, backend_app_safety_output_guard_check [EXTRACTED 1.00]
- **Luồng đặt/hủy lịch** — backend_app_services_booking_list_available_slots, backend_app_services_booking_create_booking, backend_app_services_booking_cancel_booking, backend_app_services_prep_prep_checklist [EXTRACTED 1.00]
- **Pipeline seed dữ liệu mô phỏng** — backend_scripts_seed_seed_catalog, backend_scripts_seed_seed_slots, backend_scripts_seed_seed_users [EXTRACTED 1.00]
- **Pipeline trợ lý LangGraph an toàn** — docs_superpowers_plans_2026_11_21_plan_4_agent_langgraph_graph, docs_superpowers_plans_2026_11_21_plan_4_agent_red_flag_two_layer, docs_superpowers_plans_2026_11_21_plan_4_agent_output_guard_node, docs_superpowers_plans_2026_11_21_plan_4_agent_agent_tools [EXTRACTED 1.00]
- **Luồng xử lý lỗi giao diện (api, 422, safeNext, ErrorState)** — docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_lib_api, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_vi_422_handler, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_lib_nav, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_pagestate [INFERRED 0.85]
- **Kiến trúc deploy Neon + Render + Vercel** — docs_superpowers_plans_2026_11_21_plan_6_deploy_neon, docs_superpowers_plans_2026_11_21_plan_6_deploy_render, docs_superpowers_plans_2026_11_21_plan_6_deploy_vercel [EXTRACTED 1.00]
- **Cụm giao diện trợ lý nổi** — docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_assistantprovider, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_assistantwidget, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_blockview, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_usepagecontext [EXTRACTED 1.00]
- **Starter template SVG assets in frontend/public** — frontend_public_file, frontend_public_globe, frontend_public_next, frontend_public_vercel, frontend_public_window [INFERRED 0.75]

## Communities (58 total, 35 thin omitted)

### Community 0 - "Cấu hình và migration DB"
Cohesion: 0.05
Nodes (23): run_migrations_offline(), run_migrations_online(), _url(), downgrade(), upgrade(), get_settings(), Settings, get_db() (+15 more)

### Community 1 - "API đặt lịch của khách"
Cohesion: 0.09
Nodes (19): book(), cancel(), checklist(), my_bookings(), raise_http(), all_bookings(), cancel(), health() (+11 more)

### Community 2 - "API bệnh viện và gói khám"
Cohesion: 0.08
Nodes (23): hospital_detail(), list_hospitals(), compare_packages(), package_detail(), package_slots(), search_packages(), BookingIn, ChecklistItem (+15 more)

### Community 3 - "Cấu hình khung Next.js"
Cohesion: 0.05
Nodes (44): geistMono, geistSans, metadata, eslintConfig, nextConfig, dependencies, cn@^0.5.2, date-fns@^4.4.0 (+36 more)

### Community 4 - "API đăng nhập"
Cohesion: 0.08
Nodes (18): login(), logout(), me(), register(), clear_auth_cookie(), create_access_token(), current_user(), hash_password() (+10 more)

### Community 5 - "Service đặt lịch và test"
Cohesion: 0.11
Nodes (33): TimeSlot, create_booking(), book(), _client_for(), consultant_client(), customer(), customer_client(), first_slot() (+25 more)

### Community 6 - "Kế hoạch 3: giao diện đặt khám"
Cohesion: 0.05
Nodes (38): Kế hoạch 3: Giao diện đặt khám, AuthProvider / useAuth, Trang đặt lịch /book/[code], Trang danh mục (home, hospitals, packages, compare), CompareTable, Trang tư vấn viên /consultant, lib/api.ts (api(), ApiError), lib/constants.ts (DISCLAIMER, TAG_LABEL, CITY_OPTIONS) (+30 more)

### Community 7 - "Models và danh mục"
Cohesion: 0.11
Nodes (19): Base, Hospital, Package, _pk(), ServiceItem, _active_packages(), list_hospitals(), search_packages() (+11 more)

### Community 8 - "Spec và quy tắc dự án"
Cohesion: 0.07
Nodes (33): CLAUDE.md project notes, Implementation plans 1-6 status table, MediFlow-AI Design Spec, Agent tools (search_packages, compare_packages, get_available_slots, prep tools), FastAPI REST API under /api, Floating AI assistant (LangGraph agent), Booking concurrency rule (SELECT FOR UPDATE), check_symptoms tool (red-flag layer 2) (+25 more)

### Community 9 - "Kế hoạch 5: trợ lý giao diện"
Cohesion: 0.10
Nodes (19): Kế hoạch 5: Trợ lý AI trên giao diện, lib/assistant.ts (pure logic), AssistantProvider (React context), AssistantWidget, BlockView, BookingConfirm, Tab Cảnh báo cờ đỏ của tư vấn viên, InlineLogin (LoginForm/RegisterForm compact) (+11 more)

### Community 10 - "Cấu hình shadcn"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 11 - "Cấu hình TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 12 - "Docker Postgres"
Cohesion: 0.12
Nodes (16): environment, healthcheck, image, ports, volumes, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER (+8 more)

### Community 13 - "Test danh mục"
Cohesion: 0.16
Nodes (4): test_city_filter_common_spellings(), test_city_filter_ignores_accents_and_case(), test_compare_errors(), test_inactive_package_hidden()

### Community 14 - "UI: Badge và Tabs"
Cohesion: 0.19
Nodes (7): Badge(), badgeVariants, TabsList(), tabsListVariants, class-variance-authority@^0.7.1, class-variance-authority, cn

### Community 15 - "UI: Select"
Cohesion: 0.20
Nodes (5): SelectContent(), SelectScrollDownButton(), SelectScrollUpButton(), lucide-react@^1.77.0, lucide-react

### Community 16 - "Kế hoạch 2: lõi an toàn"
Cohesion: 0.22
Nodes (10): output_guard.check, find_amounts, find_package_codes, pii.redact, red_flags.detect, red_flags.evaluate_codes, red_flags.yaml (luật cờ đỏ), normalize_vi (+2 more)

### Community 17 - "UI: Dialog"
Cohesion: 0.22
Nodes (4): DialogContent(), DialogFooter(), DialogOverlay(), DialogPortal()

### Community 18 - "UI: Sheet"
Cohesion: 0.22
Nodes (3): SheetContent(), SheetOverlay(), SheetPortal()

### Community 21 - "UI: Button và Calendar"
Cohesion: 0.73
Nodes (4): Button(), buttonVariants, Calendar(), CalendarDayButton()

### Community 22 - "UI: Input"
Cohesion: 0.33
Nodes (4): @base-ui/react@^1.9.0, react@19.3.0, @base-ui/react, react

### Community 23 - "Icon mẫu Next.js"
Cohesion: 0.40
Nodes (6): Default create-next-app starter assets, File icon (document page outline, grey), Globe icon (circle with meridians), Next.js wordmark logo (black), Vercel triangle logo (white), Browser window icon (grey)

### Community 24 - "Kế hoạch 1 và nền tảng"
Cohesion: 0.50
Nodes (3): Kế hoạch 1: Khởi tạo dự án + nền backend, Monorepo backend FastAPI + frontend Next.js, Kế hoạch 2: Lõi an toàn

## Knowledge Gaps
- **48 isolated node(s):** `mediflow-backend`, `VMEC-15 assignment (Basic scope only)`, `PII masking (pii.py)`, `Booking concurrency rule (SELECT FOR UPDATE)`, `Simulated seed data (hospitals ALP/BET/GAM, packages)` (+43 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 314 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Package` connect `Models và danh mục` to `API đặt lịch của khách`, `API bệnh viện và gói khám`, `Test danh mục`, `Service đặt lịch và test`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `User` (e.g. with `login()` and `current_user()`) actually correct?**
  _`User` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `mediflow-backend`, `VMEC-15 assignment (Basic scope only)`, `PII masking (pii.py)` to the rest of the system?**
  _48 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Cấu hình và migration DB` be split into smaller, more focused modules?**
  _Cohesion score 0.0506558118498417 - nodes in this community are weakly interconnected._
- **Why does `User` connect `API đăng nhập` to `API đặt lịch của khách`, `Service đặt lịch và test`, `Models và danh mục`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Package` (e.g. with `PackageDetailOut` and `PackageSummary`) actually correct?**
  _`Package` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Should `API đặt lịch của khách` be split into smaller, more focused modules?**
  _Cohesion score 0.09049773755656108 - nodes in this community are weakly interconnected._