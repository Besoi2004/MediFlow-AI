# Graph Report - MediFlow-AI  (2026-11-22)

## Corpus Check
- 2 files · ~50,986 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 851 nodes · 1595 edges · 66 communities (36 shown, 30 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- API đặt lịch của khách
- API bệnh viện và gói khám
- Guard đầu ra
- Che PII
- Phát hiện cờ đỏ
- Spec và quy tắc dự án
- Cấu hình và kết nối DB
- Phân quyền và router API
- Models dữ liệu
- Cấu hình ESLint và devDependencies
- Cấu hình shadcn
- UI: Dialog
- Cấu hình TypeScript
- API đăng nhập
- Cấu trúc red_flags.yaml
- Bộ câu mẫu cờ đỏ
- Docker Postgres
- UI: Badge và Tabs
- Mật khẩu và seed tài khoản
- Thử Gemini (spike)
- Test danh mục
- Dependencies frontend
- UI: Sheet
- Kế hoạch 6: deploy
- Layout gốc Next.js
- UI: Card
- UI: Select
- Migration và test schema
- Kế hoạch 5: trợ lý giao diện
- Kế hoạch 3: trang danh mục
- Alembic env
- Bảng trạng thái các kế hoạch
- Kế hoạch 3: đặt lịch
- Kế hoạch 3: đăng nhập và tư vấn viên
- Icon mẫu Next.js
- Script npm frontend
- Kế hoạch 5: block và cảnh báo
- Kế hoạch 5: xác nhận đặt lịch
- Lịch hẹn và checklist (UI)
- Giới hạn ngày giờ VN
- Mẫu trang Next.js
- Stack và deploy
- pyproject backend

## God Nodes (most connected - your core abstractions)
1. `Package` - 27 edges
2. `check()` - 27 edges
3. `User` - 24 edges
4. `TimeSlot` - 21 edges
5. `Booking` - 20 edges
6. `create_booking()` - 20 edges
7. `seed_catalog()` - 18 edges
8. `Hospital` - 17 edges
9. `get_settings()` - 17 edges
10. `compilerOptions` - 16 edges

## Surprising Connections (you probably didn't know these)
- `seed_slots()` --references--> `VN_TZ`  [EXTRACTED]
  backend/scripts/seed.py → docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md
- `Query: how create_booking connects Package, TimeSlot and Booking` --references--> `TimeSlot`  [EXTRACTED]
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

## Communities (66 total, 30 thin omitted)

### Community 0 - "API đặt lịch của khách"
Cohesion: 0.06
Nodes (52): book(), cancel(), checklist(), my_bookings(), raise_http(), all_bookings(), cancel(), Booking (+44 more)

### Community 1 - "API bệnh viện và gói khám"
Cohesion: 0.06
Nodes (31): hospital_detail(), list_hospitals(), compare_packages(), package_detail(), package_slots(), search_packages(), Package, ChecklistItem (+23 more)

### Community 2 - "Guard đầu ra"
Cohesion: 0.07
Nodes (41): _after_last_connector(), _amount_patterns(), check(), _contains(), _decimal(), find_amounts(), find_package_codes(), _forbidden_sentences() (+33 more)

### Community 3 - "Che PII"
Cohesion: 0.06
Nodes (31): _flags(), _marks_optional(), _name_end(), redact(), _redact_names(), accented_negations, connectors, coordinators (+23 more)

### Community 4 - "Phát hiện cờ đỏ"
Cohesion: 0.06
Nodes (39): _clause_before(), detect(), evaluate_codes(), Grammar, _grammar(), single_words(), Hit, _list_goes_on() (+31 more)

### Community 5 - "Spec và quy tắc dự án"
Cohesion: 0.06
Nodes (33): CLAUDE.md project notes, User rules (simple Vietnamese commit messages, no Claude attribution, never print .env), MediFlow-AI Design Spec, Agent tools (search_packages, compare_packages, get_available_slots, prep tools), FastAPI REST API under /api, Floating AI assistant (LangGraph agent), Booking concurrency rule (SELECT FOR UPDATE), check_symptoms tool (red-flag layer 2) (+25 more)

### Community 6 - "Cấu hình và kết nối DB"
Cohesion: 0.09
Nodes (11): Settings, get_db(), catalog(), check_test_url(), client(), db(), engine(), settings_with_seed_passwords() (+3 more)

### Community 7 - "Phân quyền và router API"
Cohesion: 0.11
Nodes (4): current_user(), optional_user(), require_role(), health()

### Community 8 - "Models dữ liệu"
Cohesion: 0.17
Nodes (13): Base, Hospital, _pk(), ServiceItem, TimeSlot, _load(), main(), seed_catalog() (+5 more)

### Community 9 - "Cấu hình ESLint và devDependencies"
Cohesion: 0.12
Nodes (21): eslintConfig, devDependencies, eslint@^9, eslint-config-next@16.4.6, tailwindcss@4.3.3, @tailwindcss/turbopack@4.3.3, @types/node@^20, @types/react@^19 (+13 more)

### Community 10 - "Cấu hình shadcn"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 11 - "UI: Dialog"
Cohesion: 0.18
Nodes (10): Button(), buttonVariants, Calendar(), CalendarDayButton(), DialogContent(), DialogFooter(), DialogOverlay(), DialogPortal() (+2 more)

### Community 12 - "Cấu hình TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 13 - "API đăng nhập"
Cohesion: 0.21
Nodes (9): login(), logout(), me(), register(), clear_auth_cookie(), create_access_token(), hash_password(), set_auth_cookie() (+1 more)

### Community 14 - "Cấu trúc red_flags.yaml"
Cohesion: 0.12
Nodes (17): exact, except, phrases, exact, except, not_after, phrases, still_if (+9 more)

### Community 15 - "Bộ câu mẫu cờ đỏ"
Cohesion: 0.12
Nodes (16): co_giat, dau_bung_du_doi, dau_keo_dai, dau_nguc, dot_quy, ho_keo_dai, kho_tho, khoi_u (+8 more)

### Community 16 - "Docker Postgres"
Cohesion: 0.12
Nodes (16): environment, healthcheck, image, ports, volumes, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER (+8 more)

### Community 17 - "UI: Badge và Tabs"
Cohesion: 0.15
Nodes (9): Badge(), badgeVariants, TabsList(), tabsListVariants, @base-ui/react@^1.9.0, class-variance-authority@^0.7.1, @base-ui/react, class-variance-authority (+1 more)

### Community 18 - "Mật khẩu và seed tài khoản"
Cohesion: 0.20
Nodes (6): verify_password(), User, seed_users(), test_register_sets_httponly_cookie_and_customer_role(), test_seed_users_creates_consultant(), test_seed_users_never_promotes_existing_customer()

### Community 19 - "Thử Gemini (spike)"
Cohesion: 0.15
Nodes (5): get_available_slots(), Intake, main(), search_packages(), Spike thử Gemini (tool call tiếng Việt, JSON, embedding)

### Community 20 - "Test danh mục"
Cohesion: 0.16
Nodes (4): test_city_filter_common_spellings(), test_city_filter_ignores_accents_and_case(), test_compare_errors(), test_inactive_package_hidden()

### Community 21 - "Dependencies frontend"
Cohesion: 0.17
Nodes (12): dependencies, cn@^0.5.2, date-fns@^4.4.0, react-day-picker@^10.0.2, react-dom@19.3.0, shadcn@^4.23.0, tw-animate-css@^1.4.0, date-fns (+4 more)

### Community 22 - "UI: Sheet"
Cohesion: 0.22
Nodes (3): SheetContent(), SheetOverlay(), SheetPortal()

### Community 23 - "Kế hoạch 6: deploy"
Cohesion: 0.27
Nodes (7): Kế hoạch 6: Deploy lên cloud, backend/Dockerfile, Neon Postgres + pgvector, Render Web Service (Docker backend), Gợi ý chờ máy chủ khởi động (PageSkeleton), scripts/smoke.py, Vercel (Next.js frontend)

### Community 24 - "Layout gốc Next.js"
Cohesion: 0.20
Nodes (6): geistMono, geistSans, metadata, nextConfig, next@16.4.6, next

### Community 26 - "UI: Select"
Cohesion: 0.24
Nodes (3): SelectContent(), SelectScrollDownButton(), SelectScrollUpButton()

### Community 28 - "Migration và test schema"
Cohesion: 0.36
Nodes (3): downgrade(), upgrade(), test_migration_creates_business_tables()

### Community 29 - "Kế hoạch 5: trợ lý giao diện"
Cohesion: 0.32
Nodes (7): Kế hoạch 5: Trợ lý AI trên giao diện, lib/assistant.ts (pure logic), AssistantProvider (React context), AssistantWidget, resolveConversation, shouldAutoOpen / safeStorage, usePageContext

### Community 30 - "Kế hoạch 3: trang danh mục"
Cohesion: 0.29
Nodes (7): Trang danh mục (home, hospitals, packages, compare), CompareTable, lib/format.ts (formatVnd, formatDateTimeVN, toggleCode...), PackageCard, proxy.ts (Next 16 route guard), API /api/conversations, Cookie khách ký HMAC (guest.py)

### Community 31 - "Alembic env"
Cohesion: 0.53
Nodes (4): run_migrations_offline(), run_migrations_online(), _url(), get_settings()

### Community 32 - "Bảng trạng thái các kế hoạch"
Cohesion: 0.40
Nodes (5): Implementation plans 1-6 status table (plans 1-2 done), Kế hoạch 1: Khởi tạo dự án + nền backend, Monorepo backend FastAPI + frontend Next.js, Kế hoạch 2: Lõi an toàn, Kế hoạch 4: Trợ lý AI ở backend

### Community 33 - "Kế hoạch 3: đặt lịch"
Cohesion: 0.33
Nodes (5): Kế hoạch 3: Giao diện đặt khám, Trang đặt lịch /book/[code], lib/api.ts (api(), ApiError), SlotPicker, Handler 422 tiếng Việt (errors[].field/message)

### Community 34 - "Kế hoạch 3: đăng nhập và tư vấn viên"
Cohesion: 0.33
Nodes (6): AuthProvider / useAuth, Trang tư vấn viên /consultant, lib/nav.ts safeNext, Trang đăng nhập và đăng ký, Review Focus kế hoạch 3 (lỗi mạng, 401, 409, múi giờ, 422), SiteHeader

### Community 35 - "Icon mẫu Next.js"
Cohesion: 0.40
Nodes (6): Default create-next-app starter assets, File icon (document page outline, grey), Globe icon (circle with meridians), Next.js wordmark logo (black), Vercel triangle logo (white), Browser window icon (grey)

### Community 36 - "Script npm frontend"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 37 - "Kế hoạch 5: block và cảnh báo"
Cohesion: 0.50
Nodes (3): BlockView, Tab Cảnh báo cờ đỏ của tư vấn viên, UrgentAlert (Gọi 115)

## Knowledge Gaps
- **43 isolated node(s):** `mediflow-backend`, `Spike thử Gemini (tool call tiếng Việt, JSON, embedding)`, `backend/Dockerfile`, `resolveConversation`, `usePageContext` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 368 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Đồ thị LangGraph safety_check→agent⇄tools→output_guard` connect `Phát hiện cờ đỏ` to `Bảng trạng thái các kế hoạch`, `Guard đầu ra`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Package` (e.g. with `PackageDetailOut` and `PackageSummary`) actually correct?**
  _`Package` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `mediflow-backend`, `Spike thử Gemini (tool call tiếng Việt, JSON, embedding)`, `backend/Dockerfile` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `API đặt lịch của khách` be split into smaller, more focused modules?**
  _Cohesion score 0.0560875512995896 - nodes in this community are weakly interconnected._
- **Why does `Implementation plans 1-6 status table (plans 1-2 done)` connect `Bảng trạng thái các kế hoạch` to `Kế hoạch 3: đặt lịch`, `Kế hoạch 5: trợ lý giao diện`, `Spec và quy tắc dự án`, `Kế hoạch 6: deploy`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `User` (e.g. with `login()` and `current_user()`) actually correct?**
  _`User` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `API bệnh viện và gói khám` be split into smaller, more focused modules?**
  _Cohesion score 0.061381074168797956 - nodes in this community are weakly interconnected._