---
type: "query"
date: "2026-11-21T13:55:55.931002+00:00"
question: "How does create_booking connect Package, TimeSlot and Booking, and does anything bypass it?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["create_booking", "get_package", "_lock", "Booking", "TimeSlot", "book", "test_last_spot_concurrency"]
---

# Q: How does create_booking connect Package, TimeSlot and Booking, and does anything bypass it?

## Answer

Expanded from original query via vocab: [create, booking, slot, lock, update]. Node create_booking() (backend/app/services/booking.py L53, degree 18, community Service dat lich va test). Callers: API book() (api/bookings.py L37) and tests test_booking_rejections L142, test_last_spot_concurrency/worker L164, test_create_booking_reads_fresh_slot_under_lock L183, test_cancel_booking_reads_fresh_status_under_lock L191. Callees: get_package (catalog L62) for active package + price, _lock (L65) = SELECT FOR UPDATE with populate_existing on TimeSlot, _now (L70), BookingError (L64), Booking model (models L84). Rationale edge from plan 1: chong dat trung va khoa hang FOR UPDATE. Package and TimeSlot meet here: price_snapshot_vnd copies package.price_vnd and booked_count += 1 on the locked slot. Bypass check: production code never writes booked_count or constructs Booking outside services/booking.py (create/cancel); the only direct Booking() is the test fixture past_booking_id (test_booking.py L84), deliberate because create_booking rejects past slots. Plan 4 tool create_booking is specified to call this service, so the lock rule stays in one place.

## Outcome

- Signal: useful

## Source Nodes

- create_booking
- get_package
- _lock
- Booking
- TimeSlot
- book
- test_last_spot_concurrency