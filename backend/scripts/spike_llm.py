"""Thử Gemini: gọi tool tiếng Việt, rút JSON, embedding (Task 7 của Kế hoạch 1).

Chạy: uv run python -m scripts.spike_llm   (cần GOOGLE_API_KEY, LLM_MODEL, EMBEDDING_MODEL trong backend/.env)
Đây là script thử nhanh, không phải code chính; tool chỉ là tool giả trả về rỗng.
"""
import sys
from typing import Literal

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import BaseModel, Field

from app.config import get_settings


@tool
def search_packages(
    gender: Literal["male", "female"] | None = None,
    age: int | None = None,
    purpose: str | None = None,
    budget_max: int | None = None,
    city: str | None = None,
) -> str:
    """Tìm gói khám sức khỏe. purpose là một trong: tong-quat, tim-mach, ung-thu, cao-tuoi, tien-hon-nhan,
    doanh-nghiep. budget_max là ngân sách tối đa tính bằng VND. city là tỉnh/thành."""
    return "[]"


@tool
def get_available_slots(package_code: str, date_from: str | None = None) -> str:
    """Xem khung giờ còn trống của một gói khám (mã gói dạng ALP-CB01), từ ngày date_from (YYYY-MM-DD)."""
    return "[]"


SYSTEM = (
    "Bạn là trợ lý đặt lịch gói khám sức khỏe định kỳ. Khi người dùng cần tìm gói hoặc xem lịch trống, "
    "hãy gọi tool phù hợp. Không tự bịa gói hay giá."
)

# (câu hỏi, tool mong đợi; None = không được gọi tool)
CASES: list[tuple[str, str | None]] = [
    ("Tôi nam 35 tuổi muốn khám tổng quát ở Hà Nội", "search_packages"),
    ("Gói tim mạch dưới 5 triệu ở Đà Nẵng", "search_packages"),
    ("Đặt cho mẹ tôi 62 tuổi một gói người cao tuổi", "search_packages"),
    ("Gói ALP-CB01 còn lịch sáng thứ 7 không?", "get_available_slots"),
    ("Chào bạn", None),
]


class Intake(BaseModel):
    age: int | None = Field(None, description="Tuổi của người đi khám")
    gender: Literal["male", "female"] | None = Field(None, description="Giới tính")
    purpose: str | None = Field(None, description="Mục đích khám")
    budget_max: int | None = Field(None, description="Ngân sách tối đa, đơn vị VND (1 củ = 1 triệu)")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    s = get_settings()
    if not s.google_api_key:
        print("Thiếu GOOGLE_API_KEY trong backend/.env")
        return 1

    llm = init_chat_model(s.llm_model, model_provider=s.llm_provider, google_api_key=s.google_api_key)
    with_tools = llm.bind_tools([search_packages, get_available_slots])

    print(f"== 1. Gọi tool ({s.llm_model})")
    passed = 0
    for question, expected in CASES:
        reply = with_tools.invoke([SystemMessage(SYSTEM), HumanMessage(question)])
        calls = [(c["name"], c["args"]) for c in reply.tool_calls]
        got = calls[0][0] if calls else None
        ok = got == expected
        passed += ok
        print(f"[{'ĐẠT' if ok else 'SAI'}] {question}\n      -> {calls or reply.content!r}")
    print(f"Gọi tool đúng: {passed}/{len(CASES)}")

    print("\n== 2. Rút JSON")
    intake = llm.with_structured_output(Intake).invoke("mình 28t, nữ, muốn tầm soát ung thư, tầm 4 củ")
    print(intake)
    json_ok = intake.age == 28 and intake.gender == "female" and intake.budget_max == 4_000_000
    print("JSON:", "ĐẠT" if json_ok else "SAI")

    print("\n== 3. Embedding")
    if not s.embedding_model:
        print("Chưa đặt EMBEDDING_MODEL trong backend/.env, bỏ qua.")
    else:
        emb = GoogleGenerativeAIEmbeddings(
            model=s.embedding_model, google_api_key=s.google_api_key, output_dimensionality=s.embedding_dim
        )
        print(f"{s.embedding_model}: vector dài {len(emb.embed_query('nhịn ăn trước khi lấy máu'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
