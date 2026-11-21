# Kế hoạch 2: Lõi an toàn (cờ đỏ, che PII, kiểm tra đầu ra)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ba module an toàn chạy bằng luật cố định, không cần LLM, có test đầy đủ:
- `red_flags`: phát hiện dấu hiệu cấp cứu hoặc cần đi khám bác sĩ;
- `pii`: che số điện thoại, email, CCCD;
- `output_guard`: kiểm tra câu trả lời của LLM (mã gói, số tiền, câu chẩn đoán/kê đơn).

Kế hoạch 4 (agent) sẽ gọi ba module này.

**Architecture:**
- Hàm thuần (pure function) trong `backend/app/safety/`, không đụng DB, không gọi mạng.
- Danh sách luật cờ đỏ nằm trong `red_flags.yaml`, viết có dấu cho dễ đọc, khi nạp thì chuẩn hóa về không dấu.
- Mọi so khớp chữ đều chạy trên văn bản đã chuẩn hóa bằng `app.textnorm.normalize_vi`.

**Tech Stack:** Python 3.13, PyYAML, `re`, pytest. Không thêm thư viện.

**Spec:** `docs/superpowers/specs/2026-11-21-mediflow-ai-design.md` (mục 7 "safety_check", "output_guard", "Cờ đỏ trong YAML"; mục 8 PII)

**Điều kiện:** Kế hoạch 1 đã xong (`uv run pytest` trong `backend/` phải PASS hết). Docker Desktop đang chạy.

## Global Constraints

- Không thêm dependency.
- Mọi câu hiển thị cho người dùng bằng tiếng Việt có dấu.
- Luật an toàn cố định, chạy được không cần LLM. Danh sách cờ đỏ chỉ để học, không thay thế quy trình y tế thật (ghi trong comment đầu file YAML).
- Chạy test: `cd backend; uv run pytest` và `uv run ruff check .` phải sạch sau mỗi task.
- Commit message một dòng tiếng Việt, không có dòng Co-Authored-By (xem `CLAUDE.md`).

## Review Focus

1. **Cách gõ khác nhau** ("ĐAU NGỰC!!!", "dau   nguc", "đau-ngực") vẫn bắt được cờ đỏ. → test ở Task 1.
2. **Phủ định đứng trước cụm triệu chứng** ("không hề đau ngực", "chưa từng khó thở") không bị báo. Nhưng "đau ngực, không khó thở" vẫn phải báo đau ngực. → test ở Task 1.
3. **Số điện thoại có dấu cách, chấm, gạch, hoặc +84** đều bị che. Giá tiền ("1.200.000đ", "4000000"), ngày ("21/11/2026"), giờ ("07:00") không bị che. → test ở Task 2.
4. **Số tiền viết nhiều kiểu** ("1.200.000đ", "1,2 triệu", "1200000 VND", "990k", "4 củ") đều được hiểu đúng giá trị. Số tiền chính người dùng đã nói (ngân sách) không bị coi là bịa. → test ở Task 3.
5. **Mã gói viết thường** ("alp-cb01") vẫn được kiểm tra như mã viết hoa. → test ở Task 3.

---

## Cấu trúc file

```
backend/app/textnorm.py            # thêm normalize_vi(); slug_vi() dùng lại nó
backend/app/safety/red_flags.yaml  # luật cờ đỏ
backend/app/safety/red_flags.py    # detect(), evaluate_codes(), worst(), hằng số câu trả lời mẫu
backend/app/safety/pii.py          # redact()
backend/app/safety/output_guard.py # find_package_codes(), find_amounts(), check(), DISCLAIMER, SAFE_FALLBACK
backend/tests/test_red_flags.py
backend/tests/test_pii.py
backend/tests/test_output_guard.py
```

---

### Task 1: Chuẩn hóa chữ + phát hiện cờ đỏ

**Files:**
- Modify: `backend/app/textnorm.py`, `backend/app/safety/red_flags.yaml`, `backend/app/safety/red_flags.py`
- Test: `backend/tests/test_red_flags.py` (`tests/test_seed.py::test_slug_vi` phải vẫn PASS)

**Interfaces:**
- Produces (`app.textnorm`):
  - `normalize_vi(text: str) -> str`: chữ thường, bỏ dấu, `đ→d`, mọi chuỗi ký tự không phải chữ/số thành **một dấu cách**, cắt hai đầu. Ví dụ `"ĐAU NGỰC!!!" → "dau nguc"`.
  - `slug_vi(text)` giữ nguyên hành vi, viết lại thành `normalize_vi(text).replace(" ", "-")`.
- Produces (`app.safety.red_flags`):
  - `Severity = Literal["emergency", "see_doctor"]`.
  - `@dataclass(frozen=True) class Hit: rule_id: str; severity: Severity; matched: str`. `matched` là cụm đã chuẩn hóa bị bắt.
  - `RULES` (nạp một lần từ YAML lúc import), `SYMPTOM_CODES: tuple[str, ...]` (mọi `symptom_code` trong YAML; Kế hoạch 4 dùng làm `Literal` cho tool `check_symptoms`).
  - `detect(text: str) -> list[Hit]`: chuẩn hóa text rồi tìm từng cụm như một dãy token liền nhau. Bỏ qua lần khớp nếu trong **3 token ngay trước** có một cụm phủ định. Mỗi luật tối đa 1 `Hit`.
  - `evaluate_codes(codes: Iterable[str]) -> list[Hit]`: mã nào có trong YAML thì ra `Hit` (`matched` = mã); mã lạ bỏ qua.
  - `worst(hits: list[Hit]) -> Severity | None`: `emergency` nếu có, rồi `see_doctor`, không có thì `None`.
  - Hằng số câu trả lời mẫu, viết đúng nguyên văn:
    - `EMERGENCY_MESSAGE = "Các dấu hiệu bạn mô tả có thể là tình trạng cấp cứu. Hãy gọi 115 hoặc đến khoa cấp cứu gần nhất ngay, không chờ lịch khám định kỳ. Nếu có người bên cạnh, hãy nhờ họ hỗ trợ."`
    - `SEE_DOCTOR_NOTE = "Triệu chứng bạn kể nên được bác sĩ chuyên khoa khám sớm, thay vì chỉ chờ khám sức khỏe định kỳ."`
- `red_flags.yaml` có dạng:
  ```yaml
  # Danh sách cờ đỏ CHỈ ĐỂ HỌC, không thay thế quy trình y tế thật. Viết có dấu; code tự chuẩn hóa.
  negations: [không, chưa, chưa từng, không hề, hết, không còn]
  rules:
    - {id: dau_nguc, severity: emergency, symptom_code: dau_nguc, phrases: [đau ngực, đau thắt ngực, tức ngực, nặng ngực]}
  ```
- Tối thiểu các luật sau (builder được thêm cụm từ):

| id | severity | phrases (ví dụ) |
|---|---|---|
| dau_nguc | emergency | đau ngực, đau thắt ngực, tức ngực, nặng ngực |
| kho_tho | emergency | khó thở, thở dốc, hụt hơi, ngạt thở |
| dot_quy | emergency | yếu nửa người, liệt nửa người, tê nửa người, méo miệng, nói ngọng đột ngột, nói khó |
| ngat | emergency | ngất, bất tỉnh, ngất xỉu |
| co_giat | emergency | co giật |
| xuat_huyet | emergency | ho ra máu, nôn ra máu, đi ngoài ra máu, chảy máu không cầm |
| sot_cung_co | emergency | cứng cổ, sốt cao co giật |
| tu_tu | emergency | tự tử, tự sát, muốn chết, không muốn sống |
| thai_ra_mau | emergency | có thai ra máu, mang thai ra máu, đang bầu ra máu |
| dau_bung_du_doi | emergency | đau bụng dữ dội |
| dau_keo_dai | see_doctor | đau kéo dài, đau mấy ngày nay, đau nhiều ngày |
| sot_keo_dai | see_doctor | sốt kéo dài, sốt mấy ngày |
| sut_can | see_doctor | sụt cân không rõ lý do, sụt cân nhanh, giảm cân không rõ nguyên nhân |
| khoi_u | see_doctor | sờ thấy khối u, nổi cục, có khối u |
| ho_keo_dai | see_doctor | ho kéo dài, ho mấy tuần |

- [ ] **Step 1: Viết test thất bại `tests/test_red_flags.py`**

```python
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
])
def test_emergency_detected(text, rule):
    hits = detect(text)
    assert rule in {h.rule_id for h in hits} and worst(hits) == "emergency"

@pytest.mark.parametrize("text", ["sụt cân không rõ lý do 2 tháng nay", "ho kéo dài cả tháng", "sờ thấy khối u ở cổ"])
def test_see_doctor_detected(text):
    assert worst(detect(text)) == "see_doctor"

@pytest.mark.parametrize("text", ["tôi không hề đau ngực", "chưa từng khó thở", "giờ hết đau ngực rồi",  # Review Focus 2
    "tôi muốn khám tổng quát", "gói tim mạch giá bao nhiêu", "nhịn ăn mấy tiếng trước khi lấy máu"])
def test_no_false_alarm(text):
    assert detect(text) == []

def test_negation_only_covers_following_phrase():                       # Review Focus 2
    ids = {h.rule_id for h in detect("đau ngực, không khó thở")}
    assert ids == {"dau_nguc"}
    assert {h.rule_id for h in detect("không đau ngực nhưng khó thở")} == {"kho_tho"}

def test_one_hit_per_rule():
    assert len([h for h in detect("đau ngực, tức ngực, nặng ngực") if h.rule_id == "dau_nguc"]) == 1

def test_evaluate_codes_and_symptom_codes():
    assert "dau_nguc" in SYMPTOM_CODES and "sut_can" in SYMPTOM_CODES
    assert worst(evaluate_codes(["sut_can", "ma_la"])) == "see_doctor"
    assert worst(evaluate_codes(["kho_tho"])) == "emergency"
    assert evaluate_codes([]) == [] and worst([]) is None

def test_messages_are_fixed_vietnamese():
    assert "115" in EMERGENCY_MESSAGE and "bác sĩ" in SEE_DOCTOR_NOTE
```

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `uv run pytest tests/test_red_flags.py -q`
Expected: FAIL (ImportError: `normalize_vi`, `detect` chưa có).

- [ ] **Step 3: Viết `normalize_vi`, sửa `slug_vi`, viết YAML và `red_flags.py`**

So khớp token: tách `normalize_vi(text).split()`, so từng cụm (đã tách token) như dãy liền nhau. Phủ định: nối 3 token trước vị trí khớp thành chuỗi rồi kiểm tra có chứa một cụm phủ định ở ranh giới từ hay không.

Cụm "muốn chết" sẽ bắt cả câu nói quá như "nóng muốn chết". Cố ý chấp nhận để an toàn; ghi một dòng comment `shortcut:` trong YAML.

- [ ] **Step 4: Chạy test**

Run: `uv run pytest -q; uv run ruff check .`
Expected: toàn bộ PASS (cả `test_slug_vi` cũ), ruff sạch.

- [ ] **Step 5: Commit**

```powershell
git add backend
git commit -m "feat: phát hiện cờ đỏ bằng luật cố định"
```

---

### Task 2: Che PII

**Files:**
- Modify: `backend/app/safety/pii.py`
- Test: `backend/tests/test_pii.py`

**Interfaces:**
- Produces (`app.safety.pii`): `redact(text: str) -> str`. Thay theo thứ tự:
  1. Email → `[EMAIL]`.
  2. CCCD: đúng 12 chữ số liền, không có chữ số kề hai bên → `[CCCD]`.
  3. Số điện thoại Việt Nam → `[SĐT]`. Nhận dạng: bắt đầu bằng `0` hoặc `+84` / `84`, sau đó 9–10 chữ số. Giữa các chữ số có thể có dấu cách, `.` hoặc `-`. Không có chữ số kề hai bên.
- Không che CMND 9 số: dễ trùng với số tiền như "120000000". Ghi `shortcut:` trong code.

- [ ] **Step 1: Viết test thất bại `tests/test_pii.py`**

```python
@pytest.mark.parametrize("raw,expected", [
    ("sđt mình 0901234567 nhé", "sđt mình [SĐT] nhé"),
    ("gọi 0901 234 567", "gọi [SĐT]"), ("gọi 0901.234.567", "gọi [SĐT]"),       # Review Focus 3
    ("gọi 0901-234-567", "gọi [SĐT]"), ("số +84 901234567", "số [SĐT]"),
    ("bàn 02838123456", "bàn [SĐT]"),
    ("mail an.nguyen@gmail.com", "mail [EMAIL]"),
    ("CCCD 001090012345", "CCCD [CCCD]"),
])
def test_redacts(raw, expected):
    assert redact(raw) == expected

@pytest.mark.parametrize("text", ["gói 1.200.000đ", "ngân sách 4000000", "khám ngày 21/11/2026 lúc 07:00",  # Review Focus 3
    "tôi 35 tuổi", "mã gói ALP-CB01", "giá 120000000 đồng"])
def test_keeps_non_pii(text):
    assert redact(text) == text

def test_redacts_several_in_one_message():
    out = redact("0901234567 hoặc 0912 345 678, mail a@b.vn")
    assert out == "[SĐT] hoặc [SĐT], mail [EMAIL]"
```

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `uv run pytest tests/test_pii.py -q`
Expected: FAIL (`redact` chưa có).

- [ ] **Step 3: Viết `redact`**

- [ ] **Step 4: Chạy test**

Run: `uv run pytest -q; uv run ruff check .`
Expected: toàn bộ PASS.

- [ ] **Step 5: Commit**

```powershell
git add backend
git commit -m "feat: che số điện thoại, email, cccd"
```

---

### Task 3: Kiểm tra đầu ra của LLM

**Files:**
- Modify: `backend/app/safety/output_guard.py`
- Test: `backend/tests/test_output_guard.py`

**Interfaces:**
- Consumes: `normalize_vi`.
- Produces (`app.safety.output_guard`):
  - `DISCLAIMER = "Thông tin chỉ mang tính tham khảo, vui lòng tham vấn bác sĩ để cá nhân hóa tầm soát."`
  - `SAFE_FALLBACK = "Xin lỗi, mình chưa trả lời chính xác được. Bạn xem thông tin gói và giá trong các thẻ bên dưới, hoặc hỏi lại giúp mình nhé."`
  - `find_package_codes(text: str) -> set[str]`:
    - Bắt token dạng 3 chữ cái + `-` + ít nhất 2 chữ/số, có ranh giới từ ở đầu. Ví dụ `ALP-CB01`, `alp-cb01`, `[BET-TQNAM]`.
    - Trả về viết hoa.
    - Không bắt mã hạng mục 2 chữ (`SA-BUNG`) hay 4 chữ (`KHAM-NOI`).
  - `find_amounts(text: str) -> set[int]`: số tiền VND theo các dạng:
    - `1.200.000` / `1,200,000` (nhóm nghìn, có hoặc không có `đ/₫/vnd/vnđ/đồng`);
    - `1200000 đ|vnd|đồng` (từ 4 chữ số trở lên kèm đơn vị);
    - `1,2 triệu` / `4 tr` / `4 củ` → ×1.000.000;
    - `990k` / `990 nghìn|ngàn` → ×1.000.
    - Không coi ngày, giờ, tuổi là tiền.
  - `FORBIDDEN_PHRASES` (đã chuẩn hóa, so ở ranh giới từ), tối thiểu: `ban bi benh`, `ban mac benh`, `chan doan la`, `chan doan cua ban`, `ban bi ung thu`, `nen uong thuoc`, `hay uong thuoc`, `ke don`, `lieu dung`, `ban nen lam them xet nghiem`.
  - `check(text: str, *, known_codes: set[str], allowed_amounts: set[int]) -> list[str]`: danh sách lỗi bằng tiếng Việt (rỗng = đạt). Ba loại lỗi:
    - `"Mã gói không có trong danh mục: X"`
    - `"Số tiền không khớp giá gói nào: N"`
    - `"Câu có dạng chẩn đoán hoặc kê đơn: '...'"`
  - Kế hoạch 4 truyền `allowed_amounts` = giá mọi gói đang bán ∪ các số tiền mà người dùng đã nói trong hội thoại.

- [ ] **Step 1: Viết test thất bại `tests/test_output_guard.py`**

```python
CODES = {"ALP-CB01", "GAM-TIM"}
PRICES = {1_200_000, 4_600_000}

@pytest.mark.parametrize("text,amount", [("giá 1.200.000đ", 1_200_000), ("giá 1,2 triệu", 1_200_000),  # Review Focus 4
    ("1200000 VND", 1_200_000), ("chỉ 990k", 990_000), ("tầm 4 củ", 4_000_000), ("4,6 tr", 4_600_000),
    ("1,200,000 đồng", 1_200_000)])
def test_find_amounts(text, amount):
    assert amount in find_amounts(text)

@pytest.mark.parametrize("text", ["khám ngày 21/11/2026", "lúc 07:00", "35 tuổi", "nhịn ăn 8 tiếng"])
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
    "Mình kê đơn cho bạn", "Bạn nên làm thêm xét nghiệm PSA"])
def test_forbidden(text):
    assert check(text, known_codes=CODES, allowed_amounts=PRICES) != []

@pytest.mark.parametrize("text", ["Nếu đang uống thuốc điều trị, hãy hỏi bác sĩ trước khi nhịn ăn",
    "Gói này không chẩn đoán bệnh, chỉ tầm soát"])
def test_allowed_medical_wording(text):
    assert check(text, known_codes=CODES, allowed_amounts=PRICES) == []
```

- [ ] **Step 2: Chạy, xác nhận thất bại**

Run: `uv run pytest tests/test_output_guard.py -q`
Expected: FAIL (`check` chưa có).

- [ ] **Step 3: Viết `output_guard.py`**

Số tiền:
- Tìm trên chữ thường, giữ nguyên chữ số.
- Thứ tự: thử dạng có đơn vị "triệu/tr/củ/k/nghìn/ngàn" trước, rồi tới nhóm nghìn, rồi tới số trần kèm `đ/vnd/đồng`.
- Không đếm trùng cùng một đoạn chữ.
- `1,2` trong "1,2 triệu" là số thập phân. `1,200,000` là nhóm nghìn.

- [ ] **Step 4: Chạy test**

Run: `uv run pytest -q; uv run ruff check .`
Expected: toàn bộ PASS.

- [ ] **Step 5: Commit + cập nhật trạng thái**

Sửa bảng trong `CLAUDE.md`: Kế hoạch 2 → "xong".
```powershell
git add backend CLAUDE.md
git commit -m "feat: kiểm tra đầu ra của llm"
```
