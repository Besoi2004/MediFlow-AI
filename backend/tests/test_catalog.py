import pytest
from sqlalchemy import update

from app.models import Package


def test_filter_male_35(client, catalog):
    codes = {p["code"] for p in client.get("/api/packages", params={"gender": "male", "age": 35}).json()}
    assert {"ALP-TQNAM", "BET-TQNAM", "ALP-CB01"} <= codes
    assert not codes & {"ALP-TQNU", "BET-UTNU", "ALP-CAOTUOI", "ALP-TIM"}


@pytest.mark.parametrize("city", ["Hà Nội", "ha noi", "HÀ NỘI"])
def test_city_filter_ignores_accents_and_case(client, catalog, city):  # Review Focus 1
    res = client.get("/api/packages", params={"city": city}).json()
    assert res and all(p["code"].startswith("ALP-") for p in res)


def test_hospital_list_city_filter(client, catalog):
    res = client.get("/api/hospitals", params={"city": "da nang"}).json()
    assert [h["code"] for h in res] == ["GAM"]


def test_tag_and_price(client, catalog):
    res = client.get("/api/packages", params={"tag": "tim-mach", "price_max": 5_000_000}).json()
    assert [p["code"] for p in res] == ["GAM-TIM"]


def test_sorted_by_price(client, catalog):
    prices = [p["price_vnd"] for p in client.get("/api/packages").json()]
    assert len(prices) == 15 and prices == sorted(prices)


def test_inactive_package_hidden(client, catalog, db):
    db.execute(update(Package).where(Package.code == "ALP-CB01").values(active=False))
    db.commit()
    assert "ALP-CB01" not in {p["code"] for p in client.get("/api/packages").json()}
    assert client.get("/api/packages/ALP-CB01").status_code == 404


def test_compare_union_and_order(client, catalog):
    out = client.get("/api/packages/compare", params={"codes": "GAM-CB01,ALP-CB01"}).json()
    assert [p["code"] for p in out["packages"]] == ["GAM-CB01", "ALP-CB01"]
    assert any(r["included"] == [False, True] for r in out["rows"])
    assert all(len(r["included"]) == 2 for r in out["rows"])


@pytest.mark.parametrize("codes,status", [
    ("ALP-CB01", 400),
    ("ALP-CB01,BET-CB01,GAM-CB01,ALP-TIM", 400),
    ("ALP-CB01,KHONG-CO", 404),
])
def test_compare_errors(client, catalog, codes, status):
    assert client.get("/api/packages/compare", params={"codes": codes}).status_code == status


def test_hospital_detail(client, catalog):
    h = client.get("/api/hospitals/GAM").json()
    assert h["name"].endswith("(mô phỏng)") and h["packages"]
    assert all(p["code"].startswith("GAM-") for p in h["packages"])
    assert client.get("/api/hospitals/XYZ").status_code == 404


def test_package_detail_has_items_with_prep(client, catalog):
    d = client.get("/api/packages/ALP-CB01").json()
    assert d["hospital_name"] == "Bệnh viện Alpha (mô phỏng)"
    assert any(i["code"] == "XN-DUONG" and i["fasting_hours"] == 8 for i in d["items"])


def test_negative_age_rejected(client, catalog):
    assert client.get("/api/packages", params={"age": -1}).status_code == 422
