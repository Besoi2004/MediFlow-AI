---
type: "query"
date: "2026-11-21T13:49:58.017272+00:00"
question: "Why does Package connect the catalog models community to booking API, catalog API, catalog tests and booking service?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["Package", "search_packages", "get_package", "PackageSummary", "PackageDetailOut", "list_bookings", "prep_checklist", "seed_catalog"]
---

# Q: Why does Package connect the catalog models community to booking API, catalog API, catalog tests and booking service?

## Answer

Expanded from original query via vocab: [package, packages]. Started at node Package (backend/app/models.py L90, degree 24, community Models va danh muc). Neighbors span 5 communities: API benh vien va goi kham (schemas PackageSummary.of L95, PackageDetailOut.of L122, catalog.get_package L65, prep.prep_checklist L9); Models va danh muc (catalog.search_packages L48, _active_packages L32, seed_catalog L53, test_seed); Service dat lich va test (test_booking past_booking_id L83, test_booking_rejections L149); API dat lich cua khach (booking.list_bookings L130, booking.py import L9); Test danh muc (test_inactive_package_hidden L44). Package bridges because it is the single shared ORM record for price, eligibility (gender_scope, age range), tags and items that catalog, schemas, prep, booking, seed and tests all read; each consumer group clusters around its own module. Bypass check: no raw SQL against the packages table; only Alembic migration d642840cb377 repeats the columns (by design); the main.py hit is packages.router (false positive). Gap: no doc node links to Package, so spec rules such as price-from-DB are not connected to the model in the graph.

## Outcome

- Signal: useful

## Source Nodes

- Package
- search_packages
- get_package
- PackageSummary
- PackageDetailOut
- list_bookings
- prep_checklist
- seed_catalog