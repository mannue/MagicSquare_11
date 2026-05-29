# Test Plan — AC-FR-01-01 Input Shape Verification (FR-01 / BR-01)

| Meta | Value |
|---|---|
| **Document ID** | TP-AC-FR-01-01 |
| **Version** | 1.0 |
| **Date** | 2026-05-29 |
| **Author Role** | Senior QA Lead |
| **Primary AC** | **AC-FR-01-01** — 4×4 외 입력 즉시 실패 |
| **PRD References** | FR-01 (§10), BR-01 (§11), I/O Contract (§12), Error Policy (§13), Dual-Track §15.1, Traceability §21 |
| **Scenarios** | SC-BND-VAL-000 (None), SC-BND-VAL-004 (non-4×4 shape) |
| **Stack** | Python 3.13+, pytest, pydantic, `unittest.mock` |
| **Out of Scope (this plan)** | 4×4 정상 입력, 빈칸 개수·값 범위·중복 검증 (FR-01 후속 AC) |

---

## 1. Purpose & Scope

본 계획서는 **AC-FR-01-01** 선행 조건인 **입력 형상(4×4) 검증**을 pytest 단위 테스트로 고정하기 위한 문서이다.  
핵심 불변식: **형상 오류 시 Boundary에서 즉시 실패하고, Domain 해 결정 진입점은 호출되지 않는다.**

### 1.1 Error Code Mapping

| Layer | Code (test assertion) | Message (PRD §13) | PRD §12 alias |
|---|---|---|---|
| Boundary shape failure | `INVALID_SIZE` *(test plan label)* | `입력은 4x4 행렬이어야 합니다.` | `E_INVALID_SHAPE` |

> 구현·PRD 추적성 문서에서는 `E_INVALID_SHAPE`를 사용하고, 본 AC 샘플·RED 보드에서는 동일 의미로 **`INVALID_SIZE`** 를 검증 키로 사용한다.

### 1.2 Expected Failure Response Contract (pydantic)

```python
# Conceptual — implementation in src/boundary/errors.py (planned)
class BoundaryErrorResponse(BaseModel):
    code: Literal["INVALID_SIZE"]  # maps to E_INVALID_SHAPE
    message: str = "입력은 4x4 행렬이어야 합니다."
```

---

## 2. Test Objectives

| # | Objective | Verification |
|---|---|---|
| O-1 | `grid=None` 시 `INVALID_SIZE` 즉시 반환 | Assert response `code` / `message` |
| O-2 | 비-4×4 형상(빈 리스트, 열 없음, 3×4·4×3·5×5) 동일 오류 코드 | Parametrized boundary tests |
| O-3 | 형상 검증 실패 시 **Domain 진입 0회** | `unittest.mock` spy on `ResolveMagicSquareUseCase` |
| O-4 | Boundary 커버리지 **≥ 85%** (본 AC 범위) | `pytest-cov` layer-scoped run |
| O-5 | Domain 전역 목표 **≥ 95%** 유지 (본 AC는 Domain 미진입) | Full-suite gate; no false Domain hits |

---

## 3. Unit Test Scope & Priority (pytest)

### 3.1 In-Scope Components

| Priority | Module (planned) | Test Module | Rationale |
|---|---|---|---|
| **P0** | `src/boundary/validator.py` — `BoundaryValidator.validate()` | `tests/boundary/test_validator_shape.py` | AC-FR-01-01 직접 검증 단위 |
| **P0** | `src/boundary/errors.py` — error model / factory | `tests/boundary/test_errors.py` | 응답 계약(pydantic) 고정 |
| **P1** | `src/control/use_cases/resolve_magic_square.py` | `tests/control/test_resolve_magic_square_shape_guard.py` | Control 경유 시 Domain 미호출 오케스트레이션 |
| **P2** | `src/boundary/cli/` (if present) | `tests/boundary/test_cli_shape.py` | CLI는 validator 위임만 검증 (로직 중복 금지) |

### 3.2 Explicitly Out of Scope

| Item | Reason |
|---|---|
| `grid` = valid 4×4 board | AC-FR-01-01 범위 외 — FR-02~05 / 후속 FR-01 AC로 분리 |
| Blank count, value range, duplicate rules | FR-01 AC-FR-01-02~04 (별도 test plan) |
| `BlankFinder`, `Solver`, `MagicSquareValidator` | Domain logic — Track B, shape guard 통과 후 |

### 3.3 RED Test ID Mapping

| Priority | RED ID | Scenario | Test function (candidate) |
|---|---|---|---|
| P0 | TRED-BND-000 | SC-BND-VAL-000 | `test_none_input_rejects_without_domain_call` |
| P1 | TRED-BND-001 | SC-BND-VAL-004 | `test_invalid_shape_rejects_non_4x4[param]` |

### 3.4 Execution Order (Dual-Track §15.3)

1. **Track A RED** — Boundary shape tests fail (`ImportError` / `AssertionError`).
2. **Track A GREEN** — `BoundaryValidator` 최소 shape guard.
3. **Track A REFACTOR** — rule extraction; re-run shape suite only.
4. Domain 구현·연결은 **본 AC GREEN 완료 후** 진행 (Domain 선행 구현 금지).

---

## 4. Boundary Value Cases

모든 케이스는 **동일 기대 결과**를 가정한다 (형상 선행 실패).

```text
{ "code": "INVALID_SIZE", "message": "입력은 4x4 행렬이어야 합니다." }
```

| Case ID | Input (`grid`) | Shape detail | Included | Notes |
|---|---|---|---|---|
| BV-01 | `None` | 명시적 None | **Yes** | AC-FR-01-01 대표 샘플; `TypeError` 미발생, 계약 오류 반환 |
| BV-02 | `[]` | 0행 | **Yes** | 빈 리스트 — row count ≠ 4 |
| BV-03 | `[[]] * 4` | 4행, 각 행 len=0 | **Yes** | 행 존재·열 없음 — column count ≠ 4 |
| BV-04 | `3×4` matrix | 3 rows × 4 cols | **Yes** | row mismatch |
| BV-05 | `4×3` matrix | 4 rows × 3 cols | **Yes** | column mismatch |
| BV-06 | `5×5` matrix | 5 rows × 5 cols | **Yes** | both dimensions mismatch |
| BV-07 | valid `4×4` | 4 rows × 4 cols, syntactically valid | **No** | **AC-FR-01-01 범위 외 — 본 계획서에 포함 금지** |

### 4.1 Parametrize Matrix (pytest)

```python
# Illustrative IDs only — not production code
@pytest.mark.parametrize(
    "grid,case_id",
    [
        (None, "BV-01"),
        ([], "BV-02"),
        ([[]] * 4, "BV-03"),
        (make_grid(3, 4), "BV-04"),
        (make_grid(4, 3), "BV-05"),
        (make_grid(5, 5), "BV-06"),
    ],
    ids=["none", "empty_list", "four_empty_rows", "3x4", "4x3", "5x5"],
)
```

### 4.2 Assertion Checklist (per case)

- [ ] `result.success is False` (or equivalent discriminated union)
- [ ] `result.error.code == "INVALID_SIZE"`
- [ ] `result.error.message` matches PRD message exactly
- [ ] Validator returns without mutating input (`NFR-04` input immutability spot-check where applicable)
- [ ] Domain entry spy `call_count == 0`

---

## 5. Exception & Edge Cases

| Case ID | Category | Input / Condition | Expected behavior |
|---|---|---|---|
| EX-01 | Non-iterable | `grid = 123` or `"abcd"` | `INVALID_SIZE` (shape guard before cell access) |
| EX-02 | Ragged rows | `[[1]*4, [2]*3, [3]*4, [4]*4]` | `INVALID_SIZE` — column inconsistency |
| EX-03 | Nested non-list row | `grid = [(1,2,3,4)] * 4` | `INVALID_SIZE` if contract requires `list` of `list`; document decision in validator |
| EX-04 | `None` row element | `grid = [None, [], [], []]` | `INVALID_SIZE` — treat as invalid row |
| EX-05 | Early exit | BV-01 `None` | Must **not** invoke blank/range/duplicate sub-validators (fail-fast) |
| EX-06 | Double invocation | Call `validate` twice on same `None` | Deterministic same error (`NFR-03`); no Domain side effects |
| EX-07 | Mock leak | Forgotten `patch` teardown | Use `with patch(...)` context; `call_count` reset per test (`function` scope) |

---

## 6. Domain Entry-Point Call Count Verification (mock / spy)

### 6.1 Domain Entry Point Definition

| Name | Path (planned) | Role |
|---|---|---|
| **Primary spy target** | `ResolveMagicSquareUseCase.execute` | Control-layer 해 결정 진입점 |
| Secondary (optional) | `Solver.solve`, `BlankFinder.find` | Entity 직접 호출 금지 경로 감시 |

PRD §13: `E_INVALID_SHAPE` / `INVALID_SIZE` → **Domain resolver 호출: No**

### 6.2 Strategy A — Control Use Case (recommended integration-of-unit)

```python
from unittest.mock import MagicMock, patch

def test_shape_failure_does_not_enter_domain():
    # Arrange
    domain_spy = MagicMock()
    use_case = ResolveMagicSquareUseCase(
        validator=BoundaryValidator(),
        solver=domain_spy,  # or patch object passed to execute
    )
    # Act
    result = use_case.execute(grid=None)
    # Assert
    assert result.error.code == "INVALID_SIZE"
    domain_spy.assert_not_called()
    domain_spy.solve.assert_not_called()  # if solver mock
```

### 6.3 Strategy B — Patch at import site (validator-only unit test)

```python
@patch("src.control.use_cases.resolve_magic_square.ResolveMagicSquareUseCase._run_domain")
def test_validator_none_never_calls_run_domain(mock_run_domain):
    validator = BoundaryValidator()
    result = validator.validate(grid=None)
    assert result.error.code == "INVALID_SIZE"
    mock_run_domain.assert_not_called()
```

### 6.4 Strategy C — `wraps` spy (call count exactness)

```python
from unittest.mock import patch

@patch(
    "src.control.use_cases.resolve_magic_square.ResolveMagicSquareUseCase.execute",
    wraps=ResolveMagicSquareUseCase.execute,
)
def test_none_input_domain_execute_call_count_zero(mock_execute, use_case_fixture):
    use_case_fixture.execute(grid=None)
    # Domain branch inside execute must not run — if full execute is mocked with wraps,
    # assert inner domain collaborator call_count == 0 instead.
```

### 6.5 Verification Rules

| Rule | Requirement |
|---|---|
| V-1 | Shape-fail tests **must** assert `call_count == 0` on Domain entry, not only `assert_not_called` on unused mocks |
| V-2 | One spy per test — avoid shared module-level mocks |
| V-3 | Prefer **`with patch(...)`** over manual `start/stop` |
| V-4 | BV-01 (`None`) is the **mandatory** gate test before parametrized shape suite merges |
| V-5 | Do not mock `BoundaryValidator.validate` when testing Control orchestration — only mock Domain side |

---

## 7. Coverage Goals

| Layer | PRD / NFR | Target | This plan contribution |
|---|---|---|---|
| **Domain (Entity + rules)** | NFR-01 | **≥ 95%** | Shape-fail path adds **0** Domain lines executed — no penalty if Boundary tests isolated |
| **Boundary (validator, errors, formatter)** | NFR-02 | **≥ 85%** | `validator.py` shape branches must hit **100%** of shape guard lines |
| **Control (use_cases)** | Supporting | ≥ 80% (recommended) | `execute` early-return branch for shape errors |

### 7.1 Acceptance Criteria for Coverage Gate

- [ ] `src/boundary/validator.py` — all shape guard branches covered (BV-01~06, EX-01~02 minimum)
- [ ] No coverage inflation via 4×4 valid boards in this suite
- [ ] Domain package coverage ≥ 95% on **full** `pytest` run (project gate), not shape-only subset

---

## 8. pytest-cov Measurement Strategy

### 8.1 Install

```bash
pip install pytest-cov
```

### 8.2 Full project (CI gate)

```bash
pytest --cov=src --cov-report=term-missing
```

### 8.3 Boundary-focused (AC-FR-01-01 iteration)

```bash
pytest tests/boundary/test_validator_shape.py tests/control/test_resolve_magic_square_shape_guard.py \
  --cov=src/boundary \
  --cov=src/control/use_cases \
  --cov-report=term-missing \
  --cov-fail-under=85
```

### 8.4 Domain gate (separate job / nightly)

```bash
pytest tests/entity tests/control \
  --cov=src/entity \
  --cov-report=term-missing \
  --cov-fail-under=95
```

### 8.5 Reporting conventions

| Report | Use |
|---|---|
| `term-missing` | Local RED/GREEN — line-level gaps |
| `html` (optional CI artifact) | `pytest --cov=src --cov-report=html` |
| Omit from coverage | `tests/`, `__init__.py` stubs without logic (configure in `pyproject.toml` / `.coveragerc` when introduced) |

### 8.6 Interpretation notes

- Shape-only runs **overstate** Boundary % if `src/boundary` is small — always confirm against **full** `--cov=src`.
- `grid=None` test should execute **only** validator + error mapping lines; Domain modules appear in report with **0 hits** (expected).

---

## 9. Test Design Standards

| Standard | Rule |
|---|---|
| Framework | pytest |
| Pattern | AAA (Arrange – Act – Assert) |
| Naming | `test_<behavior>_<condition>` |
| Markers | `@pytest.mark.boundary`, `@pytest.mark.ac_fr_01_01` (optional) |
| Models | pydantic `BoundaryErrorResponse` / `ValidationResult` union |
| Mocking | `unittest.mock.patch`, `MagicMock`, `wraps` |
| Fixtures | Scope `function`; shared `make_grid(rows, cols)` helper in `tests/conftest.py` |
| Determinism | Same input → same error (`NFR-03`) |

---

## 10. Traceability Matrix (excerpt)

| AC ID | BR | FR | Scenario | RED ID | Test module | Coverage module |
|---|---|---|---|---|---|---|
| AC-FR-01-01 | BR-01 | FR-01 | SC-BND-VAL-000 | TRED-BND-000 | `tests/boundary/test_validator_shape.py` | `src/boundary/validator.py` |
| AC-FR-01-01 | BR-01 | FR-01 | SC-BND-VAL-004 | TRED-BND-001 | same | `src/boundary/validator.py` |
| Domain isolation | §13 | FR-01 | SC-BND-VAL-000/004 | TRED-BND-000/001 | `tests/control/test_resolve_magic_square_shape_guard.py` | `src/control/use_cases/resolve_magic_square.py` |

---

## 11. Test Run Checklist (QA Sign-off)

- [ ] BV-01 (`None`) passes with `INVALID_SIZE` before merging parametrized suite
- [ ] BV-02 ~ BV-06 pass; BV-07 **absent** from this plan's test files
- [ ] Domain entry `call_count == 0` verified on BV-01 and at least one of BV-04~BV-06
- [ ] `pytest --cov=src/boundary --cov-fail-under=85` green for shape suite
- [ ] Full `pytest --cov=src` documents Domain ≥ 95% (project-level, may pending until Track B exists)
- [ ] No test weakening / deletion to force GREEN (PRD §15.3, §20)

---

## 12. References

- `docs/PRD_MagicSquare.md` — FR-01, §12, §13, NFR-01/02
- `README.md` §6 Scenario → AC → RED Tracking Board
- `.cursor/rules/magicsquare-tdd-testing.mdc`
- `.cursor/rules/magicsquare-ecb-architecture.mdc`
