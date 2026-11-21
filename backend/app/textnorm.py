"""Chuẩn hóa chữ tiếng Việt (bỏ dấu) và múi giờ Việt Nam."""
import re
import unicodedata
from zoneinfo import ZoneInfo

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


def slug_vi(text: str) -> str:
    """'TP. Hồ Chí Minh' -> 'tp-ho-chi-minh': chữ thường, bỏ dấu, đ→d, ký tự khác chữ/số thành '-'."""
    s = unicodedata.normalize("NFD", text.lower().replace("đ", "d"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
