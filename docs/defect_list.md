# Defect List — Magic Square 4×4 (RED Phase)

| Meta | Value |
|---|---|
| **Document ID** | DL-RED-AC-FR-01-01 |
| **Last Updated** | 2026-05-29 |
| **Test Run** | `python -m pytest tests/boundary/test_validator_shape_ac_fr_01_01.py tests/control/test_resolve_shape_guard_ac_fr_01_01.py -v` |
| **Result Summary** | 30 collected — **23 ERROR**, **2 FAILED**, **5 PASSED** (scope/meta only) |
| **Related AC** | AC-FR-01-01 (FR-01 / BR-01, PRD §8.1 `INVALID_SIZE`) |
| **Related Tests** | `tests/boundary/test_validator_shape_ac_fr_01_01.py`, `tests/control/test_resolve_shape_guard_ac_fr_01_01.py` |

> **Note:** 본 목록은 RED 단계에서 테스트가 드러낸 **production 결함(미구현)** 입니다.  
> 범위 제한 메타 테스트 5건은 의도적으로 PASS이며 결함이 아닙니다.

---

## Defect Register

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| DEF-001 | Critical | AC-FR-01-01 | `pytest tests/boundary/...` 실행 시 `boundary_validator` fixture 로드 | `src.boundary` 패키지 import 성공 | `ModuleNotFoundError: No module named 'src.boundary'` | `src/boundary/` 패키지·`__init__.py` 미생성 | `src/boundary/` 스캐폴드 추가 (`validator.py`, `errors.py`) |
| DEF-002 | Critical | AC-FR-01-01 | `pytest tests/control/...` 실행 시 `resolve_use_case` fixture 로드 | `src.control` 패키지 import 성공 | `ModuleNotFoundError: No module named 'src.control'` | `src/control/use_cases/` 미생성 | `src/control/use_cases/resolve_magic_square.py` 스캐폴드 추가 |
| DEF-003 | Critical | AC-FR-01-01 | `grid=None` → `BoundaryValidator.validate(grid)` 호출 (`test_none_grid_returns_code_invalid_size`) | `{ success: false, error.code: "INVALID_SIZE", error.message: "Grid must be 4x4." }` | fixture setup ERROR (DEF-001) | `BoundaryValidator`·None 분기 미구현 | `if grid is None: return ValidationFailure(INVALID_SIZE)` |
| DEF-004 | Critical | AC-FR-01-01 | `grid=None` → `ResolveMagicSquareUseCase.execute(grid)` (`test_none_grid_resolve_call_count_is_zero`) | `domain_resolver.resolve` 호출 **0회** + shape 실패 반환 | fixture setup ERROR (DEF-002) | Control shape guard·Domain 격리 미구현 | `execute` 초입에서 validator 호출, 실패 시 `resolve()` 미호출 |
| DEF-005 | High | AC-FR-01-01 | `grid=[]` → `validate(grid)` (`test_empty_list_grid_returns_invalid_size_failure`) | `code="INVALID_SIZE"`, Domain 미진입 | ERROR at setup (DEF-001) | 빈 리스트(0행) 형상 검사 누락 | row count `!= 4` 시 `INVALID_SIZE` 반환 |
| DEF-006 | High | AC-FR-01-01 | `grid=[[]]*4` → `validate(grid)` (`test_four_empty_rows_grid_returns_invalid_size_failure`) | `code="INVALID_SIZE"` (열 길이 0 ≠ 4) | ERROR at setup (DEF-001) | 열 길이 검증 누락 | 각 row `len(row) != 4` 시 즉시 실패 |
| DEF-007 | High | AC-FR-01-01 | `grid=make_grid(3,4)` / `(4,3)` / `(5,5)` → `validate(grid)` | 모든 비-4×4 입력에 `INVALID_SIZE` | ERROR at setup (DEF-001) | 4×4 고정 shape guard 없음 | `rows==4 and all(len(r)==4 for r in grid)` 검사 추가 |
| DEF-008 | High | AC-FR-01-01 | `grid=None` 후 `result.error.message` 비교 (`test_none_grid_message_exact_match_prd_8_1`) | `"Grid must be 4x4."` 문자 단위 일치 | ERROR at setup (DEF-001) | 오류 메시지 상수·팩토리 없음 | `INVALID_SIZE_MESSAGE` 상수 정의 후 단일 소스 사용 |
| DEF-009 | Medium | AC-FR-01-01 | `test_none_grid_returns_validation_failure_type` — `_validate(None)` 직접 호출 | `isinstance(result, ValidationFailure)` | `ModuleNotFoundError: src.boundary` (import 단계) | `src.boundary.errors.ValidationFailure` pydantic 모델 미정의 | `ValidationFailure` / `BoundaryErrorResponse` pydantic 모델 추가 |
| DEF-010 | Medium | AC-FR-01-01 | `grid=None` 입력 시 `TypeError` 없이 계약 실패 (`test_none_grid_does_not_raise_type_error_on_validate`) | `validate(None)` 정상 반환, `success is False` | ERROR at setup (DEF-001) | None에 대해 예외만 발생하거나 미처리 | None 선행 분기에서 예외 대신 `ValidationFailure` 반환 |
| DEF-011 | Critical | AC-FR-01-01 | `grid=[]` / `3×4` / `[[]]*4` 각각 `execute(grid)` (`test_empty_list_resolve_never_called` 등) | `resolve.call_count == 0` | ERROR at setup (DEF-002) | Use case가 validator 없이 Domain 진입 | validator 실패 시 early return, spy `assert_not_called` |
| DEF-012 | Medium | AC-FR-01-01 | `pytest --cov=src` 실행 (RED 전체 스위트) | Boundary **≥85%**, Domain **≥95%** (NFR-01/02) | `src/boundary`, `src/control` **0%** (미존재) | AC-FR-01-01 대상 production 코드 없음 | DEF-001~004 해결 후 shape suite GREEN → cov 재측정 |

---

## Failure → Defect Mapping

| pytest 결과 | 건수 | 대표 원인 | 관련 Defect |
|---|---|---|---|
| ERROR (fixture setup) | 23 | `src.boundary` / `src.control` 미존재 | DEF-001, DEF-002 |
| FAILED (test body import) | 2 | `_validate()` 내부 `from src.boundary.validator` 실패 | DEF-001, DEF-009 |
| PASSED (scope/meta) | 5 | 테스트 스위트 구조 검증만 수행 | — (결함 아님) |

### ERROR 상세 (fixture 기준)

| 테스트 모듈 | ERROR 건수 | 실제 예외 |
|---|---|---|
| `tests/boundary/test_validator_shape_ac_fr_01_01.py` | 14 | `ModuleNotFoundError: No module named 'src.boundary'` |
| `tests/control/test_resolve_shape_guard_ac_fr_01_01.py` | 9 | `ModuleNotFoundError: No module named 'src.control'` |

### FAILED 상세

| 테스트 | 실제 예외 |
|---|---|
| `test_none_grid_returns_validation_failure_type` | `ModuleNotFoundError: No module named 'src.boundary'` (`_validate` import) |
| `test_invalid_size_message_byte_for_byte_equals_constant` | 동일 |

---

## 수정 우선순위 (GREEN 권장 순서)

1. **DEF-001** → `src/boundary/errors.py`, `validator.py` (pydantic 계약)
2. **DEF-003, DEF-005~008, DEF-010** → shape guard (`None`, `[]`, ragged, non-4×4)
3. **DEF-002, DEF-004, DEF-011** → `ResolveMagicSquareUseCase` + validator 연동·Domain 격리
4. **DEF-009** → `ValidationFailure` 타입 반환
5. **DEF-012** → 전체 스위트 GREEN 후 `pytest --cov=src --cov-report=term-missing`

---

## 회귀 확인 기준 (결함 종료)

- [ ] AC-FR-01-01 shape suite 30건 중 **구현 대상 25건** PASS (scope/meta 5건 유지)
- [ ] `grid=None` → `INVALID_SIZE` + `resolve()` **0회**
- [ ] Boundary coverage **≥85%**, Domain **≥95%** (전체 `--cov=src`)
- [ ] README **「모든 결함 수정 후 회귀 테스트 통과 확인」** 체크

---

## References

- `docs/test_plan.md` — TP-AC-FR-01-01
- `docs/PRD_MagicSquare.md` — FR-01, §13 Error Policy
- `README.md` — § RED 단계 To-Do 리스트
