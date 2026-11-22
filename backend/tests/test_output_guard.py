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
    "đặt cho 2 cụ nhà tôi",  # "cụ" không phải "củ"
    "Bạn có thể ăn 1 củ khoai lang luộc vào tối hôm trước", "Đi bộ 10.000 bước mỗi ngày"])
def test_not_amounts(text):
    assert find_amounts(text) == set()


@pytest.mark.parametrize("text,amount", [("ngân sách 4000000", 4_000_000), ("tam 4 cu", 4_000_000),
    ("khoang 500 ngan", 500_000), ("toi co 3000000", 3_000_000), ("1200000d", 1_200_000),
    ("ngân sách 1 triệu rưỡi", 1_500_000), ("5 trăm nghìn", 500_000), ("ngân sách 5 triệu 2 người", 5_000_000)])
def test_find_amounts_loose_reads_user_budget(text, amount):
    # tin nhắn của người dùng: hiểu rộng, vì chỉ làm rộng tập số tiền được phép nhắc lại
    assert amount in find_amounts(text, loose=True)


def test_compound_amounts():
    # phần lẻ sau "triệu" là phần lẻ của triệu, trừ khi có "nghìn" đi kèm
    assert find_amounts("tầm 1tr5") == {1_500_000}
    assert find_amounts("2 triệu 500 nghìn") == {2_500_000}
    assert find_amounts("2 triệu 50 nghìn") == {2_050_000}


def test_code_check_needs_brackets_or_known_hospital():
    # tên xét nghiệm và tag dạng slug không phải mã gói
    assert check("Gói có HPV-DNA, non-HDL, thuộc nhóm tim-mach", known_codes=CODES, allowed_amounts=PRICES) == []
    # mã trong [...] luôn bị kiểm, kể cả tiền tố bệnh viện lạ
    assert check("Gói [XYZ-VIP] rất tốt", known_codes=CODES, allowed_amounts=PRICES) != []
    assert check("Gói [DELTA-VIP] giá 1.200.000đ", known_codes=CODES, allowed_amounts=PRICES) != []


def test_known_codes_any_case():
    assert check("Gói [ALP-CB01] và alp-cb01", known_codes={"alp-cb01"}, allowed_amounts=set()) == []


HOSPITALS = {"Bệnh viện Alpha (mô phỏng)", "ALP", "Bệnh viện Gamma (mô phỏng)", "GAM"}


def test_unknown_hospital_flagged():
    problems = check("Bệnh viện Chợ Rẫy có gói [ALP-CB01]", known_codes=CODES, allowed_amounts=PRICES,
                     known_hospitals=HOSPITALS)
    assert any("Chợ Rẫy" in p for p in problems)
    assert check("bệnh viện tư nhân Tâm Anh rất tốt", known_codes=CODES, allowed_amounts=PRICES,
                 known_hospitals=HOSPITALS) != []


@pytest.mark.parametrize("text", ["Bệnh viện Alpha có gói [ALP-CB01]", "Bệnh viện Đa khoa Alpha (mô phỏng) ở Hà Nội",
    "Các bệnh viện Hà Nội có nhiều gói", "bệnh viện gần nhà bạn", "BV ALP có gói này", "Bệnh viện Gamma Đà Nẵng"])
def test_known_hospitals_pass(text):
    assert check(text, known_codes=CODES, allowed_amounts=PRICES, known_hospitals=HOSPITALS) == []


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
    "Không sao đâu, bạn bị bệnh nhẹ thôi",  # "không" ở vế trước không làm câu sau thành lời từ chối
    "Kết quả chưa rõ nhưng bạn bị bệnh tiểu đường",  # từ nối "nhưng" chặn phủ định lại
    "Bạn bị tiểu đường rồi.", "Bạn bị cao huyết áp, cần điều trị.", "Có thể bạn đang bị tiểu đường type 2.",
    "Bạn nên dùng thuốc hạ áp mỗi sáng.", "Bạn nên uống Metformin 500mg sau ăn.", "Hãy dùng paracetamol 500mg mỗi 6 giờ.",
    "Bạn nên xét nghiệm thêm PSA.", "Mình khuyên bạn làm thêm xét nghiệm HbA1c ngoài gói.",
    "Bạn cần làm thêm xét nghiệm chức năng tuyến giáp.",
    "Mình không chắc, nhưng bạn nên uống thuốc hạ áp",
    "Bạn nên làm xét nghiệm PSA.", "Bạn nên đi xét nghiệm tầm soát ung thư."])
def test_forbidden(text):
    assert check(text, known_codes=CODES, allowed_amounts=PRICES) != []


@pytest.mark.parametrize("text", ["Nếu đang uống thuốc điều trị, hãy hỏi bác sĩ trước khi nhịn ăn",
    "Gói này không chẩn đoán bệnh, chỉ tầm soát",
    "Mình không thể kê đơn hay chẩn đoán, bạn hãy hỏi bác sĩ nhé",        # lời từ chối
    "Nếu bạn bị bệnh tiểu đường, gói này có xét nghiệm đường huyết",     # giả định, không phải chẩn đoán
    # lời từ chối và câu nói về việc của bác sĩ
    "Mình không phải bác sĩ nên không thể chẩn đoán hay kê đơn thuốc cho bạn.",
    "Mình không thể chẩn đoán, kê đơn hoặc chỉ định xét nghiệm.",
    "Mình không thể:\n- chẩn đoán bệnh\n- kê đơn thuốc\n- chỉ định liều dùng",
    "Mình là trợ lý đặt lịch nên không chẩn đoán hay kê đơn được.",
    "Việc kê đơn thuốc cần bác sĩ trực tiếp thăm khám.", "Liều dùng thuốc cần do bác sĩ chỉ định.",
    "Kết quả chẩn đoán là do bác sĩ đưa ra sau khi khám.",
    "Khi bạn bị bệnh mạn tính, nên mang theo kết quả cũ.", "Trường hợp bạn bị bệnh tim, hãy báo trước cho bệnh viện.",
    "Nếu bác sĩ đã kê đơn thuốc huyết áp, bạn vẫn uống như bình thường.",
    "Bạn có hay uống thuốc gì thường xuyên không?", "Bạn đang bị bệnh gì không?",
    # lời dặn chuẩn bị (có thời điểm), không phải khuyên làm xét nghiệm
    "Bạn nên làm xét nghiệm máu vào buổi sáng khi chưa ăn", "Bạn nên làm xét nghiệm máu lúc đói",
    "Bạn cần làm xét nghiệm đường huyết trước 9 giờ sáng", "Bạn không cần làm xét nghiệm thêm"])
def test_allowed_medical_wording(text):
    assert check(text, known_codes=CODES, allowed_amounts=PRICES) == []


def test_fixed_texts_pass_guard():
    assert check(f"{SAFE_FALLBACK} {DISCLAIMER}", known_codes=CODES, allowed_amounts=PRICES) == []
