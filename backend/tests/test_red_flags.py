import time
from pathlib import Path

import pytest
import yaml

from app.safety import red_flags
from app.safety.red_flags import (
    EMERGENCY_MESSAGE,
    SEE_DOCTOR_NOTE,
    SYMPTOM_CODES,
    _load,
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
    # phủ định đứng trước từ nối ("nhưng", "mà") không phủ định phần sau
    ("tôi không đau nhưng khó thở", "kho_tho"), ("không sốt mà ho ra máu", "xuat_huyet"),
    # cách nói thường gặp
    ("Mẹ tôi vừa bị xỉu", "ngat"), ("bố tôi té xỉu ở nhà", "ngat"), ("sốt cao ngất đi", "ngat"),
    ("Tôi đang mang thai 10 tuần và bị ra máu", "thai_ra_mau"), ("bầu 3 tháng bị ra máu", "thai_ra_mau"),
    ("có thai mà bị chảy máu", "thai_ra_mau"), ("đi cầu ra máu nhiều", "xuat_huyet"),
    ("đau bụng rất dữ dội", "dau_bung_du_doi"), ("bụng đau dữ dội", "dau_bung_du_doi"), ("ngực đau nhói", "dau_nguc"),
    ("bố tôi tự nhiên nói khó hiểu", "dot_quy"), ("uống thuốc không thấy đỡ khó thở", "kho_tho"),
    # tin nhắn có dấu: "chua", "hét", "hệt", "cha" không phải "chưa", "hết", "chả"
    ("Tôi bị ợ chua kèm tức ngực", "dau_nguc"), ("Tôi hét lên vì đau ngực", "dau_nguc"),
    ("đau giống hệt đau ngực lần trước", "dau_nguc"), ("Cha tôi đau ngực", "dau_nguc"),
    ("Không những đau ngực, tôi còn mệt", "dau_nguc"), ("chưa kể đau ngực từ tối qua", "dau_nguc"),
    ("Không ngờ bị đau ngực dữ vậy", "dau_nguc"),
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
    "tôi muốn củng cố sức khỏe", "nỗi khổ của người bị tiểu đường",
    # cụm vô hại viết có dấu trùng cụm cờ đỏ; cứng cổ không kèm sốt không phải cấp cứu
    "Tôi từng nâng ngực, có siêu âm tuyến vú được không?", "Bạn nói khó hiểu quá, giải thích lại giúp mình",
    "Giá gói này cao ngất ngưởng vậy", "Gói này đắt ngất trời", "Đo điện tim có giật không?",
    "Sáng ngủ dậy bị cứng cổ, mỏi vai gáy, nên khám gói nào?", "hay bị mỏi cổ cứng gáy do ngồi máy tính",
    "Tôi có bầu, hay bị chảy máu chân răng",
    # câu phủ nhận khi trả lời câu hỏi sàng lọc
    "Tôi không đau ngực hay khó thở gì cả", "Tôi không có triệu chứng đau ngực hay khó thở",
    "Không có dấu hiệu khó thở", "Tôi chưa bao giờ bị đau ngực", "Tôi không bao giờ bị khó thở",
    "Tôi chẳng đau ngực gì cả", "Tôi chả khó thở gì"])
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


def test_every_yaml_phrase_matches_itself():
    # cụm nào trong YAML cũng phải bắt được chính nó; bắt lỗi tách từ hoặc gõ cụm không thể khớp
    data = yaml.safe_load(Path(red_flags.__file__).with_name("red_flags.yaml").read_text(encoding="utf-8"))
    for rule in data["rules"]:
        for phrase in rule.get("phrases", []) + rule.get("exact", []):
            assert rule["id"] in {h.rule_id for h in detect(phrase)}, phrase
        for phrase in rule.get("except", []):
            assert rule["id"] not in {h.rule_id for h in detect(phrase)}, phrase
        if rule.get("all_of"):
            combo = ", ".join((group.get("phrases") or group["exact"])[0] for group in rule["all_of"])
            assert rule["id"] in {h.rule_id for h in detect(combo)}, combo


def test_long_message_is_fast():
    # mỗi lần khớp chỉ xét vài từ ngay trước, nên thời gian tăng tuyến tính theo độ dài tin nhắn
    start = time.perf_counter()
    detect("không đau ngực " * 3000)
    assert time.perf_counter() - start < 1.0


def test_worst_accepts_severities():
    # Kế hoạch 4 gộp mức cũ trong state với mức mới: worst([cũ, mới])
    assert worst(["see_doctor", None, "emergency"]) == "emergency"
    assert worst([None, "see_doctor"]) == "see_doctor" and worst([None]) is None


def test_empty_yaml_phrase_is_rejected(tmp_path):
    # cụm phủ định rỗng khớp ở mọi vị trí và sẽ tắt hết cờ đỏ, nên phải báo lỗi ngay lúc nạp
    bad = tmp_path / "red_flags.yaml"
    bad.write_text('negations: [không, "!!!"]\nrules:\n'
                   '  - {id: x, severity: emergency, symptom_code: x, phrases: [đau ngực]}\n', encoding="utf-8")
    with pytest.raises(ValueError):
        _load(bad)


def test_messages_are_fixed_vietnamese():
    assert "115" in EMERGENCY_MESSAGE and "bác sĩ" in SEE_DOCTOR_NOTE
