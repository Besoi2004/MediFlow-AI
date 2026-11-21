"""Checklist chuẩn bị trước khám và RAG tài liệu chuẩn bị (RAG ở Kế hoạch 4)."""
from app.models import Package
from app.schemas import ChecklistItem

BRING_ID = "Mang theo CCCD hoặc giấy tờ tùy thân"
ARRIVE_EARLY = "Đến trước giờ hẹn 15 phút để làm thủ tục"


def prep_checklist(package: Package) -> list[ChecklistItem]:
    """Gộp quy tắc chuẩn bị của các hạng mục; cố định, không qua LLM."""
    out: list[ChecklistItem] = []
    fasting = [i for i in package.items if i.fasting_hours > 0]
    if fasting:
        hours = max(i.fasting_hours for i in fasting)
        out.append(ChecklistItem(
            text=f"Nhịn ăn ít nhất {hours} tiếng trước giờ khám (được uống nước lọc)",
            items=[i.name for i in fasting],
        ))

    by_text: dict[str, list[str]] = {}
    for item in package.items:
        if item.prep_instruction:
            by_text.setdefault(item.prep_instruction, []).append(item.name)
    out += [ChecklistItem(text=t, items=names) for t, names in by_text.items()]

    out += [ChecklistItem(text=BRING_ID, items=[]), ChecklistItem(text=ARRIVE_EARLY, items=[])]
    return out
