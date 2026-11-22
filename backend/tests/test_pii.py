import pytest

from app.safety.pii import redact


@pytest.mark.parametrize("raw,expected", [
    ("sđt mình 0901234567 nhé", "sđt mình [SĐT] nhé"),
    ("gọi 0901 234 567", "gọi [SĐT]"), ("gọi 0901.234.567", "gọi [SĐT]"),       # Review Focus 3
    ("gọi 0901-234-567", "gọi [SĐT]"), ("số +84 901234567", "số [SĐT]"),
    ("bàn 02838123456", "bàn [SĐT]"), ("bàn (028) 3812 3456", "bàn [SĐT]"), ("gọi (0901234567)", "gọi ([SĐT])"),
    ("mail an.nguyen@gmail.com", "mail [EMAIL]"),
    ("CCCD 001090012345", "CCCD [CCCD]"),
])
def test_redacts(raw, expected):
    assert redact(raw) == expected


@pytest.mark.parametrize("text", ["gói 1.200.000đ", "ngân sách 4000000", "khám ngày 21/11/2026 lúc 07:00",  # Review Focus 3
    "tôi 35 tuổi", "mã gói ALP-CB01", "giá 120000000 đồng",
    "đặt lịch 05-12-2026 08:00", "ngày 05.12.2026 08:00"])  # ngày kèm giờ đủ 9 chữ số sau số 0 đầu
def test_keeps_non_pii(text):
    assert redact(text) == text


def test_redacts_several_in_one_message():
    out = redact("0901234567 hoặc 0912 345 678, mail a@b.vn")
    assert out == "[SĐT] hoặc [SĐT], mail [EMAIL]"
