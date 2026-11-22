"""Phát hiện dấu hiệu cờ đỏ theo red_flags.yaml (Kế hoạch 2)."""
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, get_args

import yaml

from app.textnorm import has_vi_marks, normalize_vi, words_vi

Severity = Literal["emergency", "see_doctor"]

EMERGENCY_MESSAGE = (
    "Các dấu hiệu bạn mô tả có thể là tình trạng cấp cứu. Hãy gọi 115 hoặc đến khoa cấp cứu gần nhất ngay, "
    "không chờ lịch khám định kỳ. Nếu có người bên cạnh, hãy nhờ họ hỗ trợ."
)
SEE_DOCTOR_NOTE = "Triệu chứng bạn kể nên được bác sĩ chuyên khoa khám sớm, thay vì chỉ chờ khám sức khỏe định kỳ."

_GAP = 2  # số từ tối đa giữa cụm phủ định và triệu chứng: "không bị đau ngực", "không có triệu chứng khó thở"
_WINDOW = 3  # số từ trước triệu chứng xét not_after ("sợ lấy máu muốn chết")
_SENTENCE_BREAK = re.compile(r"[.;:!?\n]+")
_COMMA = ","  # giữ dấu phẩy thành một từ trong câu: chặn phủ định, nhưng nối được danh sách "A, B hay C"
_YAML = Path(__file__).with_name("red_flags.yaml")
_Phrases = tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class Hit:
    rule_id: str
    severity: Severity
    matched: str


@dataclass(frozen=True)
class Pattern:
    phrases: _Phrases  # từ đã bỏ dấu
    exact: _Phrases  # từ giữ dấu
    excepts: _Phrases  # từ giữ dấu; đoạn khớp chồng lên một cụm này thì bỏ
    not_after: _Phrases  # từ giữ dấu; có trong _WINDOW từ ngay trước đoạn khớp thì bỏ
    still_if: _Phrases  # từ giữ dấu; có trong cùng khoảng thì vẫn giữ đoạn khớp dù có not_after


@dataclass(frozen=True)
class Rule:
    id: str
    severity: Severity
    symptom_code: str
    patterns: tuple[Pattern, ...]  # cụm chính và các nhóm any_of: khớp nhóm nào cũng được
    all_of: tuple[Pattern, ...]  # mọi nhóm cùng có mặt trong tin nhắn, không cần liền nhau


@dataclass(frozen=True)
class Grammar:
    """Từ chức năng ở một dạng: giữ dấu (tin nhắn có dấu) hoặc bỏ dấu (tin nhắn gõ không dấu)."""
    negations: _Phrases
    not_negations: _Phrases
    connectors: frozenset[str]
    coordinators: frozenset[str]


def _starts(words: list[str], phrase: tuple[str, ...]) -> list[int]:
    n = len(phrase)
    return [i for i in range(len(words) - n + 1) if tuple(words[i:i + n]) == phrase]


def _phrases(items: list[str], where: str, *, accented: bool = False) -> _Phrases:
    """Tách cụm đúng như tách tin nhắn (words_vi, rồi bỏ dấu từng từ nếu cần), để hai bên luôn so được."""
    out = tuple(tuple(w if accented else normalize_vi(w) for w in words_vi(p)) for p in items)
    if any(not p or "" in p for p in out):  # cụm rỗng khớp ở mọi vị trí: một phủ định rỗng sẽ tắt hết cờ đỏ
        raise ValueError(f"red_flags.yaml: có cụm rỗng ở {where}")
    return out


def _pattern(d: dict, where: str) -> Pattern:
    return Pattern(_phrases(d.get("phrases", []), where), _phrases(d.get("exact", []), where, accented=True),
                   _phrases(d.get("except", []), where, accented=True),
                   _phrases(d.get("not_after", []), where, accented=True),
                   _phrases(d.get("still_if", []), where, accented=True))


def _grammar(data: dict, accented: bool) -> Grammar:
    def single_words(key: str) -> frozenset[str]:
        phrases = _phrases(data.get(key, []), key, accented=accented)
        if any(len(p) != 1 for p in phrases):
            raise ValueError(f"red_flags.yaml: mỗi mục trong {key} phải là một từ")
        return frozenset(p[0] for p in phrases)

    negations = data["negations"] + (data.get("accented_negations", []) if accented else [])
    return Grammar(_phrases(negations, "negations", accented=accented),
                   _phrases(data.get("not_negations", []), "not_negations", accented=accented),
                   single_words("connectors"), single_words("coordinators"))


def _load(path: Path = _YAML) -> tuple[tuple[Rule, ...], dict[bool, Grammar]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    rules = []
    for r in data["rules"]:
        if r["severity"] not in get_args(Severity):  # gõ sai severity thì worst() sẽ bỏ sót cấp cứu
            raise ValueError(f"red_flags.yaml: severity lạ ở luật {r['id']}: {r['severity']}")
        rules.append(Rule(r["id"], r["severity"], r["symptom_code"],
                          tuple(_pattern(g, r["id"]) for g in [r, *r.get("any_of", [])]),
                          tuple(_pattern(g, r["id"]) for g in r.get("all_of", []))))
    for key in ("id", "symptom_code"):  # trùng symptom_code thì evaluate_codes chỉ giữ một luật
        values = [r[key] for r in data["rules"]]
        if dup := sorted({v for v in values if values.count(v) > 1}):
            raise ValueError(f"red_flags.yaml: {key} bị trùng: {dup}")
    return tuple(rules), {True: _grammar(data, True), False: _grammar(data, False)}


RULES, GRAMMAR = _load()
SYMPTOM_CODES: tuple[str, ...] = tuple(r.symptom_code for r in RULES)
# Khóa (id luật, nhóm): nhóm -1 là cụm chính và any_of của luật, 0, 1... là các nhóm all_of
_PATTERNS = ([((r.id, -1), p) for r in RULES for p in r.patterns]
             + [((r.id, k), p) for r in RULES for k, p in enumerate(r.all_of)])


def _clause_before(words: list[str], s: int, size: int) -> list[str]:
    """Tối đa size từ ngay trước s, không vượt qua dấu phẩy."""
    before = words[max(0, s - size):s]
    return before[len(before) - before[::-1].index(_COMMA):] if _COMMA in before else before


def _spans(p: Pattern, raw: list[str], norm: list[str]) -> list[tuple[int, int]]:
    """Các đoạn [đầu, cuối) khớp cụm của p, trừ đoạn chồng lên cụm loại trừ hoặc đứng sau từ not_after."""
    masked = {k for x in p.excepts for j in _starts(raw, x) for k in range(j, j + len(x))}
    spans = [(i, i + len(ph)) for words, phrases in ((norm, p.phrases), (raw, p.exact))
             for ph in phrases for i in _starts(words, ph)]

    def said_lightly(s: int) -> bool:  # "mệt muốn chết" là nói quá; "mệt mỏi chỉ muốn chết" thì không
        window = _clause_before(raw, s, _WINDOW)
        return (any(_starts(window, x) for x in p.not_after)
                and not any(_starts(window, x) for x in p.still_if))

    return [(s, e) for s, e in spans if masked.isdisjoint(range(s, e)) and not said_lightly(s)]


def _negated(fw: list[str], s: int, g: Grammar) -> bool:
    """Có cụm phủ định kết thúc cách s tối đa _GAP từ, không bị từ nối hay dấu phẩy chặn, không phải cụm như "hết sức"."""
    lo = max(0, s - _GAP - max(map(len, g.negations)))  # chỉ xét vài từ ngay trước s, để chạy tuyến tính
    for neg in g.negations:
        for j in (lo + k for k in _starts(fw[lo:s], neg)):
            end = j + len(neg)
            between = fw[end:s]
            if (s - end <= _GAP and _COMMA not in between and g.connectors.isdisjoint(between)
                    and not any(tuple(fw[j:j + len(x)]) == x for x in g.not_negations)):
                return True
    return False


def _list_goes_on(fw: list[str], e: int, starts: set[int], g: Grammar) -> bool:
    """Ngay sau vị trí e (bỏ qua dấu phẩy) là một triệu chứng khác hoặc "hay/hoặc/và", tức danh sách còn tiếp."""
    k = e
    while k < len(fw) and fw[k] == _COMMA:
        k += 1
    return k < len(fw) and (fw[k] in g.coordinators or k in starts)


def _sentence_words(sentence: str) -> list[str]:
    raw: list[str] = []
    for k, part in enumerate(sentence.split(_COMMA)):
        raw += ([_COMMA] if k else []) + words_vi(part)
    return raw


def detect(text: str) -> list[Hit]:
    accented = has_vi_marks(text)
    g = GRAMMAR[accented]
    found: dict[tuple[str, int], str] = {}  # (id luật, nhóm) -> cụm đầu tiên không bị phủ định
    for sentence in _SENTENCE_BREAK.split(text):
        raw = _sentence_words(sentence)
        norm = [w if w == _COMMA else normalize_vi(w) for w in raw]
        fw = raw if accented else norm
        spans = sorted((s, e, key) for key, p in _PATTERNS for s, e in _spans(p, raw, norm))
        starts = {s for s, _, _ in spans}
        negated_ends: set[int] = set()
        for s, e, key in spans:
            # triệu chứng liệt kê sau "hay/hoặc/và", hoặc sau dấu phẩy khi danh sách còn tiếp ngay sau nó,
            # nhận phủ định của triệu chứng ngay trước: "không đau ngực, khó thở hay ngất"
            prev = fw[s - 1] if s > 0 else None
            listed = s - 1 in negated_ends and (prev in g.coordinators
                                                or (prev == _COMMA and _list_goes_on(fw, e, starts, g)))
            if listed or _negated(fw, s, g):
                negated_ends.add(e)
            else:
                found.setdefault(key, " ".join(norm[s:e]))
    hits = []
    for r in RULES:
        if (r.id, -1) in found:
            hits.append(Hit(r.id, r.severity, found[(r.id, -1)]))
        elif r.all_of and all((r.id, k) in found for k in range(len(r.all_of))):
            hits.append(Hit(r.id, r.severity, " + ".join(found[(r.id, k)] for k in range(len(r.all_of)))))
    return hits


def evaluate_codes(codes: Iterable[str]) -> list[Hit]:
    by_code = {r.symptom_code: r for r in RULES}
    hits = {by_code[c].id: Hit(by_code[c].id, by_code[c].severity, c) for c in codes if c in by_code}
    return list(hits.values())


def worst(items: Iterable[Hit | Severity | None]) -> Severity | None:
    """Mức nặng nhất. Nhận Hit hoặc mức, để Kế hoạch 4 gộp mức cũ trong state với mức mới: worst([cũ, mới])."""
    severities = {i.severity if isinstance(i, Hit) else i for i in items}
    if "emergency" in severities:
        return "emergency"
    return "see_doctor" if "see_doctor" in severities else None
