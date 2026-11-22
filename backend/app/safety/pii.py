"""Che số điện thoại, email, CCCD trước khi gửi LLM hoặc lưu (Kế hoạch 2)."""
import re

# Thứ tự quan trọng: email trước (có thể chứa số), CCCD trước số điện thoại.
# shortcut: không che CMND 9 số vì dễ trùng số tiền như "120000000"; muốn che thì cần ngữ cảnh ("CMND ...").
_PATTERNS = (
    # (?<!...) để chỉ thử từ đầu chuỗi ký tự email: không có nó regex chạy bậc hai với chuỗi dài
    (re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[EMAIL]"),
    # 12 số liền, hoặc tách đều 3-3-3-3 / 4-4-4; tách tùy ý thì trùng ngày giờ "05.12.2026 07.30"
    (re.compile(r"(?<![\d+.,])(?:\d{12}|\d{3}([ .-])\d{3}\1\d{3}\1\d{3}|\d{4}([ .-])\d{4}\2\d{4})(?![.,]?\d)"), "[CCCD]"),
    # 0 / +84 / (+84) / 0084 / 84, rồi 9–10 chữ số; mã vùng được trong ngoặc "(028)", "(0236)".
    # Hai chữ số đầu sau đầu số phải liền nhau, nên ngày "05-12-2026 08:00" không bị nhận nhầm;
    # không bắt đầu giữa một số có nhóm nghìn ("2.000.000 - 3.000.000").
    (re.compile(r"(?<![\d+])(?<!\d[.,])(?:(?:\(?\+84\)?|0084|84)[ .-]?\d\d|\(0\d{2,3}\)|0\d\d)(?:[ .-]{0,3}\d){7,8}(?!\d)"),
     "[SĐT]"),
)


def redact(text: str) -> str:
    for pattern, label in _PATTERNS:
        text = pattern.sub(label, text)
    return text
