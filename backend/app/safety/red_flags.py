"""Phát hiện dấu hiệu cờ đỏ theo red_flags.yaml (Kế hoạch 2)."""
import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, get_args

import yaml

from app.textnorm import normalize_vi

Severity = Literal["emergency", "see_doctor"]

EMERGENCY_MESSAGE = (
    "Các dấu hiệu bạn mô tả có thể là tình trạng cấp cứu. Hãy gọi 115 hoặc đến khoa cấp cứu gần nhất ngay, "
    "không chờ lịch khám định kỳ. Nếu có người bên cạnh, hãy nhờ họ hỗ trợ."
)
SEE_DOCTOR_NOTE = "Triệu chứng bạn kể nên được bác sĩ chuyên khoa khám sớm, thay vì chỉ chờ khám sức khỏe định kỳ."

_NEGATION_WINDOW = 3
_CLAUSE_BREAK = re.compile(r"[,.;:!?\n]+")


@dataclass(frozen=True)
class Hit:
    rule_id: str
    severity: Severity
    matched: str


@dataclass(frozen=True)
class Rule:
    id: str
    severity: Severity
    symptom_code: str
    phrases: tuple[tuple[str, ...], ...]  # từ đã bỏ dấu
    exact: tuple[tuple[str, ...], ...]  # từ giữ dấu


def _words(text: str) -> list[str]:
    """Tách từ, giữ dấu: 'Tự TỬ!' -> ['tự', 'tử']."""
    return re.findall(r"[^\W_]+", unicodedata.normalize("NFC", text.lower()))


def _starts(words: list[str], phrase: tuple[str, ...]) -> list[int]:
    n = len(phrase)
    return [i for i in range(len(words) - n + 1) if tuple(words[i:i + n]) == phrase]


_Phrases = tuple[tuple[str, ...], ...]
_YAML = Path(__file__).with_name("red_flags.yaml")


def _phrases(items: list[str], where: str, *, keep_accents: bool = False) -> _Phrases:
    """Tách cụm bằng đúng cách tách tin nhắn (_words rồi bỏ dấu từng từ), để hai bên luôn so được với nhau."""
    out = tuple(tuple(w if keep_accents else normalize_vi(w) for w in _words(p)) for p in items)
    if any(not p or "" in p for p in out):  # cụm rỗng khớp ở mọi vị trí: một phủ định rỗng sẽ tắt hết cờ đỏ
        raise ValueError(f"red_flags.yaml: có cụm rỗng ở {where}")
    return out


def _load(path: Path = _YAML) -> tuple[tuple[Rule, ...], _Phrases, _Phrases, frozenset[str]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    rules = []
    for r in data["rules"]:
        if r["severity"] not in get_args(Severity):  # gõ sai severity thì worst() sẽ bỏ sót cấp cứu
            raise ValueError(f"red_flags.yaml: severity lạ ở luật {r['id']}: {r['severity']}")
        rules.append(Rule(r["id"], r["severity"], r["symptom_code"], _phrases(r["phrases"], r["id"]),
                          _phrases(r.get("exact", []), r["id"], keep_accents=True)))
    return (tuple(rules), _phrases(data["negations"], "negations"),
            _phrases(data.get("not_negations", []), "not_negations"),
            frozenset(normalize_vi(c) for c in data.get("connectors", [])))


RULES, NEGATIONS, NOT_NEGATIONS, CONNECTORS = _load()
SYMPTOM_CODES: tuple[str, ...] = tuple(r.symptom_code for r in RULES)


def _before(norm: list[str], i: int) -> list[str]:
    """Tối đa 3 từ ngay trước vị trí i, bỏ phần đứng trước từ nối gần nhất ("không đau nhưng khó thở")."""
    before = norm[max(0, i - _NEGATION_WINDOW):i]
    cuts = [k for k, w in enumerate(before) if w in CONNECTORS]
    return before[cuts[-1] + 1:] if cuts else before


def _negated(before: list[str]) -> bool:
    """Các từ ngay trước có cụm phủ định, trừ cụm như "hết sức", "không chỉ"."""
    return any(
        not any(tuple(before[j:j + len(x)]) == x for x in NOT_NEGATIONS)
        for neg in NEGATIONS for j in _starts(before, neg)
    )


def _match(rule: Rule, raw: list[str], norm: list[str]) -> str | None:
    """Cụm đầu tiên của luật khớp mà không bị phủ định; trả về cụm đó (đã bỏ dấu)."""
    for words, phrases in ((norm, rule.phrases), (raw, rule.exact)):
        for phrase in phrases:
            for i in _starts(words, phrase):
                if not _negated(_before(norm, i)):
                    return " ".join(norm[i:i + len(phrase)])
    return None


def detect(text: str) -> list[Hit]:
    hits: dict[str, Hit] = {}
    # Xét từng vế câu: "Không, tôi đau ngực" thì "không" không phủ định "đau ngực"
    for clause in _CLAUSE_BREAK.split(text):
        raw = _words(clause)
        norm = [normalize_vi(w) for w in raw]
        for rule in RULES:
            if rule.id not in hits and (matched := _match(rule, raw, norm)):
                hits[rule.id] = Hit(rule.id, rule.severity, matched)
    return list(hits.values())


def evaluate_codes(codes: Iterable[str]) -> list[Hit]:
    by_code = {r.symptom_code: r for r in RULES}
    hits = {by_code[c].id: Hit(by_code[c].id, by_code[c].severity, c) for c in codes if c in by_code}
    return list(hits.values())


def worst(hits: list[Hit]) -> Severity | None:
    severities = {h.severity for h in hits}
    if "emergency" in severities:
        return "emergency"
    return "see_doctor" if "see_doctor" in severities else None
