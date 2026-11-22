"""Che số điện thoại, email, CCCD, CMND, tên tự giới thiệu trước khi gửi LLM hoặc lưu (Kế hoạch 2)."""
import re
import unicodedata

from app.safety.red_flags import detect

# Thứ tự quan trọng: email trước (có thể chứa số), CCCD trước số điện thoại.
_PATTERNS = (
    # (?<!...) để chỉ thử từ đầu chuỗi ký tự email: không có nó regex chạy bậc hai với chuỗi dài
    (re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[EMAIL]"),
    # 12 số liền, hoặc tách đều 3-3-3-3 / 4-4-4; tách tùy ý thì trùng ngày giờ "05.12.2026 07.30"
    (re.compile(r"(?<![\d+.,])(?:\d{12}|\d{3}([ .-])\d{3}\1\d{3}\1\d{3}|\d{4}([ .-])\d{4}\2\d{4})(?![.,]?\d)"), "[CCCD]"),
    # CMND 9 số chỉ che khi có từ dẫn: số trần 9 chữ số dễ là tiền ("120000000")
    (re.compile(r"(?i)\b(cmnd|cmt|chứng minh(?:\s+nhân\s+dân)?)(\s*(?:số\s*)?:?\s*)(?:\d{9}|\d{3}([ .-])\d{3}\3\d{3})(?!\d)"),
     r"\1\2[CMND]"),
    # 0 / +84 / (+84) / 0084 / 84, rồi 9–10 chữ số; mã vùng được trong ngoặc "(028)", "(0236)".
    # Hai chữ số đầu sau đầu số phải liền nhau, nên ngày "05-12-2026 08:00" không bị nhận nhầm;
    # không bắt đầu giữa một số có nhóm nghìn ("2.000.000 - 3.000.000").
    (re.compile(r"(?<![\d+])(?<!\d[.,])(?:(?:\(?\+84\)?|0084|84)[ .-]?\d\d|\(0\d{2,3}\)|0\d\d)(?:[ .-]{0,3}\d){7,8}(?!\d)"),
     "[SĐT]"),
)

# Tên chỉ che khi người dùng tự giới thiệu: "tên tôi là Nguyễn Văn An", "mẹ tôi tên là Bình".
# shortcut: tên không có từ dẫn ("Nguyễn Văn An, 35 tuổi") không che được nếu không có NER
_PERSON = (r"(?:tôi|mình|em|con|cháu|anh|chị|mẹ|má|bố|ba|cha|vợ|chồng|ông|bà|bé)"
           r"(?:\s+(?:nội|ngoại|gái|trai))?(?:\s+(?:tôi|mình|em|anh|chị))?")  # "ông nội", "con gái tôi"
_NAME_CUE = re.compile(r"(?i)\b(?:tên\s+(?:của\s+)?" + _PERSON + r"\s+là"  # "tên con tôi là": thử trước, kẻo che "tôi"
                       r"|tên\s+(?:của\s+)?(?:tôi|mình|em|con|cháu)"  # "tên tôi Lan"
                       r"|" + _PERSON + r"\s+tên(?:\s+là)?)[ \t]+")  # "mẹ tên là Bình", "bố tên Hùng"
_WORD = re.compile(r"[ \t]*([^\W\d_]+)")
_NOT_NAME = {"gì", "tuổi", "năm", "sinh", "ở", "và", "muốn", "đang", "cần", "nhé", "ạ", "nha", "thì", "mà", "nhưng",
             "làm", "đi", "đặt", "khám", "hỏi", "có", "được", "bị", "cho", "là", "nay", "hiện", "nhỉ", "vậy", "này",
             # đầu cụm triệu chứng: "tôi tên lan đau ngực" chỉ che "lan"
             "đau", "nhức", "mệt", "sốt", "ho", "khó", "tức", "chóng", "nôn", "ói", "buồn", "ngất", "xỉu", "không",
             "hay", "rất", "thấy", "cảm"}


def _name_end(text: str, pos: int, max_lower: int) -> int:
    """Hết tên bắt đầu ở pos: các từ viết hoa liền nhau (tối đa 7, như "Tôn Nữ Thị Hoàng Bảo Anh"), hoặc tối đa
    max_lower từ thường trước một từ không phải tên."""
    end, count, capital = pos, 0, None
    while count < 7 and (m := _WORD.match(text, end)):
        word = m[1]
        capital = word[0].isupper() if capital is None else capital
        if (capital and not word[0].isupper()) or (not capital and (word.lower() in _NOT_NAME or count == max_lower)):
            break
        end, count = m.end(), count + 1
    return end


def _redact_names(text: str, max_lower: int) -> str:
    out, pos = [], 0
    for m in _NAME_CUE.finditer(text):
        end = _name_end(text, m.end(), max_lower)
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
