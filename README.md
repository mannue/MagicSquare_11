# Magic Square 4x4 TDD Practice

## 1. Project Start Declaration

**MagicSquare_XX** 저장소에서 시작하는 것은 4×4 마방진 **도메인 구현**이 아니라, PRD(`docs/PRD_MagicSquare.md`)에 고정된 **입력/출력 계약·도메인 불변식·Dual-Track TDD·ECB(Clean Architecture)** 를 따라 **RED → GREEN → REFACTOR** 루프를 학습하는 TDD 실습입니다.

**현재 단계:** AC-FR-01-01 shape suite RED 완료(Report/08) → **TDD GREEN 진행 중** (`stabilize/green` 브랜치). Track A **G-01**(`grid=None`)·**G-02**(`grid=[]`) 완료, G-03~G-06 대기.

**RED 정의:** 실패하는 테스트를 작성하고, `pytest`로 실행한 뒤, **의도한 요구사항·규칙 위반 때문에** 실패했음을 확인하는 단계입니다. RED 확인 전 production 구현을 시작하지 않습니다.

본 README는 구현 전 **개발 방향·추적 구조·품질 게이트**를 고정하는 문서입니다. Scenario → AC → RED Test ID → Test Skeleton → Expected RED Failure → GREEN Task → REFACTOR Candidate 체인을 따라 작업합니다.

**범위 구분:** `src/entity/models/user.py`, `tests/entity/test_user.py`는 ECB·pytest **연습용 User 엔티티 스캐폴드**이며, **마방진 도메인 범위 밖**입니다. 마방진 RED 테스트는 `tests/boundary/`, `tests/control/`, `tests/entity/rules/` 등 별도 경로에서 시작합니다.

---

## 2. PRD Summary

### 프로젝트 목적

알고리즘 난이도보다 **불변식 기반 사고**, **입력/출력 계약 고정**, **Dual-Track TDD**, **ECB 계층 분리**, **Concept-to-Code Traceability** 훈련을 목표로 합니다. 핵심은 "마방진을 만든다"가 아니라 **규칙 만족 판정과 계약 준수**입니다.

### 학습 목표

- Track A(Boundary): 입력 검증, 출력 계약, 오류 응답, Domain 미호출 검증
- Track B(Domain/Logic): 빈칸·누락 숫자·합 34·Solver 조합 시도
- RED 확인 후 최소 구현(GREEN), 이후 구조 개선(REFACTOR) 분리
- 요구사항(FR/BR) ↔ 시나리오 ↔ 테스트 ↔ 컴포넌트 추적

### 핵심 도메인 규칙 (BR 요약)

| ID | 규칙 |
|---|---|
| BR-01 | 입력은 항상 4×4 정수 행렬 |
| BR-02 | 빈칸 `0`은 정확히 2개 |
| BR-03 | 값은 `0` 또는 `1..16` |
| BR-04 | `0`을 제외한 숫자 중복 금지 |
| BR-05 | 첫 번째 빈칸은 row-major 스캔 기준 |
| BR-06 | 누락 숫자는 정확히 2개 |
| BR-07 | 누락 숫자 쌍은 오름차순 `[small, large]` |
| BR-08 | 마방진 상수 = **34** |
| BR-09 | 유효 마방진: 모든 행·열·대각선 합 = 34 |
| BR-10 | 출력 좌표는 1-index (1..4) |
| BR-11 | 성공 출력: `int[6] = [r1,c1,n1,r2,c2,n2]` |

### 입력/출력 계약

| 항목 | 규칙 |
|---|---|
| 입력 | `int[4][4]`, `0`=빈칸(정확히 2개), 값 `0` 또는 `1..16`, 0 제외 중복 금지 |
| 출력(성공) | `int[6]`, `[r1,c1,n1,r2,c2,n2]`, 좌표 1-index |
| 빈칸 순서 | row-major로 처음 발견되는 `0`이 첫 빈칸 |
| 누락 숫자 | `1..16` 중 보드에 없는 2개, 오름차순 `[small, large]` |
| Solver | 시도 1: small→첫 빈칸, large→둘째 빈칸 → 마방진 검증; 실패 시 시도 2: 반대 조합 |
| 도메인 실패 | 두 조합 모두 실패 → `E_UNSOLVABLE_COMBINATION` (입력 오류 아님) |
| Boundary 실패 | 입력 검증 실패 시 **Domain resolver 미호출** |

### 성공 기준

- **판정:** 완성 보드의 행·열·대각선 합이 모두 34일 때만 valid
- **계약 준수:** 입력/출력 형식·좌표·오류 코드가 PRD §12·§13과 일치
- **Dual-Track 병행:** Boundary RED와 Domain RED를 분리해 각각 RED → GREEN → REFACTOR 진행 (Domain 전부 선구현 후 Boundary 연결 금지, PRD §15.3)

---

## 3. TDD Development Flow

```
Scenario → Acceptance Criteria → RED Test ID → Test Skeleton
  → Run Test → Confirm Failure (= RED)
  → Minimal Implementation (= GREEN) → Structure Improvement (= REFACTOR)
```

| 단계 | 설명 |
|---|---|
| **Scenario** | Report/06·PRD에서 식별한 기술 시나리오(SC-*). 한 시나리오는 하나의 검증 가능 행위를 표현합니다. |
| **Acceptance Criteria** | Given/When/Then 또는 검증 가능 한 문장으로 "통과 조건"을 고정합니다. |
| **RED Test ID** | `TRED-*` 식별자로 테스트를 추적합니다. PRD §21 Traceability Matrix와 연결합니다. |
| **Test Skeleton** | pytest + AAA 패턴의 실패 테스트 골격을 작성합니다. 구현 코드는 아직 없거나 불충분합니다. |
| **Run Test** | `python -m pytest`로 실행합니다. (`pyproject.toml` 미구성 — 프로젝트 규칙상 pytest 사용 예정) |
| **Confirm Failure = RED** | `AssertionError`, `ModuleNotFoundError`, `AttributeError` 등 **의도한 이유**로 실패했음을 확인합니다. |
| **Minimal Implementation = GREEN** | 현재 RED 하나를 통과시키는 **최소** production 코드만 추가합니다. |
| **Structure Improvement = REFACTOR** | GREEN 이후 동작을 바꾸지 않고 이름·중복·모듈 경계를 개선합니다. (본 README에서는 후보만 기록) |

---

## 4. Development Methodology

### Dual-Track TDD

| Track | 초점 | 대표 시나리오 |
|---|---|---|
| **Track A — Boundary** | 입력 검증, 출력 형식, 오류 응답, Domain 미호출 | SC-BND-VAL-*, SC-BND-OUT-* |
| **Track B — Domain/Logic** | 빈칸·누락·합 34·Solver 조합 | SC-DOM-BLK-*, SC-DOM-MISS-*, SC-DOM-VAL-*, SC-DOM-SOL-* |

UI RED와 Logic RED를 **분리**하고, 각 트랙을 **최소 구현**으로 GREEN한 뒤 REFACTOR합니다.

### ECB 역할 분리

- **Entity:** 순수 도메인 규칙·상태 (BlankFinder, MissingNumberFinder, MagicSquareValidator, Solver)
- **Control:** Use case orchestration — Boundary와 Entity 흐름 조정
- **Boundary:** 외부 입출력 계약 — 입력 검증, 결과 포맷, 오류 매핑 (Domain Invariant 직접 구현 금지)

의존 방향: `Boundary → Control → Entity`. Entity는 Boundary/Control/UI/DB/Web/파일 시스템에 의존하지 않습니다.

### Concept-to-Code Traceability

```
Concept / Invariant → Business Rule → FR → AC → Scenario ID → RED Test ID → Component → Code Target
```

Tracking Board(§6)가 이 체인의 실행 보드입니다.

### RED → GREEN → REFACTOR 원칙

- RED: 실패 확인 전 구현 금지
- GREEN: 현재 테스트 하나를 통과하는 최소 코드만
- REFACTOR: 관찰 가능한 동작 변경 없이 구조 개선
- 테스트 약화·삭제로 GREEN 달성 금지

### 병행 진행 규칙 (PRD §15.3)

- Domain 전부 선구현 후 Boundary 연결 방식 **금지**
- Track A/B 각각 RED → GREEN → REFACTOR
- 입력 검증 실패 시 Domain resolver **미호출** (Boundary 테스트에서 mock/spy로 검증)

---

## 5. ECB Role Separation

| ECB Layer | Responsibility | Example Component |
|---|---|---|
| **Entity** | Board 상태, 순수 도메인 규칙 — 빈칸 탐색, 누락 숫자, 마방진 판정, 조합 시도 | `BlankFinder`, `MissingNumberFinder`, `MagicSquareValidator`, `Solver`, `Board` (PRD §18) |
| **Control** | 검증·해 결정 흐름 조정, Boundary↔Entity 연결 | `ResolveMagicSquareUseCase`, `SolverService` (`src/control/use_cases/`) |
| **Boundary** | 입력 검증, 출력 `int[6]` 포맷, 오류 코드 매핑 — **Domain Invariant 직접 구현 금지** | `BoundaryValidator`, `ResultFormatter` (`src/boundary/`) |

**제약:** Entity는 UI/DB/Web/파일 시스템에 의존하지 않습니다. Boundary는 Entity를 직접 호출하지 않고 Control을 경유합니다.

---

## 6. Scenario → AC → RED → GREEN Tracking Board

> **Status 초기값:** `RED-PENDING` — Test Skeleton 미작성·RED 미확인 상태  
> **Note:** `tests/entity/test_user.py`는 마방진 범위 밖(연습 스캐폴드)입니다.

| Status | Scenario ID | Scenario Summary | Acceptance Criteria | RED Test ID | Test Skeleton Candidate | Expected RED Failure | GREEN Task Candidate | REFACTOR Candidate | ECB Layer | Code Target |
|---|---|---|---|---|---|---|---|---|---|---|
| RED-PENDING | SC-BND-VAL-000 | None 입력 | **Given** board=`None` **When** BoundaryValidator 검증 **Then** 즉시 실패, Domain 미호출, 타입/형상 오류 반환 | TRED-BND-000 | `tests/boundary/test_validator.py::test_none_input_rejects_without_domain_call` | `TypeError` 또는 `AssertionError`(검증 실패/`E_INVALID_SHAPE` 미반환) | `BoundaryValidator.validate()`에 `None` 거부 분기 + 오류 코드 반환 stub | 오류 코드 enum·메시지 팩토리 분리 | Boundary | `src/boundary/validator.py`, `tests/boundary/test_validator.py` |
| RED-PENDING | SC-BND-VAL-004 | 4×4가 아닌 입력 | **Given** 3×4 또는 4×3 행렬 **When** 검증 **Then** `E_INVALID_SHAPE`, Domain 미호출 | TRED-BND-001 | `tests/boundary/test_validator.py::test_invalid_shape_rejects_3x4` | `ModuleNotFoundError` / `ImportError` 또는 shape 검증 미구현 `AssertionError` | shape(4×4) 검사 최소 로직 | 검증 규칙을 개별 private validator로 분리 | Boundary | `src/boundary/validator.py` |
| RED-PENDING | SC-BND-VAL-001 | 빈칸 개수 오류 | **Given** `0`이 1개 또는 3개인 4×4 **When** 검증 **Then** `E_INVALID_BLANK_COUNT`, Domain 미호출 | TRED-BND-002 | `tests/boundary/test_validator.py::test_invalid_blank_count_not_two` | `AssertionError: ... E_INVALID_BLANK_COUNT` | `0` 개수==2 검사 추가 | blank count 규칙을 `BlankCountRule`로 추출 | Boundary | `src/boundary/validator.py` |
| RED-PENDING | SC-BND-VAL-003 | 값 범위 오류 | **Given** `-1` 또는 `17` 포함 보드 **When** 검증 **Then** `E_INVALID_VALUE_RANGE`, Domain 미호출 | TRED-BND-003 | `tests/boundary/test_validator.py::test_invalid_value_range_outside_0_to_16` | `AssertionError`(범위 위반 미검출) | 셀 값 `0 or 1..16` 검사 추가 | ValueRangeRule 단위 테스트 가능 구조로 분리 | Boundary | `src/boundary/validator.py` |
| RED-PENDING | SC-BND-VAL-002 | 중복 숫자 오류 | **Given** 0 제외 동일 숫자 2회 **When** 검증 **Then** `E_DUPLICATE_NON_ZERO`, Domain 미호출 | TRED-BND-004 | `tests/boundary/test_validator.py::test_duplicate_non_zero_values_rejected` | `AssertionError`(중복 미검출) | non-zero set 크기 검사 추가 | 중복 검사를 `UniquenessRule`로 분리 | Boundary | `src/boundary/validator.py` |
| RED-PENDING | SC-DOM-BLK-001 | 빈칸 좌표 row-major 탐색 | **Given** 유효 4×4에 `0` 2개 **When** BlankFinder 실행 **Then** row-major 첫·둘째 `(row,col)` 0-index 반환 | TRED-DOM-001 | `tests/entity/test_blank_finder.py::test_finds_blanks_in_row_major_order` | `ModuleNotFoundError` / 좌표 불일치 `AssertionError` | row-major 스캔으로 빈칸 2좌표 반환 | `Board` 순회 유틸과 Finder 분리 | Entity | `src/entity/rules/blank_finder.py` |
| RED-PENDING | SC-DOM-MISS-001 | 누락 숫자 오름차순 탐색 | **Given** 유효 보드 **When** MissingNumberFinder 실행 **Then** `1..16` 중 absent 2개를 `[small, large]`로 반환 | TRED-DOM-002 | `tests/entity/test_missing_number_finder.py::test_missing_numbers_ascending_pair` | `AssertionError`(순서·값 오류) | present set 차집합 + sort `[small,large]` | 1..16 전域 생성을 상수/팩토리로 공유 | Entity | `src/entity/rules/missing_number_finder.py` |
| RED-PENDING | SC-DOM-VAL-001 | 모든 행 합 34 검증 | **Given** 완성 4×4 **When** MagicSquareValidator 행 검사 **Then** 4행 모두 34일 때만 pass | TRED-DOM-003 | `tests/entity/test_magic_square_validator.py::test_all_rows_sum_to_magic_constant` | `AssertionError`(행 합 불일치 미검출) | 행별 합==`MAGIC_CONSTANT(34)` 검사 | `LineSumChecker` 추출 | Entity | `src/entity/rules/magic_square_validator.py` |
| RED-PENDING | SC-DOM-VAL-002 | 모든 열 합 34 검증 | **Given** 완성 4×4 **When** 열 검사 **Then** 4열 모두 34일 때만 pass | TRED-DOM-004 | `tests/entity/test_magic_square_validator.py::test_all_columns_sum_to_magic_constant` | `AssertionError`(열 합 불일치 미검출) | 열별 합 검사 추가 | 행/열 공통 sum helper 통합 | Entity | `src/entity/rules/magic_square_validator.py` |
| RED-PENDING | SC-DOM-VAL-003 | 두 대각선 합 34 검증 | **Given** 완성 4×4 **When** 대각선 검사 **Then** 주·부 대각선 합 모두 34일 때만 pass | TRED-DOM-005 | `tests/entity/test_magic_square_validator.py::test_both_diagonals_sum_to_magic_constant` | `AssertionError`(대각선 합 오류) | 주·부 대각선 합 검사 추가 | diagonal index helper 추출 | Entity | `src/entity/rules/magic_square_validator.py` |
| RED-PENDING | SC-DOM-SOL-002 | small-first 성공 | **Given** 유효 보드·누락 `[s,l]` **When** Solver 시도1(s→blank1, l→blank2) **Then** 마방진이면 해당 배치 즉시 성공 | TRED-SLV-001 | `tests/entity/test_solver.py::test_small_first_combination_succeeds` | `AssertionError`(성공 배치·순서 불일치) | Attempt1 채우기 + validator 호출 최소 구현 | Solver 전략 객체(`SmallFirstStrategy`) 분리 | Entity/Control | `src/entity/rules/solver.py`, `src/control/use_cases/resolve_magic_square.py` |
| RED-PENDING | SC-DOM-SOL-001 | small-first 실패 후 reverse 성공 | **Given** Attempt1 invalid **When** Attempt2(l→blank1, s→blank2) **Then** valid이면 reverse 순서로 성공 | TRED-SLV-002 | `tests/entity/test_solver.py::test_reverse_combination_succeeds_after_small_first_fails` | `AssertionError`(reverse 미시도 또는 순서 오류) | Attempt2 fallback + 성공 시 reverse 순서 반환 | attempt loop를 `CombinationAttemptPolicy`로 추출 | Entity/Control | `src/entity/rules/solver.py` |
| RED-PENDING | SC-DOM-SOL-003 | 두 조합 모두 실패 | **Given** 두 배치 모두 invalid **When** Solver 실행 **Then** `E_UNSOLVABLE_COMBINATION` (입력 오류 아님) | TRED-SLV-003 | `tests/entity/test_solver.py::test_both_combinations_unsolvable` | `AssertionError`(unsolvable 미반환/예외 타입 불일치) | unsolvable 결과 타입/코드 반환 stub | DomainFailure vs BoundaryError 타입 계층 정리 | Entity/Control | `src/entity/rules/solver.py`, `src/boundary/error_mapper.py` |
| RED-PENDING | SC-BND-OUT-001 | 결과 배열 길이 6 | **Given** Solver 성공 배치 **When** ResultFormatter 포맷 **Then** `len(result)==6` | TRED-BND-OUT-001 | `tests/boundary/test_result_formatter.py::test_success_result_has_length_six` | `AssertionError: len(...) != 6` | `[r1,c1,n1,r2,c2,n2]` 6-tuple/list 생성 stub | formatter 입력 DTO 도입 | Boundary | `src/boundary/result_formatter.py` |
| RED-PENDING | SC-BND-OUT-002 | 반환 좌표 1-index | **Given** 0-index blank `(0,1)` **When** 포맷 **Then** 출력 `(1,2,...)` — 모든 r,c ∈ 1..4 | TRED-BND-OUT-002 | `tests/boundary/test_result_formatter.py::test_coordinates_are_one_indexed` | `AssertionError`(0-index 그대로 반환) | 좌표 +1 변환 최소 로직 | index 변환을 `CoordinateConverter`로 분리 | Boundary | `src/boundary/result_formatter.py` |

---

## 7. RED Start Checklist

RED 단계 착수·확인 전 아래 항목을 점검합니다.

- [ ] Tracking Board에서 대상 **Scenario ID**가 확정되었는가?
- [ ] **Acceptance Criteria**가 Given/When/Then 또는 검증 가능 한 문장으로 작성되었는가?
- [ ] **RED Test ID**(`TRED-*`)가 PRD §21·§23 및 §6 보드와 일치하는가?
- [ ] **ECB Layer**가 확정되었고, Boundary/Entity 책임 혼합이 없는가?
- [ ] **Code Target** 경로(`src/...`, `tests/...`)가 정해졌는가?
- [ ] **Test Skeleton**이 pytest + AAA 패턴으로 작성되었는가?
- [ ] 해당 시나리오에 대한 **production 구현이 RED 확인 전에 추가되지 않았는가?**
- [ ] `python -m pytest <target>` 실행 시 **의도한 이유**로 실패하는가?
- [ ] **Expected RED Failure** 유형(`AssertionError`, `ImportError` 등)과 실제 실패가 일치하는가?
- [ ] Boundary 입력 오류 시나리오에서 **Domain resolver 미호출**을 검증할 계획(또는 mock/spy)이 있는가?
- [ ] 테스트 **약화·삭제 없이** RED를 확인했는가?
- [ ] **PRD**(`docs/PRD_MagicSquare.md`)와 Tracking Board 시나리오가 일치하는가?
- [ ] **User 스캐폴드**(`test_user.py`)와 마방진 RED 테스트가 혼동되지 않았는가?

---

## AC-FR-01-01 GREEN 로드맵

> **기준 스위트:** `tests/boundary/test_validator_shape_ac_fr_01_01.py` (20) + `tests/control/test_resolve_shape_guard_ac_fr_01_01.py` (10) = **30건**  
> **GREEN 대상:** 구현 필요 **23건** | **메타/범위 7건** — production 없이 항상 PASS (커밋 불필요)  
> **정렬:** 인프라 → 입력 단순도(`None` → `[]` → 비-4×4 → ragged) → 검증 강도 → Track B  
> **상수 SSOT:** `tests/conftest.py` — `INVALID_SIZE_CODE`, `INVALID_SIZE_MESSAGE`

### 커밋 묶음 진행 현황

| 커밋 | 범위 | 테스트 수 | 상태 | 구현 요약 |
|---|---|---:|---|---|
| **G-01** | Track A — `grid=None` | 8 | ✅ GREEN | `src/boundary/` + `if grid is None: return ValidationFailure` |
| **G-02** | Track A — `grid=[]` | 2 | ✅ GREEN | `grid is None or len(grid) != 4` → `INVALID_SIZE` |
| **G-03** | Track A — 3×4 / 4×3 / 5×5 | 4 | 🔴 RED | `all(len(r)==4)` 열 guard (3×4·5×5는 G-02 row guard로 선통과) |
| **G-04** | Track A — `[[]]*4` ragged | 2 | 🔴 RED | `len(row) != 4` (G-03 guard로 커버) |
| **G-05** | Track B — Control + `None` 격리 | 4 (+fixture) | 🔴 ERROR | `src/control/use_cases/resolve_magic_square.py` — validator 선행, `resolve()` 0회 |
| **G-06** | Track B — 나머지 shape 격리 | 4 | 🔴 ERROR | G-02~G-05 orchestration 재사용 |
| *(메타)* | 범위/구조 검증 | 7 | ✅ PASS | 커밋 불필요 |

**pytest 현황 (G-02 이후):** Boundary **17 PASS** / **3 FAIL** | Control **1 PASS** / **9 ERROR** | 합계 **18/30 PASS**

### GREEN 오름차순 전체 목록 (#01 ~ #26)

| GREEN # | Track | 클래스 | 테스트 | 입력 | 새로 필요한 구현 | 커밋 |
|--------:|-------|--------|--------|------|------------------|------|
| 01 | A | `TestAcFr0101NormalFailureReturn` | `test_none_grid_returns_failure_not_success` | `None` | `grid is None` → `success=False` | G-01 ✅ |
| 02 | A | ↑ | `test_none_grid_returns_code_invalid_size` | `None` | `error.code=INVALID_SIZE` | G-01 ✅ |
| 03 | A | ↑ | `test_none_grid_returns_message_grid_must_be_4x4` | `None` | `error.message` 상수 | G-01 ✅ |
| 04 | A | ↑ | `test_none_grid_returns_validation_failure_type` | `None` | `ValidationFailure` pydantic 모델 | G-01 ✅ |
| 05 | A | ↑ | `test_none_grid_does_not_raise_type_error_on_validate` | `None` | None 선행 분기(예외 X) | G-01 ✅ |
| 06 | A | `TestAcFr0101MessageExactMatch` | `test_none_grid_message_exact_match_prd_8_1` | `None` | (G-01과 동일) | G-01 ✅ |
| 07 | A | ↑ | `test_invalid_size_message_byte_for_byte_equals_constant` | `None` | (G-01과 동일) | G-01 ✅ |
| 08 | A | `TestAcFr0101ScopeLimit` | `test_scope_forbidden_error_codes_not_used_as_expected_pass` | `None` | (G-01과 동일) | G-01 ✅ |
| 09 | A | `TestAcFr0101BoundaryValues` | `test_empty_list_grid_returns_invalid_size_failure` | `[]` | `len(grid) != 4` | G-02 ✅ |
| 10 | A | `TestAcFr0101MessageExactMatch` | `test_empty_list_message_exact_match_prd_8_1` | `[]` | (G-02와 동일) | G-02 ✅ |
| 11 | A | `TestAcFr0101BoundaryValues` | `test_3x4_grid_returns_invalid_size_failure` | 3×4 | `rows==4 ∧ cols==4` | G-03 |
| 12 | A | ↑ | `test_4x3_grid_returns_invalid_size_failure` | 4×3 | (G-03과 동일) | G-03 |
| 13 | A | ↑ | `test_5x5_grid_returns_invalid_size_failure` | 5×5 | (G-03과 동일) | G-03 |
| 14 | A | `TestAcFr0101MessageExactMatch` | `test_3x4_message_exact_match_prd_8_1` | 3×4 | (G-03과 동일) | G-03 |
| 15 | A | `TestAcFr0101BoundaryValues` | `test_four_empty_rows_grid_returns_invalid_size_failure` | `[[]]*4` | `len(row) != 4` | G-04 |
| 16 | A | `TestAcFr0101MessageExactMatch` | `test_four_empty_rows_message_exact_match_prd_8_1` | `[[]]*4` | (G-04와 동일) | G-04 |
| 17 | B | — | *(fixture)* `resolve_use_case` | — | `src/control/...` 스캐폴드 | G-05 선행 |
| 18 | B | `TestAcFr0101DomainIsolation` | `test_none_grid_resolve_call_count_is_zero` | `None` | `execute` → validator, `resolve()` 0회 | G-05 |
| 19 | B | ↑ | `test_none_grid_use_case_returns_invalid_size_without_resolve` | `None` | 실패 응답 + spy | G-05 |
| 20 | B | ↑ | `test_none_grid_run_domain_patch_assert_not_called` | `None` | `_run_domain` 미호출 | G-05 |
| 21 | B | `TestAcFr0101ResolveContractIsolation` | `test_boundary_handles_none_before_resolve_invoked` | `None` | (G-05와 동일) | G-05 |
| 22 | B | `TestAcFr0101DomainIsolation` | `test_empty_list_resolve_never_called` | `[]` | shape guard 연동 | G-06 |
| 23 | B | ↑ | `test_3x4_grid_resolve_never_called` | 3×4 | (G-06과 동일) | G-06 |
| 24 | B | `TestAcFr0101ResolveContractIsolation` | `test_4x3_grid_resolve_call_count_is_zero` | 4×3 | (G-06과 동일) | G-06 |
| 25 | B | ↑ | `test_5x5_grid_resolve_never_called` | 5×5 | (G-06과 동일) | G-06 |
| 26 | B | ↑ | `test_four_empty_rows_resolve_call_count_is_zero` | `[[]]*4` | (G-06과 동일) | G-06 |

**메타 7건 (커밋 불필요, 이미 PASS):** `test_scope_module_docstring_declares_ac_fr_01_01_only`, `test_scope_shape_suite_does_not_import_blank_finder`, `test_scope_shape_suite_does_not_import_solver`, `test_scope_no_valid_4x4_shape_failure_test_in_module`, `test_scope_ac_fr_01_02_to_05_cases_not_in_control_shape_module` 등 범위·구조 검증.

### 커밋별 pytest 명령 (검증용)

```bash
# G-01 ✅
python -m pytest tests/boundary/test_validator_shape_ac_fr_01_01.py::TestAcFr0101NormalFailureReturn -v

# G-02 ✅
python -m pytest tests/boundary/test_validator_shape_ac_fr_01_01.py -k "empty_list" -v

# G-03
python -m pytest tests/boundary/test_validator_shape_ac_fr_01_01.py -k "3x4 or 4x3 or 5x5" -v

# G-04
python -m pytest tests/boundary/test_validator_shape_ac_fr_01_01.py -k "four_empty_rows" -v

# G-05
python -m pytest tests/control/test_resolve_shape_guard_ac_fr_01_01.py -k "none_grid" -v

# G-06
python -m pytest tests/control/test_resolve_shape_guard_ac_fr_01_01.py -k "empty_list or 3x4 or 4x3 or 5x5 or four_empty_rows" -v

# 회귀 (AC-FR-01-01 shape suite 전체)
python -m pytest tests/boundary/test_validator_shape_ac_fr_01_01.py tests/control/test_resolve_shape_guard_ac_fr_01_01.py -v
```

---

## RED / GREEN To-Do 리스트

> RED 체크리스트: @docs/test_plan.md 기반. GREEN 진행 시 아래 **G-** 커밋 번호와 연동합니다.

### Track A — Boundary (AC-FR-01-01)

- [x] TC-A-01: `grid=None` → 실패 결과 반환 — **G-01** ✅
- [x] TC-A-02: `code == "INVALID_SIZE"` — **G-01** ✅
- [x] TC-A-03: `message == "Grid must be 4x4."` 문자 단위 일치 — **G-01** ✅
- [ ] TC-A-04: `grid=None` 시 Domain 진입점 0회 호출 — **G-05**
- [x] TC-A-05: `grid=[]` → 실패 — **G-02** ✅
- [ ] TC-A-06: 3×4 / 4×3 / 5×5 → 실패 — **G-03**, **G-04**
- [x] TC-A-07: 반환 타입 `ValidationFailure` — **G-01** ✅

### Track B — Control / Domain 격리 (AC-FR-01-01)

- [ ] TC-B-01: `resolve()`가 `None` grid를 직접 처리하지 않음 — **G-05**
- [ ] TC-B-02: Boundary shape guard 후 `resolve()` 미호출 — **G-05**, **G-06**
- [ ] TC-B-03: `resolve()` mock 호출 시 테스트 실패 — **G-05**, **G-06**
- [x] TC-B-04: AC-FR-01-02~05 범위 미포함 확인 (메타 테스트 PASS)

### 커버리지 목표 (G-06 완료 후 측정)

- [ ] Domain Logic: 95%+ (`pytest --cov=src`)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결

- [x] `docs/defect_list.md` 생성 및 발견 결함 기록
- [x] DEF-001 해소 — `src/boundary/` 스캐폴드 (**G-01**)
- [x] DEF-003 해소 — `grid=None` → `INVALID_SIZE` (**G-01**)
- [x] DEF-005 해소 — `grid=[]` → `INVALID_SIZE` (**G-02**)
- [ ] DEF-002, DEF-004, DEF-006~012 — **G-03**~**G-06** 대기
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인 (shape suite 25건 GREEN 목표)

---

## 8. Quality Gates

| 게이트 | 기준 | 출처 |
|---|---|---|
| Domain Logic coverage | **95%+** | PRD NFR-01 |
| Boundary Validation coverage | **85%+** | PRD NFR-02 |
| 테스트 프레임워크 | **pytest**, AAA 패턴 | `.cursor/rules/magicsquare-tdd-testing.mdc` |
| 테스트 무결성 | 테스트 약화·삭제로 GREEN 금지 | PRD §15.3, §20 |
| 디버깅 | production 코드 `print()` 금지 | `.cursor/rules/magicsquare-forbidden.mdc` |
| Magic number | 설명 없는 magic number 금지 — **34는 명명 상수** (`MAGIC_CONSTANT` 등) | PRD NFR-07, forbidden rules |
| 타입·스타일 | type hints 필수, PEP 8, line length **88** | `.cursor/rules/magicsquare-python-code-style.mdc` |
| 예외 처리 | bare `except` 금지 | forbidden rules |
| 계약 불변 | 입력/출력 계약 변경 금지 | PRD §12, §16.3 |
| 입력 불변 | 입력 행렬 **원본 변경 금지** (NFR-04) | PRD NFR-04 |
| 결정성 | 동일 입력 → 동일 출력 (NFR-03) | PRD NFR-03 |
| ECB 분리 | Boundary/Domain 책임 혼합 금지 | PRD NFR-06, ECB rules |
| 실행 환경 | Python **3.13.13** | project rules |
| 빌드 설정 | `pyproject.toml` **미구성** — pytest는 프로젝트 규칙상 사용 예정 (`python -m pytest`) | Report/03 |

---

## 9. Reference Documents

| 문서 | 역할 |
|---|---|
| `docs/PRD_MagicSquare.md` | FR/BR, 입출력 계약, 오류 정책, Dual-Track TDD, Traceability Matrix, TRED-* 후보 — **1차 실행 기준** |
| `docs/defect_list.md` | RED 단계 결함 등록·추적 (AC-FR-01-01, DEF-001~012) |
| `docs/test_plan.md` | AC-FR-01-01 테스트 계획서 |
| `Report/08.MagicSquare_AC-FR-01-01-RED-Test-and-Defect_Report.md` | AC-FR-01-01 RED 테스트·결함 등록 실행 보고 |
| `Report/12.MagicSquare_AC-FR-01-01-GREEN-None-Grid_Report.md` | AC-FR-01-01 GREEN G-01 (`grid=None`) 실행 보고 |
| `Prompt/08.MagicSquare_AC-FR-01-01-RED-Test-and-Defect_Prompt-Transcript.md` | RED 세션 Transcript |
| `Prompt/12.MagicSquare_AC-FR-01-01-GREEN-None-Grid_Prompt-Transcript.md` | GREEN G-01 세션 Transcript |
| `Report/01.MagicSqure_Problem-Definition-Report.md` | STEP 1~5 문제 정의, Invariant, Why Chain, "판정 vs 완성" 관점 |
| `Report/02.MagicSquare_4x4_Dual-Track-TDD-CleanArchitecture-Report.md` | Dual-Track, Layer Boundary, 입출력 계약, 오류 정책, Invariant 설계 |
| `Report/03.MagicSquare_CursorRules-Entity-Implementation-Report.md` | 개발 환경, ECB, TDD, pytest, User Entity 스캐폴드 |
| `Report/04.MagicSquare_Rules-Refactor-Export-Report.md` | `.cursorrules` → `.cursor/rules/*.mdc` 분리 이력 |
| `Report/05.Agent-Setup-and-Backup-Execution_Report.md` | 에이전트·백업 운영 (README 핵심 흐름 보조) |
| `Report/06.MagicSquare_Level1-5-Scenario-Verification-Report.md` | Epic → Journey → Story → Technical Scenario, SC-* ID, 보강 권고 |
| `Report/07.PRD-Authoring-and-Review-Execution_Report.md` | PRD 작성·리뷰 이력, 알려진 모순/보완점 |
| `.cursorrules` | Cursor Rules 인덱스 — 실제 규칙은 `.cursor/rules/` 참조 |
| `.cursor/rules/magicsquare-project.mdc` | 프로젝트 컨텍스트, TDD·ECB 작업 전후 규칙 |
| `.cursor/rules/magicsquare-ecb-architecture.mdc` | ECB 계층 책임·의존 방향·디렉터리 구조 |
| `.cursor/rules/magicsquare-tdd-testing.mdc` | RED/GREEN/REFACTOR, pytest, AAA, fixture scope |
| `.cursor/rules/magicsquare-python-code-style.mdc` | Python 3.13.13, PEP8, type hints, line length 88 |
| `.cursor/rules/magicsquare-forbidden.mdc` | `print()`, bare except, 하드코딩 상수 금지 |

---

## 10. Current Project Status

| 항목 | 상태 |
|---|---|
| **현재 단계** | AC-FR-01-01 **TDD GREEN 진행 중** — G-01·G-02 완료, G-03~G-06 대기 |
| **브랜치** | `stabilize/green` (`origin` push 완료, 커밋 `2128905`) |
| **AC-FR-01-01 shape suite** | **18/30 PASS** (G-01: `None` 8건 + G-02: `[]` 2건 + 메타 5건 + Control 메타 1건; Boundary 3건·Control 9건 미통과) |
| **존재하는 production 코드** | `src/boundary/` (`errors.py`, `validator.py`) — `grid is None`·`len(grid) != 4` 분기 |
| **미구현** | `src/control/` (Track B), 열 guard(`4×3`·ragged), Entity rules |
| **연습 스캐폴드** | `src/entity/models/user.py`, `tests/entity/test_user.py` (**마방진 범위 밖**) |
| **FR-01~05 Skeleton** | `test_u_*_red.py`, `test_d_*_red.py` — 24건 `pytest.fail` (shape suite GREEN 후 진행) |
| **미구성** | `pyproject.toml` 없음 — `python -m pytest` + `requirements.txt` |
| **다음 GREEN 커밋** | **G-03** — `all(len(r)==4)` 열 guard (`4×3`·`[[]]*4`, 4+2건) |

---

*README 갱신: AC-FR-01-01 GREEN G-02(`grid=[]`) 완료 반영. Tracking Board Status는 RED `RED-CONFIRMED` → GREEN `GREEN` → REFACTOR `DONE`으로 갱신합니다.*
