import pytest

from app.safety.output_guard import DISCLAIMER, SAFE_FALLBACK, check, find_amounts, find_package_codes

CODES = {"ALP-CB01", "GAM-TIM"}
PRICES = {1_200_000, 4_600_000}


@pytest.mark.parametrize("text,amount", [("giá 1.200.000đ", 1_200_000), ("giá 1,2 triệu", 1_200_000),  # Review Focus 4
    ("1200000 VND", 1_200_000), ("chỉ 990k", 990_000), ("tầm 4 củ", 4_000_000), ("4,6 tr", 4_600_000),
    ("1,200,000 đồng", 1_200_000),
    ("ngan sach 2 trieu", 2_000_000)])  # người dùng hay gõ không dấu; Kế hoạch 4 lấy ngân sách từ tin nhắn của họ
def test_find_amounts(text, amount):
    assert amount in find_amounts(text)


@pytest.mark.parametrize("text", ["khám ngày 21/11/2026", "lúc 07:00", "35 tuổi", "nhịn ăn 8 tiếng",
    "đặt cho 2 cụ nhà tôi"])  # "cụ" không phải "củ"
def test_not_amounts(text):
    assert find_amounts(text) == set()


def test_find_codes():
    assert find_package_codes("Gói [ALP-CB01] và alp-tim, xét nghiệm SA-BUNG, KHAM-NOI") == {"ALP-CB01", "ALP-TIM"}


def test_ok_answer():
    text = "Gói [ALP-CB01] giá 1.200.000đ, nằm trong ngân sách 2 triệu của bạn."
    assert check(text, known_codes=CODES, allowed_amounts=PRICES | {2_000_000}) == []


def test_unknown_code_and_amount():
    problems = check("Gói [ALP-VIP99] chỉ 999.000đ", known_codes=CODES, allowed_amounts=PRICES)
    assert any("ALP-VIP99" in p for p in problems) and any("999000" in p for p in problems)


def test_lowercase_code_checked():                                       # Review Focus 5
    assert check("gói alp-cb01 rất hợp", known_codes=CODES, allowed_amounts=PRICES) == []
    assert check("gói alp-xyz9", known_codes=CODES, allowed_amounts=PRICES) != []


@pytest.mark.parametrize("text", ["Bạn bị bệnh tiểu đường rồi", "Chẩn đoán là viêm gan", "Bạn nên uống thuốc hạ áp",
    "Mình kê đơn cho bạn", "Bạn nên làm thêm xét nghiệm PSA",
    "Không sao đâu, bạn bị bệnh nhẹ thôi"])  # "không" ở vế trước không làm câu sau thành lời từ chối
def test_forbidden(text):
    assert check(text, known_codes=CODES, allowed_amounts=PRICES) != []


@pytest.mark.parametrize("text", ["Nếu đang uống thuốc điều trị, hãy hỏi bác sĩ trước khi nhịn ăn",
    "Gói này không chẩn đoán bệnh, chỉ tầm soát",
    "Mình không thể kê đơn hay chẩn đoán, bạn hãy hỏi bác sĩ nhé",        # lời từ chối
    "Nếu bạn bị bệnh tiểu đường, gói này có xét nghiệm đường huyết"])     # giả định, không phải chẩn đoán
def test_allowed_medical_wording(text):
    assert check(text, known_codes=CODES, allowed_amounts=PRICES) == []


def test_fixed_texts_pass_guard():
    assert check(f"{SAFE_FALLBACK} {DISCLAIMER}", known_codes=CODES, allowed_amounts=PRICES) == []
