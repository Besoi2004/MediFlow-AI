"""Kiểm tra câu trả lời của LLM: mã gói, giá, chẩn đoán (Kế hoạch 2)."""
import re
import unicodedata
from decimal import Decimal

from app.textnorm import normalize_vi

DISCLAIMER = "Thông tin chỉ mang tính tham khảo, vui lòng tham vấn bác sĩ để cá nhân hóa tầm soát."
SAFE_FALLBACK = (
    "Xin lỗi, mình chưa trả lời chính xác được. Bạn xem thông tin gói và giá trong các thẻ bên dưới, "
    "hoặc hỏi lại giúp mình nhé."
)

FORBIDDEN_PHRASES = (
    "ban bi benh", "ban mac benh", "chan doan la", "chan doan cua ban", "ban bi ung thu",
    "nen uong thuoc", "hay uong thuoc", "ke don", "lieu dung", "ban nen lam them xet nghiem",
)
# Có một từ này trong 3 từ ngay trước (cùng vế câu) thì không phải lời khẳng định:
# "không thể kê đơn" là từ chối, "nếu bạn bị bệnh X" là giả định.
_NOT_A_CLAIM = {"khong", "chua", "neu"}
_CLAUSE_BREAK = re.compile(r"[,.;:!?\n]+")

# shortcut: bắt cả tên xét nghiệm dạng "HPV-16"; nếu LLM hay viết vậy thì chỉ bắt mã nằm trong [...]
_PACKAGE_CODE = re.compile(r"(?<![\w-])[A-Za-z]{3}-[A-Za-z0-9]{2,}")

_NUM = r"(?<![\d.,])(\d+(?:[.,]\d+)?)\s*"
# Thử theo thứ tự; đoạn đã lấy được xóa đi để không đếm lại.
# shortcut: "2 triệu 500 nghìn" thành hai số 2.000.000 và 500.000; LLM được dặn ghi giá đúng như tool trả.
_AMOUNT_PATTERNS = (
    (re.compile(_NUM + r"(?:triệu|trieu|tr|củ)(?!\w)"), lambda n: Decimal(n.replace(",", ".")) * 1_000_000),
    (re.compile(_NUM + r"(?:k|nghìn|nghin|ngàn)(?!\w)"), lambda n: Decimal(n.replace(",", ".")) * 1_000),
    (re.compile(r"(?<![\d.,])(\d{1,3}(?:[.,]\d{3})+)(?![.,]?\d)"), lambda n: int(re.sub(r"\D", "", n))),
    (re.compile(r"(?<![\d.,])(\d{4,})\s*(?:đồng|dong|vnđ|vnd|đ|₫)(?!\w)"), int),
)


def find_package_codes(text: str) -> set[str]:
    return {code.upper() for code in _PACKAGE_CODE.findall(text)}


def find_amounts(text: str) -> set[int]:
    s = unicodedata.normalize("NFC", text.lower())
    found: set[int] = set()
    for pattern, parse in _AMOUNT_PATTERNS:
        found |= {int(parse(n)) for n in pattern.findall(s)}
        s = pattern.sub(lambda m: " " * len(m[0]), s)
    return found


def _is_claim(words: list[str], phrase: list[str]) -> bool:
    n = len(phrase)
    return any(words[i:i + n] == phrase and not _NOT_A_CLAIM & set(words[max(0, i - 3):i])
               for i in range(len(words) - n + 1))


def _forbidden_clauses(text: str) -> list[str]:
    return [clause.strip() for clause in _CLAUSE_BREAK.split(text)
            if any(_is_claim(normalize_vi(clause).split(), p.split()) for p in FORBIDDEN_PHRASES)]


def check(text: str, *, known_codes: set[str], allowed_amounts: set[int]) -> list[str]:
    """Danh sách lỗi bằng tiếng Việt; rỗng là đạt."""
    problems = [f"Mã gói không có trong danh mục: {c}" for c in sorted(find_package_codes(text) - known_codes)]
    problems += [f"Số tiền không khớp giá gói nào: {n}" for n in sorted(find_amounts(text) - allowed_amounts)]
    problems += [f"Câu có dạng chẩn đoán hoặc kê đơn: '{c}'" for c in _forbidden_clauses(text)]
    return problems
