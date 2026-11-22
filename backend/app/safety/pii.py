"""Che số điện thoại, email, CCCD trước khi gửi LLM hoặc lưu (Kế hoạch 2)."""
import re

# Thứ tự quan trọng: email trước (có thể chứa số), CCCD trước số điện thoại.
# shortcut: không che CMND 9 số vì dễ trùng số tiền như "120000000"; muốn che thì cần ngữ cảnh ("CMND ...").
_PATTERNS = (
    (re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[EMAIL]"),
    (re.compile(r"(?<!\d)\d{12}(?!\d)"), "[CCCD]"),
    # 0 hoặc +84/84, rồi 9–10 chữ số; giữa các chữ số được có dấu cách, chấm, gạch; mã vùng được trong ngoặc "(028)".
    # Hai chữ số đầu sau 0/+84 phải liền nhau, nên ngày "05-12-2026 08:00" không bị nhận nhầm.
    (re.compile(r"(?<![\d+])(?:(?:\+84|84)[ .-]?\d\d|\(0\d\d\)|0\d\d)(?:[ .-]?\d){7,8}(?!\d)"), "[SĐT]"),
)


def redact(text: str) -> str:
    for pattern, label in _PATTERNS:
        text = pattern.sub(label, text)
    return text
