"""Chuẩn hóa chữ tiếng Việt (bỏ dấu) và múi giờ Việt Nam."""
import re
import unicodedata
from zoneinfo import ZoneInfo

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


def normalize_vi(text: str) -> str:
    """'ĐAU NGỰC!!!' -> 'dau nguc': chữ thường, bỏ dấu, đ→d, ký tự khác chữ/số thành một dấu cách."""
    s = unicodedata.normalize("NFD", text.lower().replace("đ", "d"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def slug_vi(text: str) -> str:
    """'TP. Hồ Chí Minh' -> 'tp-ho-chi-minh'."""
    return normalize_vi(text).replace(" ", "-")


def words_vi(text: str) -> list[str]:
    """Tách từ, chữ thường, giữ dấu: 'Tự TỬ!' -> ['tự', 'tử']."""
    return re.findall(r"[^\W_]+", unicodedata.normalize("NFC", text.lower()))


def has_vi_marks(text: str) -> bool:
    """Có dấu tiếng Việt không: 'đau ngực' có, 'dau nguc' không."""
    return "đ" in text.lower() or any(unicodedata.category(c) == "Mn" for c in unicodedata.normalize("NFD", text))


_CITY_PREFIXES = ("thanh-pho-", "tp-", "tinh-")
_CITY_ALIASES = {
    "hcm": "ho-chi-minh", "tphcm": "ho-chi-minh", "sai-gon": "ho-chi-minh", "saigon": "ho-chi-minh",
    "hanoi": "ha-noi", "danang": "da-nang",
}


def city_key(text: str) -> str:
    """Khóa so khớp tỉnh/thành: 'TP.HCM', 'Sài Gòn', 'Thành phố Hồ Chí Minh' -> 'ho-chi-minh'."""
    s = slug_vi(text)
    for prefix in _CITY_PREFIXES:
        if s.startswith(prefix):
            s = s.removeprefix(prefix)
            break
    return _CITY_ALIASES.get(s, s)
