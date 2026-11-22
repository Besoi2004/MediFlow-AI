import time
from pathlib import Path

import pytest
import yaml

from app.safety import red_flags
from app.safety.pii import redact
from app.safety.red_flags import detect


@pytest.mark.parametrize("raw,expected", [
    ("sđt mình 0901234567 nhé", "sđt mình [SĐT] nhé"),
    ("gọi 0901 234 567", "gọi [SĐT]"), ("gọi 0901.234.567", "gọi [SĐT]"),       # Review Focus 3
    ("gọi 0901-234-567", "gọi [SĐT]"), ("số +84 901234567", "số [SĐT]"),
    ("bàn 02838123456", "bàn [SĐT]"), ("bàn (028) 3812 3456", "bàn [SĐT]"), ("gọi (0901234567)", "gọi ([SĐT])"),
    ("mail an.nguyen@gmail.com", "mail [EMAIL]"),
    ("CCCD 001090012345", "CCCD [CCCD]"),
    ("số (+84) 901 234 567", "số [SĐT]"), ("số (+84)901234567", "số [SĐT]"), ("bàn (0236) 3812 345", "bàn [SĐT]"),
    ("gọi 0901  234  567", "gọi [SĐT]"), ("gọi 0901 - 234 - 567", "gọi [SĐT]"),
    ("số +840901234567", "số [SĐT]"), ("số 0084 901 234 567", "số [SĐT]"),
    ("CCCD 001 090 012 345", "CCCD [CCCD]"), ("CCCD 0010 9001 2345", "CCCD [CCCD]"),
    ("cccd: 001.090.012.345", "cccd: [CCCD]"),
    # tên tự giới thiệu, CMND có từ dẫn
    ("tên tôi là Nguyễn Văn An, 35 tuổi", "tên tôi là [TÊN], 35 tuổi"),
    ("Tôi tên An, muốn khám tổng quát", "Tôi tên [TÊN], muốn khám tổng quát"),
    ("mẹ tôi tên là Trần Thị Bình", "mẹ tôi tên là [TÊN]"), ("tên tôi là lan 30 tuổi", "tên tôi là [TÊN] 30 tuổi"),
    ("tôi tên hoa muốn khám", "tôi tên [TÊN] muốn khám"),
    # tên viết thường không được nuốt triệu chứng theo sau
    ("tôi tên lan đau ngực", "tôi tên [TÊN] đau ngực"), ("tên tôi là lan khó thở quá", "tên tôi là [TÊN] khó thở quá"),
    ("tôi tên hoa co giật", "tôi tên [TÊN] co giật"),
    ("CMND 012345678", "CMND [CMND]"), ("số chứng minh: 012 345 678", "số chứng minh: [CMND]"),
])
def test_redacts(raw, expected):
    assert redact(raw) == expected


@pytest.mark.parametrize("text", ["gói 1.200.000đ", "ngân sách 4000000", "khám ngày 21/11/2026 lúc 07:00",  # Review Focus 3
    "tôi 35 tuổi", "mã gói ALP-CB01", "giá 120000000 đồng",
    "đặt lịch 05-12-2026 08:00", "ngày 05.12.2026 08:00",  # ngày kèm giờ đủ 9 chữ số sau số 0 đầu
    "ngày 05.12.2026 07.30", "2026-12-05 08:00", "giá 2.000.000 - 3.000.000", "10.000.000.000đ",  # không phải CCCD
    "Gói này tên là gì?", "bạn tên gì vậy", "tên gói là ALP-CB01", "tên tôi là gì nhỉ"])
def test_keeps_non_pii(text):
    assert redact(text) == text


def test_redact_never_hides_red_flags():
    # Kế hoạch 4 chạy detect() trên bản đã che, nên che tên không được làm mất cảnh báo nào
    data = yaml.safe_load(Path(red_flags.__file__).with_name("red_flags.yaml").read_text(encoding="utf-8"))
    for rule in data["rules"]:
        for phrase in rule.get("phrases", []) + rule.get("exact", []):
            text = f"tôi tên lan {phrase}"
            before = {h.rule_id for h in detect(text)}
            assert before <= {h.rule_id for h in detect(redact(text))}, text


def test_long_text_is_fast():
    # regex email từng chạy bậc hai: 50.000 ký tự mất 15 giây
    start = time.perf_counter()
    redact("a" * 30_000)
    assert time.perf_counter() - start < 1.0


def test_redacts_several_in_one_message():
    out = redact("0901234567 hoặc 0912 345 678, mail a@b.vn")
    assert out == "[SĐT] hoặc [SĐT], mail [EMAIL]"
