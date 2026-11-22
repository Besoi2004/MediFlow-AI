"""Che số điện thoại, email, CCCD, CMND, tên tự giới thiệu trước khi gửi LLM hoặc lưu (Kế hoạch 2)."""
import re
import unicodedata

from app.safety.red_flags import detect
from app.textnorm import has_vi_marks, normalize_vi

# Thứ tự quan trọng: email trước (có thể chứa số), CCCD trước số điện thoại.
_PATTERNS = (
    # (?<!...) để chỉ thử từ đầu chuỗi ký tự email: không có nó regex chạy bậc hai với chuỗi dài
    (re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[EMAIL]"),
    # 12 số liền, hoặc tách đều 3-3-3-3 / 4-4-4; tách tùy ý thì trùng ngày giờ "05.12.2026 07.30"
    (re.compile(r"(?<![\d+.,])(?:\d{12}|\d{3}([ .-])\d{3}\1\d{3}\1\d{3}|\d{4}([ .-])\d{4}\2\d{4})(?![.,]?\d)"), "[CCCD]"),
    # CMND 9 số chỉ che khi có từ dẫn: số trần 9 chữ số dễ là tiền ("120000000")
    (re.compile(r"(?i)\b(cmnd|cmt|chứng minh(?:\s+nhân\s+dân)?)(\s*(?:số\s*)?:?\s*)(?:\d{9}|\d{3}([ .-])\d{3}\3\d{3})(?!\d)"),
     r"\1\2[CMND]"),
    (re.compile(r"(?i)(?<!\w)[a-z]{2}\d{13}(?!\d)"), "[BHYT]"),  # thẻ BHYT "DN4010123456789"
    # 0 / +84 / (+84) / 0084 / 84, rồi 9–10 chữ số; mã vùng được trong ngoặc "(028)", "(0236)".
    # Hai chữ số đầu sau đầu số phải liền nhau, nên ngày "05-12-2026 08:00" không bị nhận nhầm;
    # không bắt đầu giữa một số có nhóm nghìn ("2.000.000 - 3.000.000").
    (re.compile(r"(?<![\d+])(?<!\d[.,])(?:(?:\(?\+84\)?|0084|84)[ .-]?\d\d|\(0\d{2,3}\)|0\d\d)(?:[ .-]{0,3}\d){7,8}(?!\d)"),
     "[SĐT]"),
)

# Tên chỉ che khi người dùng tự giới thiệu: "tên tôi là Nguyễn Văn An", "mẹ tôi tên là Bình".
# shortcut: tên không có từ dẫn ("Nguyễn Văn An, 35 tuổi") không che được nếu không có NER
def _marks_optional(pattern: str) -> str:
    """Chữ có dấu trong regex khớp cả khi gõ không dấu: "tôi" -> "t[ôo]i" (cú pháp regex toàn ký tự ASCII)."""
    return re.sub(r"[^\x00-\x7f]", lambda m: f"[{m[0]}{normalize_vi(m[0])}]", pattern)


_PERSON = (r"(?:tôi|mình|em|con|cháu|anh|chị|mẹ|má|bố|ba|cha|vợ|chồng|ông|bà|bé)"
           r"(?:\s+(?:nội|ngoại|gái|trai))?(?:\s+(?:tôi|mình|em|anh|chị))?")  # "ông nội", "con gái tôi"
_NAME_CUE = re.compile(_marks_optional(
    r"(?i)\b(?:tên\s+(?:của\s+)?" + _PERSON + r"\s+là"  # "tên con tôi là": thử trước, kẻo che "tôi"
    r"|tên\s+(?:của\s+)?(?:tôi|mình|em|con|cháu)"  # "tên tôi Lan"
    r"|" + _PERSON + r"\s+tên(?:\s+là)?)[ \t]+"))  # "mẹ tên là Bình", "bố tên Hùng"
_WORD = re.compile(r"[ \t]*([^\W\d_]+)")
_NOT_NAME = {"gì", "tuổi", "năm", "sinh", "ở", "và", "muốn", "đang", "cần", "nhé", "ạ", "nha", "thì", "mà", "nhưng",
             "làm", "đi", "đặt", "khám", "hỏi", "có", "được", "bị", "cho", "là", "nay", "hiện", "nhỉ", "vậy", "này",
             # đầu cụm triệu chứng: "tôi tên lan đau ngực" chỉ che "lan"
             "đau", "nhức", "mệt", "sốt", "ho", "khó", "tức", "chóng", "nôn", "ói", "buồn", "ngất", "xỉu", "không",
             "hay", "rất", "thấy", "cảm"}
# Tin nhắn không dấu: so trên chữ bỏ dấu, trừ các dạng trùng tên người hay gặp ("năm"/Nam, "thì"/Thị, "đạt"/Đạt)
_NOT_NAME_PLAIN = {normalize_vi(w) for w in _NOT_NAME} - {"nam", "thi", "dat", "hien", "lam", "nhi", "cam", "ho",
                                                         "ma", "bi", "di", "dang", "hoi", "sinh"}


def _name_end(text: str, pos: int, max_lower: int, accented: bool) -> int:
    """Hết tên bắt đầu ở pos: các từ viết hoa liền nhau (tối đa 7, như "Tôn Nữ Thị Hoàng Bảo Anh"), hoặc tối đa
    max_lower từ thường trước một từ không phải tên."""
    end, count, capital = pos, 0, None
    while count < 7 and (m := _WORD.match(text, end)):
        word = m[1]
        capital = word[0].isupper() if capital is None else capital
        not_name = word.lower() in _NOT_NAME if accented else normalize_vi(word) in _NOT_NAME_PLAIN
        if (capital and not word[0].isupper()) or (not capital and (not_name or count == max_lower)):
            break
        end, count = m.end(), count + 1
    return end


def _redact_names(text: str, max_lower: int) -> str:
    out, pos, accented = [], 0, has_vi_marks(text)
    for m in _NAME_CUE.finditer(text):
        end = _name_end(text, m.end(), max_lower, accented)
        if m.start() >= pos and end > m.end():
            out += [text[pos:m.end()], "[TÊN]"]
            pos = end
    return "".join(out) + text[pos:]


def _flags(text: str) -> set[str]:
    return {h.rule_id for h in detect(text)}


def redact(text: str) -> str:
    text = unicodedata.normalize("NFC", text)  # dấu tách rời (NFD) làm regex tên không khớp, tên lọt ra ngoài
    for pattern, label in _PATTERNS:
        text = pattern.sub(label, text)
    # Kế hoạch 4 chạy detect() trên bản đã che, nên che tên không được làm mất cờ đỏ nào:
    # nuốt mất triệu chứng thì che hẹp lại (tên thường chỉ một chữ), vẫn mất thì không che tên.
    flags = _flags(text)
    for max_lower in (3, 1):
        masked = _redact_names(text, max_lower)
        if not flags or flags <= _flags(masked):
            return masked
    return text
