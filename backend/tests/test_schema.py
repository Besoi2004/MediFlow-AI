import sqlalchemy as sa


def test_migration_creates_business_tables(db):
    names = set(sa.inspect(db.get_bind()).get_table_names())
    assert {"users", "hospitals", "packages", "service_items",
            "package_items", "time_slots", "bookings"} <= names


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}
