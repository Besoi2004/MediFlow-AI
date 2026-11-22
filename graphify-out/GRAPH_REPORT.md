# Graph Report - MediFlow-AI  (2026-11-22)

## Corpus Check
- 9 files · ~50,845 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 849 nodes · 1589 edges · 65 communities (34 shown, 31 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- API đặt lịch của khách
- Service danh mục
- Fixture test (conftest)
- Guard đầu ra
- Che PII
- Phát hiện cờ đỏ
- Spec và quy tắc dự án
- Phân quyền và router API
- Cấu hình ESLint và devDependencies
- Cấu hình shadcn
- Mật khẩu và seed tài khoản
- UI: Dialog
- Cấu hình TypeScript
- Cấu trúc red_flags.yaml
- Bộ câu mẫu cờ đỏ
- Docker Postgres
- UI: Badge và Tabs
- API đăng nhập
- Schemas API
- Test danh mục
- Dependencies frontend
- UI: Sheet
- Kế hoạch 6: deploy
- Layout gốc Next.js
- UI: Card
- UI: Select
- Models dữ liệu
- Kế hoạch 5: trợ lý giao diện
- Kế hoạch 3: trang danh mục
- Schema đăng ký
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
2. `check()` - 25 edges
3. `User` - 24 edges
4. `TimeSlot` - 21 edges
5. `Booking` - 20 edges
6. `create_booking()` - 20 edges
7. `seed_catalog()` - 18 edges
8. `Hospital` - 17 edges
9. `get_settings()` - 17 edges
10. `compilerOptions` - 16 edges

## Surprising Connections (you probably didn't know these)
- `list_available_slots()` --references--> `VN_TZ`  [EXTRACTED]
  backend/app/services/booking.py → docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md
- `Package as the single shared ORM record for price, eligibility, tags and items` --rationale_for--> `Package`  [EXTRACTED]
  graphify-out/memory/query_20261121_134958_edf6de8f_why_does_package_connect_the_catalog_models_commun.md → backend/app/models.py
- `Query: how create_booking connects Package, TimeSlot and Booking` --references--> `Package`  [EXTRACTED]
  graphify-out/memory/query_20261121_135555_6d5ba0b5_how_does_create_booking_connect_package__timeslot.md → backend/app/models.py
- `Chống đặt trùng và khóa hàng FOR UPDATE` --rationale_for--> `create_booking()`  [EXTRACTED]
  docs/superpowers/plans/2026-11-21-plan-1-khoi-tao-va-backend.md → backend/app/services/booking.py
- `Query: how create_booking connects Package, TimeSlot and Booking` --references--> `get_package()`  [EXTRACTED]
  graphify-out/memory/query_20261121_135555_6d5ba0b5_how_does_create_booking_connect_package__timeslot.md → backend/app/services/catalog.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cụm giao diện trợ lý nổi** — docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_assistantprovider, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_assistantwidget, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_blockview, docs_superpowers_plans_2026_11_21_plan_5_tro_ly_tren_giao_dien_usepagecontext [EXTRACTED 1.00]
- **Kiến trúc deploy Neon + Render + Vercel** — docs_superpowers_plans_2026_11_21_plan_6_deploy_neon, docs_superpowers_plans_2026_11_21_plan_6_deploy_render, docs_superpowers_plans_2026_11_21_plan_6_deploy_vercel [EXTRACTED 1.00]
- **Luồng đặt/hủy lịch** — backend_app_services_booking_list_available_slots, backend_app_services_booking_create_booking, backend_app_services_booking_cancel_booking, backend_app_services_prep_prep_checklist [EXTRACTED 1.00]
- **Pipeline seed dữ liệu mô phỏng** — backend_scripts_seed_seed_catalog, backend_scripts_seed_seed_slots, backend_scripts_seed_seed_users [EXTRACTED 1.00]
- **Ba module lõi an toàn (cờ đỏ, PII, kiểm tra đầu ra)** — backend_app_safety_red_flags_detect, backend_app_safety_pii_redact, backend_app_safety_output_guard_check [EXTRACTED 1.00]
- **Starter template SVG assets in frontend/public** — frontend_public_file, frontend_public_globe, frontend_public_next, frontend_public_vercel, frontend_public_window [INFERRED 0.75]
- **Luồng xử lý lỗi giao diện (api, 422, safeNext, ErrorState)** — docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_lib_api, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_vi_422_handler, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_lib_nav, docs_superpowers_plans_2026_11_21_plan_3_giao_dien_dat_kham_pagestate [INFERRED 0.85]
- **Pipeline trợ lý LangGraph an toàn** — docs_superpowers_plans_2026_11_21_plan_4_agent_langgraph_graph, docs_superpowers_plans_2026_11_21_plan_4_agent_red_flag_two_layer, docs_superpowers_plans_2026_11_21_plan_4_agent_output_guard_node, docs_superpowers_plans_2026_11_21_plan_4_agent_agent_tools [EXTRACTED 1.00]
- **Assistant safety pipeline (safety_check, check_symptoms, output_guard, PII masking)** — docs_superpowers_specs_2026_11_21_mediflow_ai_design_safety_check, docs_superpowers_specs_2026_11_21_mediflow_ai_design_check_symptoms, docs_superpowers_specs_2026_11_21_mediflow_ai_design_output_guard, docs_superpowers_specs_2026_11_21_mediflow_ai_design_pii_masking [EXTRACTED 0.95]

## Communities (65 total, 31 thin omitted)

### Community 0 - "API đặt lịch của khách"
Cohesion: 0.06
Nodes (51): book(), cancel(), checklist(), my_bookings(), raise_http(), all_bookings(), cancel(), Booking (+43 more)

### Community 1 - "Service danh mục"
Cohesion: 0.07
Nodes (34): hospital_detail(), list_hospitals(), compare_packages(), package_detail(), package_slots(), search_packages(), Hospital, Package (+26 more)

### Community 2 - "Fixture test (conftest)"
Cohesion: 0.05
Nodes (23): run_migrations_offline(), run_migrations_online(), _url(), downgrade(), upgrade(), get_settings(), Settings, get_db() (+15 more)

### Community 3 - "Guard đầu ra"
Cohesion: 0.07
Nodes (39): _after_last_connector(), _amount_patterns(), check(), _contains(), _decimal(), find_amounts(), find_package_codes(), _forbidden_sentences() (+31 more)

### Community 4 - "Che PII"
Cohesion: 0.06
Nodes (31): _flags(), _marks_optional(), _name_end(), redact(), _redact_names(), accented_negations, connectors, coordinators (+23 more)

### Community 5 - "Phát hiện cờ đỏ"
Cohesion: 0.06
Nodes (39): _clause_before(), detect(), evaluate_codes(), Grammar, _grammar(), single_words(), Hit, _list_goes_on() (+31 more)

### Community 6 - "Spec và quy tắc dự án"
Cohesion: 0.06
Nodes (33): CLAUDE.md project notes, User rules (simple Vietnamese commit messages, no Claude attribution, never print .env), MediFlow-AI Design Spec, Agent tools (search_packages, compare_packages, get_available_slots, prep tools), FastAPI REST API under /api, Floating AI assistant (LangGraph agent), Booking concurrency rule (SELECT FOR UPDATE), check_symptoms tool (red-flag layer 2) (+25 more)

### Community 7 - "Phân quyền và router API"
Cohesion: 0.14
Nodes (4): current_user(), optional_user(), require_role(), health()

### Community 8 - "Cấu hình ESLint và devDependencies"
Cohesion: 0.12
Nodes (21): eslintConfig, devDependencies, eslint@^9, eslint-config-next@16.4.6, tailwindcss@4.3.3, @tailwindcss/turbopack@4.3.3, @types/node@^20, @types/react@^19 (+13 more)

### Community 9 - "Cấu hình shadcn"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 10 - "Mật khẩu và seed tài khoản"
Cohesion: 0.17
Nodes (8): hash_password(), verify_password(), User, main(), seed_users(), test_register_sets_httponly_cookie_and_customer_role(), test_seed_users_creates_consultant(), test_seed_users_never_promotes_existing_customer()

### Community 11 - "UI: Dialog"
Cohesion: 0.18
Nodes (10): Button(), buttonVariants, Calendar(), CalendarDayButton(), DialogContent(), DialogFooter(), DialogOverlay(), DialogPortal() (+2 more)

### Community 12 - "Cấu hình TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 13 - "Cấu trúc red_flags.yaml"
Cohesion: 0.12
Nodes (17): exact, except, phrases, exact, except, not_after, phrases, still_if (+9 more)

### Community 14 - "Bộ câu mẫu cờ đỏ"
Cohesion: 0.12
Nodes (16): co_giat, dau_bung_du_doi, dau_keo_dai, dau_nguc, dot_quy, ho_keo_dai, kho_tho, khoi_u (+8 more)

### Community 15 - "Docker Postgres"
Cohesion: 0.12
Nodes (16): environment, healthcheck, image, ports, volumes, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER (+8 more)

### Community 16 - "UI: Badge và Tabs"
Cohesion: 0.15
Nodes (9): Badge(), badgeVariants, TabsList(), tabsListVariants, @base-ui/react@^1.9.0, class-variance-authority@^0.7.1, @base-ui/react, class-variance-authority (+1 more)

### Community 17 - "API đăng nhập"
Cohesion: 0.23
Nodes (7): login(), logout(), me(), register(), clear_auth_cookie(), create_access_token(), set_auth_cookie()

### Community 18 - "Schemas API"
Cohesion: 0.22
Nodes (7): BookingIn, ChecklistItem, ItemOut, LoginIn, SlotOut, UserOut, prep_checklist()

### Community 19 - "Test danh mục"
Cohesion: 0.16
Nodes (4): test_city_filter_common_spellings(), test_city_filter_ignores_accents_and_case(), test_compare_errors(), test_inactive_package_hidden()

### Community 20 - "Dependencies frontend"
Cohesion: 0.17
Nodes (12): dependencies, cn@^0.5.2, date-fns@^4.4.0, react-day-picker@^10.0.2, react-dom@19.3.0, shadcn@^4.23.0, tw-animate-css@^1.4.0, date-fns (+4 more)

### Community 21 - "UI: Sheet"
Cohesion: 0.22
Nodes (3): SheetContent(), SheetOverlay(), SheetPortal()

### Community 22 - "Kế hoạch 6: deploy"
Cohesion: 0.27
Nodes (7): Kế hoạch 6: Deploy lên cloud, backend/Dockerfile, Neon Postgres + pgvector, Render Web Service (Docker backend), Gợi ý chờ máy chủ khởi động (PageSkeleton), scripts/smoke.py, Vercel (Next.js frontend)

### Community 23 - "Layout gốc Next.js"
Cohesion: 0.20
Nodes (6): geistMono, geistSans, metadata, nextConfig, next@16.4.6, next

### Community 25 - "UI: Select"
Cohesion: 0.24
Nodes (3): SelectContent(), SelectScrollDownButton(), SelectScrollUpButton()

### Community 27 - "Models dữ liệu"
Cohesion: 0.29
Nodes (3): Base, _pk(), ServiceItem

### Community 28 - "Kế hoạch 5: trợ lý giao diện"
Cohesion: 0.32
Nodes (7): Kế hoạch 5: Trợ lý AI trên giao diện, lib/assistant.ts (pure logic), AssistantProvider (React context), AssistantWidget, resolveConversation, shouldAutoOpen / safeStorage, usePageContext

### Community 29 - "Kế hoạch 3: trang danh mục"
Cohesion: 0.29
Nodes (7): Trang danh mục (home, hospitals, packages, compare), CompareTable, lib/format.ts (formatVnd, formatDateTimeVN, toggleCode...), PackageCard, proxy.ts (Next 16 route guard), API /api/conversations, Cookie khách ký HMAC (guest.py)

### Community 31 - "Bảng trạng thái các kế hoạch"
Cohesion: 0.40
Nodes (5): Implementation plans 1-6 status table (plans 1-2 done), Kế hoạch 1: Khởi tạo dự án + nền backend, Monorepo backend FastAPI + frontend Next.js, Kế hoạch 2: Lõi an toàn, Kế hoạch 4: Trợ lý AI ở backend

### Community 32 - "Kế hoạch 3: đặt lịch"
Cohesion: 0.33
Nodes (5): Kế hoạch 3: Giao diện đặt khám, Trang đặt lịch /book/[code], lib/api.ts (api(), ApiError), SlotPicker, Handler 422 tiếng Việt (errors[].field/message)

### Community 33 - "Kế hoạch 3: đăng nhập và tư vấn viên"
Cohesion: 0.33
Nodes (6): AuthProvider / useAuth, Trang tư vấn viên /consultant, lib/nav.ts safeNext, Trang đăng nhập và đăng ký, Review Focus kế hoạch 3 (lỗi mạng, 401, 409, múi giờ, 422), SiteHeader

### Community 34 - "Icon mẫu Next.js"
Cohesion: 0.40
Nodes (6): Default create-next-app starter assets, File icon (document page outline, grey), Globe icon (circle with meridians), Next.js wordmark logo (black), Vercel triangle logo (white), Browser window icon (grey)

### Community 35 - "Script npm frontend"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 36 - "Kế hoạch 5: block và cảnh báo"
Cohesion: 0.50
Nodes (3): BlockView, Tab Cảnh báo cờ đỏ của tư vấn viên, UrgentAlert (Gọi 115)

## Knowledge Gaps
- **43 isolated node(s):** `mediflow-backend`, `Spike thử Gemini (tool call tiếng Việt, JSON, embedding)`, `CompareTable`, `Trang tư vấn viên /consultant`, `lib/format.ts (formatVnd, formatDateTimeVN, toggleCode...)` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 368 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Đồ thị LangGraph safety_check→agent⇄tools→output_guard` connect `Phát hiện cờ đỏ` to `Guard đầu ra`, `Bảng trạng thái các kế hoạch`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Package` (e.g. with `PackageDetailOut` and `PackageSummary`) actually correct?**
  _`Package` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `mediflow-backend`, `Spike thử Gemini (tool call tiếng Việt, JSON, embedding)`, `CompareTable` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `API đặt lịch của khách` be split into smaller, more focused modules?**
  _Cohesion score 0.059644322845417236 - nodes in this community are weakly interconnected._
- **Why does `Implementation plans 1-6 status table (plans 1-2 done)` connect `Bảng trạng thái các kế hoạch` to `Kế hoạch 3: đặt lịch`, `Kế hoạch 5: trợ lý giao diện`, `Spec và quy tắc dự án`, `Kế hoạch 6: deploy`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `User` (e.g. with `login()` and `current_user()`) actually correct?**
  _`User` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `Service danh mục` be split into smaller, more focused modules?**
  _Cohesion score 0.06521739130434782 - nodes in this community are weakly interconnected._