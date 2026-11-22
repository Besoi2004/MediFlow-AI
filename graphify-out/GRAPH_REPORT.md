# Graph Report - MediFlow-AI  (2026-11-22)

## Corpus Check
- 11 files · ~42,188 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 745 nodes · 1414 edges · 59 communities (29 shown, 30 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 106 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- API và dịch vụ danh mục
- Lõi an toàn: cờ đỏ, PII, guard
- API đặt lịch của khách
- Service đặt lịch và test
- Spec và quy tắc dự án
- Các kế hoạch triển khai
- Kế hoạch 3: giao diện đặt khám
- Models và băm mật khẩu
- Cấu hình ESLint và devDependencies
- Cấu hình shadcn
- UI: Button, Calendar, Dialog
- Cấu hình TypeScript
- Fixture test (conftest)
- Cấu hình backend (.env)
- Script thử Gemini
- Docker Postgres
- UI: Badge, Tabs, Input
- API đăng nhập
- Xác thực và phân quyền
- Test danh mục
- Dependencies frontend
- UI: Sheet
- Layout gốc Next.js
- UI: Card
- UI: Select
- Migration đầu và test schema
- Cấu trúc red_flags.yaml
- Alembic env
- Icon mẫu Next.js
- Script npm frontend
- Lịch hẹn và checklist (UI)
- Giới hạn ngày giờ VN
- Mẫu trang Next.js
- Stack và deploy
- pyproject backend

## God Nodes (most connected - your core abstractions)
1. `Package` - 27 edges
2. `User` - 24 edges
3. `TimeSlot` - 21 edges
4. `Booking` - 20 edges
5. `create_booking()` - 20 edges
6. `seed_catalog()` - 18 edges
7. `Hospital` - 17 edges
8. `get_settings()` - 17 edges
9. `compilerOptions` - 16 edges
10. `detect()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `seed_slots()` --references--> `VN_TZ`  [EXTRACTED]
  backend/scripts/seed.py → docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md
- `Query: how create_booking connects Package, TimeSlot and Booking` --references--> `Booking`  [EXTRACTED]
  graphify-out/memory/query_20261121_135555_6d5ba0b5_how_does_create_booking_connect_package__timeslot.md → backend/app/models.py
- `Package as the single shared ORM record for price, eligibility, tags and items` --rationale_for--> `Package`  [EXTRACTED]
  graphify-out/memory/query_20261121_134958_edf6de8f_why_does_package_connect_the_catalog_models_commun.md → backend/app/models.py
- `Query: how create_booking connects Package, TimeSlot and Booking` --references--> `Package`  [EXTRACTED]
  graphify-out/memory/query_20261121_135555_6d5ba0b5_how_does_create_booking_connect_package__timeslot.md → backend/app/models.py
- `Chống đặt trùng và khóa hàng FOR UPDATE` --rationale_for--> `create_booking()`  [EXTRACTED]
  docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md → backend/app/services/booking.py

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

## Communities (59 total, 30 thin omitted)

### Community 0 - "API và dịch vụ danh mục"
Cohesion: 0.06
Nodes (38): hospital_detail(), list_hospitals(), compare_packages(), package_detail(), package_slots(), search_packages(), Hospital, Package (+30 more)

### Community 1 - "Lõi an toàn: cờ đỏ, PII, guard"
Cohesion: 0.06
Nodes (39): check(), find_amounts(), find_package_codes(), _forbidden_clauses(), _is_claim(), redact(), detect(), evaluate_codes() (+31 more)

### Community 2 - "API đặt lịch của khách"
Cohesion: 0.09
Nodes (19): book(), cancel(), checklist(), my_bookings(), raise_http(), all_bookings(), cancel(), health() (+11 more)

### Community 3 - "Service đặt lịch và test"
Cohesion: 0.11
Nodes (35): TimeSlot, create_booking(), _lock(), book(), _client_for(), consultant_client(), customer(), customer_client() (+27 more)

### Community 4 - "Spec và quy tắc dự án"
Cohesion: 0.06
Nodes (33): CLAUDE.md project notes, User rules (simple Vietnamese commit messages, no Claude attribution, never print .env), MediFlow-AI Design Spec, Agent tools (search_packages, compare_packages, get_available_slots, prep tools), FastAPI REST API under /api, Floating AI assistant (LangGraph agent), Booking concurrency rule (SELECT FOR UPDATE), check_symptoms tool (red-flag layer 2) (+25 more)

### Community 5 - "Các kế hoạch triển khai"
Cohesion: 0.07
Nodes (29): Implementation plans 1-6 status table (plans 1-2 done), Kế hoạch 1: Khởi tạo dự án + nền backend, Monorepo backend FastAPI + frontend Next.js, Kế hoạch 2: Lõi an toàn, Kế hoạch 3: Giao diện đặt khám, Trang đặt lịch /book/[code], lib/api.ts (api(), ApiError), SlotPicker (+21 more)

### Community 6 - "Kế hoạch 3: giao diện đặt khám"
Cohesion: 0.06
Nodes (32): AuthProvider / useAuth, Trang danh mục (home, hospitals, packages, compare), CompareTable, Trang tư vấn viên /consultant, lib/constants.ts (DISCLAIMER, TAG_LABEL, CITY_OPTIONS), lib/format.ts (formatVnd, formatDateTimeVN, toggleCode...), lib/nav.ts safeNext, Trang đăng nhập và đăng ký (+24 more)

### Community 7 - "Models và băm mật khẩu"
Cohesion: 0.12
Nodes (11): hash_password(), verify_password(), Base, _pk(), ServiceItem, User, main(), seed_users() (+3 more)

### Community 8 - "Cấu hình ESLint và devDependencies"
Cohesion: 0.12
Nodes (21): eslintConfig, devDependencies, eslint@^9, eslint-config-next@16.4.6, tailwindcss@4.3.3, @tailwindcss/turbopack@4.3.3, @types/node@^20, @types/react@^19 (+13 more)

### Community 9 - "Cấu hình shadcn"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 10 - "UI: Button, Calendar, Dialog"
Cohesion: 0.18
Nodes (10): Button(), buttonVariants, Calendar(), CalendarDayButton(), DialogContent(), DialogFooter(), DialogOverlay(), DialogPortal() (+2 more)

### Community 11 - "Cấu hình TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 12 - "Fixture test (conftest)"
Cohesion: 0.16
Nodes (7): catalog(), check_test_url(), client(), db(), engine(), settings_with_seed_passwords(), _test_url()

### Community 13 - "Cấu hình backend (.env)"
Cohesion: 0.15
Nodes (4): Settings, get_db(), test_refuses_test_db_equal_to_dev_db(), test_rejects_placeholder_or_short_secrets()

### Community 14 - "Script thử Gemini"
Cohesion: 0.14
Nodes (5): get_available_slots(), Intake, main(), search_packages(), Spike thử Gemini (tool call tiếng Việt, JSON, embedding)

### Community 15 - "Docker Postgres"
Cohesion: 0.12
Nodes (16): environment, healthcheck, image, ports, volumes, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER (+8 more)

### Community 16 - "UI: Badge, Tabs, Input"
Cohesion: 0.15
Nodes (9): Badge(), badgeVariants, TabsList(), tabsListVariants, @base-ui/react@^1.9.0, class-variance-authority@^0.7.1, @base-ui/react, class-variance-authority (+1 more)

### Community 17 - "API đăng nhập"
Cohesion: 0.22
Nodes (8): login(), logout(), me(), register(), clear_auth_cookie(), create_access_token(), set_auth_cookie(), LoginIn

### Community 18 - "Xác thực và phân quyền"
Cohesion: 0.19
Nodes (3): current_user(), optional_user(), require_role()

### Community 19 - "Test danh mục"
Cohesion: 0.16
Nodes (4): test_city_filter_common_spellings(), test_city_filter_ignores_accents_and_case(), test_compare_errors(), test_inactive_package_hidden()

### Community 20 - "Dependencies frontend"
Cohesion: 0.17
Nodes (12): dependencies, cn@^0.5.2, date-fns@^4.4.0, react-day-picker@^10.0.2, react-dom@19.3.0, shadcn@^4.23.0, tw-animate-css@^1.4.0, date-fns (+4 more)

### Community 21 - "UI: Sheet"
Cohesion: 0.22
Nodes (3): SheetContent(), SheetOverlay(), SheetPortal()

### Community 22 - "Layout gốc Next.js"
Cohesion: 0.20
Nodes (6): geistMono, geistSans, metadata, nextConfig, next@16.4.6, next

### Community 24 - "UI: Select"
Cohesion: 0.24
Nodes (3): SelectContent(), SelectScrollDownButton(), SelectScrollUpButton()

### Community 26 - "Migration đầu và test schema"
Cohesion: 0.36
Nodes (3): downgrade(), upgrade(), test_migration_creates_business_tables()

### Community 27 - "Cấu trúc red_flags.yaml"
Cohesion: 0.25
Nodes (7): negations, rules, exact, id, phrases, severity, symptom_code

### Community 28 - "Alembic env"
Cohesion: 0.53
Nodes (4): run_migrations_offline(), run_migrations_online(), _url(), get_settings()

### Community 29 - "Icon mẫu Next.js"
Cohesion: 0.40
Nodes (6): Default create-next-app starter assets, File icon (document page outline, grey), Globe icon (circle with meridians), Next.js wordmark logo (black), Vercel triangle logo (white), Browser window icon (grey)

### Community 30 - "Script npm frontend"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

## Knowledge Gaps
- **43 isolated node(s):** `mediflow-backend`, `Spike thử Gemini (tool call tiếng Việt, JSON, embedding)`, `Xử lý phủ định trong 3 token trước cụm triệu chứng`, `File icon (document page outline, grey)`, `Globe icon (circle with meridians)` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 318 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Package` connect `API và dịch vụ danh mục` to `Test danh mục`, `API đặt lịch của khách`, `Service đặt lịch và test`, `Models và băm mật khẩu`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Package` (e.g. with `PackageDetailOut` and `PackageSummary`) actually correct?**
  _`Package` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `mediflow-backend`, `Spike thử Gemini (tool call tiếng Việt, JSON, embedding)`, `Xử lý phủ định trong 3 token trước cụm triệu chứng` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `API và dịch vụ danh mục` be split into smaller, more focused modules?**
  _Cohesion score 0.05740740740740741 - nodes in this community are weakly interconnected._
- **Why does `Implementation plans 1-6 status table (plans 1-2 done)` connect `Các kế hoạch triển khai` to `Spec và quy tắc dự án`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `User` (e.g. with `login()` and `current_user()`) actually correct?**
  _`User` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `Lõi an toàn: cờ đỏ, PII, guard` be split into smaller, more focused modules?**
  _Cohesion score 0.06386946386946386 - nodes in this community are weakly interconnected._