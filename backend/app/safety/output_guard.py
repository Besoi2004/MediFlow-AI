"""Kiểm tra câu trả lời của LLM: mã gói, giá, chẩn đoán (Kế hoạch 2)."""
import re
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal

from app.textnorm import has_vi_marks, normalize_vi, words_vi

DISCLAIMER = "Thông tin chỉ mang tính tham khảo, vui lòng tham vấn bác sĩ để cá nhân hóa tầm soát."
SAFE_FALLBACK = (
    "Xin lỗi, mình chưa trả lời chính xác được. Bạn xem thông tin gói và giá trong các thẻ bên dưới, "
    "hoặc hỏi lại giúp mình nhé."
)

# Câu trả lời của LLM có dấu, nên so trên chữ giữ dấu ("hãy uống thuốc" khác "hay uống thuốc");
# văn bản không dấu thì so trên chữ đã bỏ dấu.
# Kê đơn, chẩn đoán, đòi thêm xét nghiệm: bỏ qua nếu trước đó trong cùng câu có _MARKERS (lời từ chối, giả định),
# hoặc cùng vế có "bác sĩ" ("Việc kê đơn thuốc cần bác sĩ thăm khám").
FORBIDDEN_PHRASES = ("kê đơn", "liều dùng", "chẩn đoán là", "chẩn đoán của bạn",
                     "nên uống thuốc", "hãy uống thuốc", "nên dùng thuốc", "hãy dùng thuốc")
_ADVISE = ("nên", "cần", "hãy", "khuyên bạn", "khuyên")
_EXTRA_TESTS = ("làm thêm xét nghiệm", "làm xét nghiệm thêm", "xét nghiệm thêm")
# Khẳng định bệnh "bạn (đang/có thể) bị/mắc <bệnh>": bỏ qua nếu 3 từ ngay trước có _MARKERS, và bỏ qua câu hỏi.
_DISEASES = ("bệnh", "ung thư", "tiểu đường", "đái tháo đường", "cao huyết áp", "tăng huyết áp", "huyết áp cao",
             "mỡ máu", "rối loạn mỡ máu", "gan nhiễm mỡ", "viêm gan", "viêm", "gút", "gout", "suy thận", "sỏi thận",
             "thiếu máu", "loãng xương", "u")
_HEDGES = ("đang", "đã", "có thể", "có lẽ")
_MARKERS = ("không", "chưa", "nếu", "khi", "trường hợp")
_CONNECTORS = ("nhưng", "mà", "nên", "thì")  # chặn tác dụng của _MARKERS: "chưa rõ nhưng bạn bị bệnh X"
_DOSAGE = re.compile(r"\d+(?:[.,]\d+)?\s*(?:mg|mcg|µg)\b(?!\s*/)")  # "500mg"; "100 mg/dL" là chỉ số
_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+|\n+")
_CLAUSE_BREAK = re.compile(r"[,;:]+")
_BULLET = re.compile(r"\n[ \t]*(?:[-*•+]|\d+[.)])[ \t]+")  # nối dòng gạch đầu dòng vào câu dẫn "Mình không thể:"

_PACKAGE_CODE = re.compile(r"(?<![\w-])[A-Za-z]{3}-[A-Za-z0-9]{2,}")
_BRACKETED_CODE = re.compile(r"\[([A-Za-z]+-[A-Za-z0-9]+)\]")


@dataclass(frozen=True)
class _Grammar:
    action: re.Pattern[str]
    assertion: re.Pattern[str]
    markers: tuple[tuple[str, ...], ...]
    connectors: frozenset[str]
    doctor: tuple[str, ...]


def _grammar(accented: bool) -> _Grammar:
    def form(x: str) -> str:
        return x if accented else normalize_vi(x)

    def alt(items: tuple[str, ...]) -> str:
        return "|".join(re.escape(form(x)) for x in sorted(items, key=len, reverse=True))

    return _Grammar(
        action=re.compile(rf"\b(?:{alt(FORBIDDEN_PHRASES)}|(?:{alt(_ADVISE)}) (?:{alt(_EXTRA_TESTS)}))\b"),
        assertion=re.compile(rf"\b{form('bạn')} (?:(?:{alt(_HEDGES)}) )?(?:{alt(('bị', 'mắc'))}) (?:{alt(_DISEASES)})\b"),
        markers=tuple(tuple(form(x).split()) for x in _MARKERS),
        connectors=frozenset(form(x) for x in _CONNECTORS),
        doctor=tuple(form("bác sĩ").split()),
    )


_GRAMMAR = {True: _grammar(True), False: _grammar(False)}


def _decimal(n: str) -> Decimal:
    return Decimal(n.replace(",", "."))


def _amount_patterns(loose: bool) -> list[tuple[re.Pattern[str], Callable[[re.Match[str]], list[Decimal | int]]]]:
    # LLM không dùng "củ" để chỉ tiền nhưng có viết "1 củ khoai"; tin nhắn người dùng thì hiểu rộng
    million = r"(?:triệu|trieu|tr|củ|cu)" if loose else r"(?:triệu|trieu|tr|củ(?!\s*[^\W\d_]))"
    thousand = r"(?:k|nghìn|nghin|ngàn|ngan)" if loose else r"(?:k|nghìn|nghin|ngàn)"
    currency = r"(?:đồng|dong|vnđ|vnd|đ|d|₫)" if loose else r"(?:đồng|dong|vnđ|vnd|đ|₫)"
    num = r"(?<![\d.,])(\d+(?:[.,]\d+)?)\s*"

    def compound(m: re.Match[str]) -> list[Decimal | int]:
        """'1tr5' = 1.500.000; '2 triệu 50 nghìn' = 2.050.000; loose: '5 triệu 2 người' có thể là 5 triệu."""
        value = int(m[1]) * 1_000_000 + int(m[2]) * 1_000 if m[3] else Decimal(f"{m[1]}.{m[2]}") * 1_000_000
        return [value, int(m[1]) * 1_000_000] if loose else [value]

    def grouped(m: re.Match[str]) -> list[Decimal | int]:
        """'1.200.000'; không kèm đơn vị mà nhỏ hơn 100.000 thì là số đếm ('10.000 bước')."""
        value = int(re.sub(r"\D", "", m[1]))
        return [value] if loose or m[2] or value >= 100_000 else []

    patterns = [
        (rf"(?<![\d.,])(\d+)\s*{million}\s*(?:rưỡi|ruoi)(?!\w)", lambda m: [(int(m[1]) + Decimal("0.5")) * 1_000_000]),
        (rf"(?<![\d.,])(\d+)\s*(?:trăm|tram)\s*{thousand}(?!\w)", lambda m: [int(m[1]) * 100_000]),
        (rf"(?<![\d.,])(\d+)\s*{million}\s*(\d{{1,3}})(\s*{thousand})?(?!\w)", compound),
        (num + million + r"(?!\w)", lambda m: [_decimal(m[1]) * 1_000_000]),
        (num + thousand + r"(?!\w)", lambda m: [_decimal(m[1]) * 1_000]),
        (rf"(?<![\d.,])(\d{{1,3}}(?:[.,]\d{{3}})+)(?![.,]?\d)(\s*{currency}(?!\w))?", grouped),
        (rf"(?<![\d.,])(\d{{4,}})\s*{currency}(?!\w)", lambda m: [int(m[1])]),
    ]
    if loose:
        patterns.append((r"(?<![\d.,])(\d{5,})(?![.,]?\d)", lambda m: [int(m[1])]))
    return [(re.compile(p), parse) for p, parse in patterns]


_STRICT_AMOUNTS, _LOOSE_AMOUNTS = _amount_patterns(False), _amount_patterns(True)


def find_package_codes(text: str) -> set[str]:
    return {code.upper() for code in _PACKAGE_CODE.findall(text)}


def find_amounts(text: str, *, loose: bool = False) -> set[int]:
    """Số tiền VND trong text. Thử theo thứ tự; đoạn đã lấy được xóa đi để không đếm lại.

    loose=True cho tin nhắn của người dùng (Kế hoạch 4 lấy ngân sách từ đó): hiểu thêm "4 cu", "500 ngan",
    "1200000d", số trần "4000000", và lấy cả hai cách hiểu khi mơ hồ. Hiểu rộng ở đây chỉ làm rộng tập số tiền
    được phép nhắc lại, nên an toàn; câu trả lời của LLM thì dùng chế độ chặt.
    """
    s = unicodedata.normalize("NFC", text.lower())
    found: set[int] = set()
    for pattern, parse in _LOOSE_AMOUNTS if loose else _STRICT_AMOUNTS:
        for m in pattern.finditer(s):
            found |= {int(v) for v in parse(m)}
        s = pattern.sub(lambda m: " " * len(m[0]), s)
    return found


def _contains(words: list[str], phrase: tuple[str, ...]) -> bool:
    n = len(phrase)
    return any(tuple(words[i:i + n]) == phrase for i in range(len(words) - n + 1))


def _after_last_connector(words: list[str], connectors: frozenset[str]) -> list[str]:
    cuts = [k for k, w in enumerate(words) if w in connectors]
    return words[cuts[-1] + 1:] if cuts else words


def _is_forbidden(sentence: str, g: _Grammar, accented: bool) -> bool:
    if _DOSAGE.search(sentence.lower()):
        return True
    question = sentence.rstrip().endswith("?")
    seen: list[str] = []  # các từ đứng trước trong cùng câu
    for clause in _CLAUSE_BREAK.split(sentence):
        words = words_vi(clause) if accented else [normalize_vi(w) for w in words_vi(clause)]
        joined = " ".join(words)
        for m in g.action.finditer(joined):
            context = _after_last_connector(seen + words[:joined[:m.start()].count(" ")], g.connectors)
            if not any(_contains(context, mk) for mk in g.markers) and not _contains(words, g.doctor):
                return True
        for m in [] if question else g.assertion.finditer(joined):
            i = joined[:m.start()].count(" ")
            window = _after_last_connector(words[max(0, i - 3):i], g.connectors)
            if not any(_contains(window, mk) for mk in g.markers):
                return True
        seen += words
    return False


def _forbidden_sentences(text: str) -> list[str]:
    accented = has_vi_marks(text)
    g = _GRAMMAR[accented]
    sentences = _SENTENCE_BREAK.split(_BULLET.sub("; ", text))
    return [s.strip() for s in sentences if s.strip() and _is_forbidden(s, g, accented)]


def check(text: str, *, known_codes: set[str], allowed_amounts: set[int]) -> list[str]:
    """Danh sách lỗi bằng tiếng Việt; rỗng là đạt."""
    # Mã trong [...] luôn bị kiểm; mã không có ngoặc chỉ bị kiểm khi tiền tố là bệnh viện có thật,
    # để tên xét nghiệm như "HPV-DNA" hay tag "tim-mach" không bị coi là mã gói.
    hospitals = {c.split("-")[0] for c in known_codes}
    codes = {c.upper() for c in _BRACKETED_CODE.findall(text)}
    codes |= {c for c in find_package_codes(text) if c.split("-")[0] in hospitals}
    problems = [f"Mã gói không có trong danh mục: {c}" for c in sorted(codes - known_codes)]
    problems += [f"Số tiền không khớp giá gói nào: {n}" for n in sorted(find_amounts(text) - allowed_amounts)]
    problems += [f"Câu có dạng chẩn đoán hoặc kê đơn: '{s}'" for s in _forbidden_sentences(text)]
    return problems
