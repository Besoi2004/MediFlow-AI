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
_FORBIDDEN_WORDS = tuple(p.split() for p in FORBIDDEN_PHRASES)
# Có một từ này trong 3 từ ngay trước (cùng vế câu) thì không phải lời khẳng định:
# "không thể kê đơn" là từ chối, "nếu bạn bị bệnh X" là giả định.
_NOT_A_CLAIM = {"khong", "chua", "neu"}
# Từ nối chặn tác dụng của các từ trên: "chưa rõ nhưng bạn bị bệnh X" vẫn là lời khẳng định.
_CONNECTORS = {"nhung", "ma", "nen", "thi"}
_CLAUSE_BREAK = re.compile(r"[,.;:!?\n]+")

_CODE = r"[A-Za-z]{3}-[A-Za-z0-9]{2,}"
_PACKAGE_CODE = re.compile(rf"(?<![\w-]){_CODE}")
_BRACKETED_CODE = re.compile(rf"\[({_CODE})\]")

_NUM = r"(?<![\d.,])(\d+(?:[.,]\d+)?)\s*"
_MILLION = r"(?:triệu|trieu|tr|củ)"
_THOUSAND = r"(?:k|nghìn|nghin|ngàn)"


def _decimal(n: str) -> Decimal:
    return Decimal(n.replace(",", "."))


def _compound(m: re.Match[str]) -> Decimal | int:
    """'1tr5' = 1.500.000; '2 triệu 50 nghìn' = 2.050.000."""
    if m[3]:
        return int(m[1]) * 1_000_000 + int(m[2]) * 1_000
    return Decimal(f"{m[1]}.{m[2]}") * 1_000_000


# Thử theo thứ tự; đoạn đã lấy được xóa đi để không đếm lại.
_AMOUNT_PATTERNS = (
    (re.compile(rf"(?<![\d.,])(\d+)\s*{_MILLION}\s*(\d{{1,3}})(\s*{_THOUSAND})?(?!\w)"), _compound),
    (re.compile(_NUM + _MILLION + r"(?!\w)"), lambda m: _decimal(m[1]) * 1_000_000),
    (re.compile(_NUM + _THOUSAND + r"(?!\w)"), lambda m: _decimal(m[1]) * 1_000),
    (re.compile(r"(?<![\d.,])(\d{1,3}(?:[.,]\d{3})+)(?![.,]?\d)"), lambda m: int(re.sub(r"\D", "", m[1]))),
    (re.compile(r"(?<![\d.,])(\d{4,})\s*(?:đồng|dong|vnđ|vnd|đ|₫)(?!\w)"), lambda m: int(m[1])),
)


def find_package_codes(text: str) -> set[str]:
    return {code.upper() for code in _PACKAGE_CODE.findall(text)}


def find_amounts(text: str) -> set[int]:
    s = unicodedata.normalize("NFC", text.lower())
    found: set[int] = set()
    for pattern, parse in _AMOUNT_PATTERNS:
        found |= {int(parse(m)) for m in pattern.finditer(s)}
        s = pattern.sub(lambda m: " " * len(m[0]), s)
    return found


def _is_claim(words: list[str], phrase: list[str]) -> bool:
    n = len(phrase)
    for i in range(len(words) - n + 1):
        if words[i:i + n] == phrase:
            before = words[max(0, i - 3):i]
            cuts = [k for k, w in enumerate(before) if w in _CONNECTORS]
            if not _NOT_A_CLAIM & set(before[cuts[-1] + 1:] if cuts else before):
                return True
    return False


def _forbidden_clauses(text: str) -> list[str]:
    clauses = []
    for clause in _CLAUSE_BREAK.split(text):
        words = normalize_vi(clause).split()
        if any(_is_claim(words, phrase) for phrase in _FORBIDDEN_WORDS):
            clauses.append(clause.strip())
    return clauses


def check(text: str, *, known_codes: set[str], allowed_amounts: set[int]) -> list[str]:
    """Danh sách lỗi bằng tiếng Việt; rỗng là đạt."""
    # Mã trong [...] luôn bị kiểm; mã không có ngoặc chỉ bị kiểm khi tiền tố là bệnh viện có thật,
    # để tên xét nghiệm như "HPV-DNA" hay tag "tim-mach" không bị coi là mã gói.
    hospitals = {c.split("-")[0] for c in known_codes}
    codes = {c.upper() for c in _BRACKETED_CODE.findall(text)}
    codes |= {c for c in find_package_codes(text) if c.split("-")[0] in hospitals}
    problems = [f"Mã gói không có trong danh mục: {c}" for c in sorted(codes - known_codes)]
    problems += [f"Số tiền không khớp giá gói nào: {n}" for n in sorted(find_amounts(text) - allowed_amounts)]
    problems += [f"Câu có dạng chẩn đoán hoặc kê đơn: '{c}'" for c in _forbidden_clauses(text)]
    return problems
