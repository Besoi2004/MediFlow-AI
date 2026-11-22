import time
import unicodedata
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
    # dấu phẩy không nối danh sách phủ định khi không có "hay/hoặc/và" khép lại
    ("Tôi không đau ngực, khó thở lắm", "kho_tho"), ("không đau nhưng mà khó thở", "kho_tho"),
    ("Tôi không đau ngực, khó thở, tôi mệt và lo lắng", "kho_tho"),  # "và" ở xa không khép danh sách
    # "muốn chết" sau từ cảm xúc thật thì vẫn báo
    ("Tôi buồn muốn chết", "tu_tu"), ("đau khổ muốn chết", "tu_tu"), ("tôi mệt mỏi, muốn chết", "tu_tu"),
    # từ nói quá đi cùng dấu hiệu ý định thật thì vẫn báo
    ("Tôi mệt mỏi chỉ muốn chết", "tu_tu"), ("mệt quá chỉ muốn chết", "tu_tu"), ("Tôi mệt mỏi muốn chết", "tu_tu"),
    # từ nói quá chỉ tắt "muốn chết"; "không muốn sống", "tự tử" thì không bao giờ là nói quá
    ("tôi mệt không muốn sống nữa", "tu_tu"), ("mệt quá không muốn sống", "tu_tu"), ("lo quá muốn tự tử", "tu_tu"),
    ("sợ quá nghĩ đến tự tử", "tu_tu"), ("mệt quá muốn tự sát", "tu_tu"),
    ("tôi không còn muốn sống nữa", "tu_tu"), ("tôi chẳng muốn sống", "tu_tu"), ("tôi chán sống quá", "tu_tu"),
    ("em không thiết sống nữa", "tu_tu"),
    # "em" còn là "của tôi": "bố em nói khó" là triệu chứng đột quỵ của bố
    ("bố em nói khó từ sáng", "dot_quy"), ("em nói khó từ sáng", "dot_quy"),
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
    "Tôi chẳng đau ngực gì cả", "Tôi chả khó thở gì",
    # phủ định áp cho cả danh sách "A, B hay C"
    "Tôi không đau ngực, khó thở hay ngất", "Tôi không bị đau ngực, khó thở, hay chóng mặt gì",
    # nói quá
    "Tôi sợ lấy máu muốn chết", "trời nóng muốn chết", "mệt muốn chết luôn"])
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
        for group in [rule, *rule.get("any_of", [])]:
            for phrase in group.get("phrases", []) + group.get("exact", []):
                assert rule["id"] in {h.rule_id for h in detect(phrase)}, phrase
            for phrase in group.get("except", []):
                assert rule["id"] not in {h.rule_id for h in detect(phrase)}, phrase
        if rule.get("all_of"):
            combo = ", ".join((group.get("phrases") or group["exact"])[0] for group in rule["all_of"])
            assert rule["id"] in {h.rule_id for h in detect(combo)}, combo


_CORPUS = yaml.safe_load(Path(__file__).with_name("red_flag_messages.yaml").read_text(encoding="utf-8"))
_POSITIVE = [(rule, text) for rule, texts in _CORPUS.items() if rule != "none" for text in texts]


def _strip_marks(text: str) -> str:
    """Bỏ dấu nhưng giữ dấu câu, như khách gõ không dấu: "Tôi khó thở, mệt" -> "Toi kho tho, met"."""
    plain = "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
    return plain.replace("đ", "d").replace("Đ", "D")


@pytest.mark.parametrize("rule,text", _POSITIVE)
def test_corpus_detected(rule, text):
    assert rule in {h.rule_id for h in detect(text)}


@pytest.mark.parametrize("text", _CORPUS["none"])
def test_corpus_no_false_alarm(text):
    assert detect(text) == []


@pytest.mark.parametrize("rule,text", _POSITIVE)
def test_corpus_unaccented(rule, text):
    # cụm trong phrases phải bắt được cả khi gõ không dấu; cụm exact thì để lớp 2 (check_symptoms)
    data = yaml.safe_load(Path(red_flags.__file__).with_name("red_flags.yaml").read_text(encoding="utf-8"))
    exact = {normalize_vi(p) for r in data["rules"] for g in [r, *r.get("any_of", []), *r.get("all_of", [])]
             for p in g.get("exact", [])}
    hit = next(h for h in detect(text) if h.rule_id == rule)
    if any(part in exact for part in hit.matched.split(" + ")):
        pytest.skip("cụm exact")
    assert rule in {h.rule_id for h in detect(_strip_marks(text))}, _strip_marks(text)


def test_seed_catalog_never_flags():
    # khách hay chép nguyên tên gói, dịch vụ vào câu hỏi: "gói Tầm soát tim mạch giá bao nhiêu"
    def strings(x):
        if isinstance(x, str):
            yield x
        for v in x.values() if isinstance(x, dict) else x if isinstance(x, list) else []:
            yield from strings(v)

    data_dir = Path(red_flags.__file__).parents[2] / "data"
    texts = [s for f in data_dir.glob("*.yaml") for s in strings(yaml.safe_load(f.read_text(encoding="utf-8")))]
    assert len(texts) > 100 and [t for t in texts if detect(t)] == []


def test_long_message_is_fast():
    # mỗi lần khớp chỉ xét vài từ ngay trước, nên thời gian tăng tuyến tính theo độ dài tin nhắn
    start = time.perf_counter()
    detect("không đau ngực " * 3000)
    assert time.perf_counter() - start < 1.0


def test_worst_accepts_severities():
    # Kế hoạch 4 gộp mức cũ trong state với mức mới: worst([cũ, mới])
    assert worst(["see_doctor", None, "emergency"]) == "emergency"
    assert worst([None, "see_doctor"]) == "see_doctor" and worst([None]) is None


_RULE = "  - {id: x, severity: emergency, symptom_code: x, phrases: [đau ngực]}\n"


@pytest.mark.parametrize("yaml_text,error", [
    # cụm rỗng khớp ở mọi vị trí: phủ định rỗng tắt hết cờ đỏ, cụm triệu chứng rỗng báo cấp cứu mọi tin nhắn
    ('negations: [không, "!!!"]\nrules:\n' + _RULE, "cụm rỗng"),
    ('negations: [không]\nrules:\n  - {id: x, severity: emergency, symptom_code: x, phrases: [đau ngực, "..."]}\n',
     "cụm rỗng"),
    ('negations: [không]\nrules:\n  - {id: x, severity: emergency, symptom_code: x, phrases: [ho], exact: ["?"]}\n',
     "cụm rỗng"),
    # trùng symptom_code thì evaluate_codes chỉ giữ một luật, có thể mất luật cấp cứu
    ("negations: [không]\nrules:\n" + _RULE + "  - {id: y, severity: see_doctor, symptom_code: x, phrases: [ho]}\n",
     "trùng"),
    ("negations: [không]\nconnectors: [nhưng mà]\nrules:\n" + _RULE, "một từ"),
])
def test_bad_yaml_is_rejected(tmp_path, yaml_text, error):
    bad = tmp_path / "red_flags.yaml"
    bad.write_text(yaml_text, encoding="utf-8")
    with pytest.raises(ValueError, match=error):
        _load(bad)


def test_messages_are_fixed_vietnamese():
    assert "115" in EMERGENCY_MESSAGE and "bác sĩ" in SEE_DOCTOR_NOTE
