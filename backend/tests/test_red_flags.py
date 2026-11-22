import pytest

from app.safety.red_flags import (
    EMERGENCY_MESSAGE,
    SEE_DOCTOR_NOTE,
    SYMPTOM_CODES,
    detect,
    evaluate_codes,
    worst,
)
from app.textnorm import normalize_vi


@pytest.mark.parametrize("raw,norm", [("ĐAU NGỰC!!!", "dau nguc"), ("dau   nguc", "dau nguc"),
    ("đau-ngực", "dau nguc"), ("  Khó   thở. ", "kho tho")])
def test_normalize_vi(raw, norm):
    assert normalize_vi(raw) == norm


@pytest.mark.parametrize("text,rule", [
    ("Tự nhiên tôi đau thắt ngực, vã mồ hôi", "dau_nguc"),
    ("ĐAU NGỰC!!!", "dau_nguc"), ("dau nguc trai", "dau_nguc"),        # Review Focus 1
    ("bố tôi bị méo miệng, nói khó từ sáng", "dot_quy"),
    ("tôi bị ho ra máu", "xuat_huyet"), ("dạo này tôi muốn chết", "tu_tu"),
    ("tôi đang có thai ra máu", "thai_ra_mau"),
    # cụm phải gõ đúng dấu (bỏ dấu thì trùng từ vô hại), gõ đúng dấu vẫn phải bắt
    ("tôi muốn tự tử", "tu_tu"), ("mẹ tôi vừa ngất", "ngat"), ("con tôi sốt cao, cứng cổ", "sot_cung_co"),
    # có từ phủ định nhưng không phủ định triệu chứng theo sau
    ("tôi hết sức khó thở", "kho_tho"), ("không chỉ đau ngực mà còn vã mồ hôi", "dau_nguc"),
    ("không hiểu sao đau ngực quá", "dau_nguc"),
])
def test_emergency_detected(text, rule):
    hits = detect(text)
    assert rule in {h.rule_id for h in hits} and worst(hits) == "emergency"


@pytest.mark.parametrize("text", ["sụt cân không rõ lý do 2 tháng nay", "ho kéo dài cả tháng", "sờ thấy khối u ở cổ"])
def test_see_doctor_detected(text):
    assert worst(detect(text)) == "see_doctor"


@pytest.mark.parametrize("text", ["tôi không hề đau ngực", "chưa từng khó thở", "giờ hết đau ngực rồi",  # Review Focus 2
    "tôi muốn khám tổng quát", "gói tim mạch giá bao nhiêu", "nhịn ăn mấy tiếng trước khi lấy máu",
    # bỏ dấu thì trùng cụm cờ đỏ: cũng có/cứng cổ, từ từ/tự tử, ngạt/ngất, củng cố/cứng cổ, nỗi khổ/nói khó
    "tôi cũng có tiền sử cao huyết áp", "bạn cứ từ từ giải thích", "dạo này tôi hay bị ngạt mũi",
    "tôi muốn củng cố sức khỏe", "nỗi khổ của người bị tiểu đường"])
def test_no_false_alarm(text):
    assert detect(text) == []


def test_negation_only_covers_following_phrase():                       # Review Focus 2
    ids = {h.rule_id for h in detect("đau ngực, không khó thở")}
    assert ids == {"dau_nguc"}
    assert {h.rule_id for h in detect("không đau ngực nhưng khó thở")} == {"kho_tho"}


def test_negation_stops_at_punctuation():
    # "Không" ở đây trả lời câu hỏi trước, không phủ định "đau ngực"
    assert {h.rule_id for h in detect("Không, tôi đau ngực từ sáng")} == {"dau_nguc"}


def test_one_hit_per_rule():
    assert len([h for h in detect("đau ngực, tức ngực, nặng ngực") if h.rule_id == "dau_nguc"]) == 1


def test_evaluate_codes_and_symptom_codes():
    assert "dau_nguc" in SYMPTOM_CODES and "sut_can" in SYMPTOM_CODES
    assert worst(evaluate_codes(["sut_can", "ma_la"])) == "see_doctor"
    assert worst(evaluate_codes(["kho_tho"])) == "emergency"
    assert evaluate_codes([]) == [] and worst([]) is None


def test_messages_are_fixed_vietnamese():
    assert "115" in EMERGENCY_MESSAGE and "bác sĩ" in SEE_DOCTOR_NOTE
