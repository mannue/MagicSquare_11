# Defect List — Magic Square 4×4 (AC-FR-01-01)

| Meta | Value |
|---|---|
| **Document ID** | DL-AC-FR-01-01 |
| **Phase** | **GREEN** (shape suite + quality gate 완료) |
| **Last Updated** | 2026-05-29 |
| **Test Run** | `python -m pytest tests/boundary/test_validator_shape_ac_fr_01_01.py tests/control/test_resolve_shape_guard_ac_fr_01_01.py -v` |
| **Result Summary** | **30 collected — 30 PASSED** |
| **Coverage Run** | shape suite + `--cov=src/boundary --cov=src/control/use_cases --cov-fail-under=85` |
| **Coverage Summary** | Boundary **100%** · Control use_cases **87%** · in-scope TOTAL **94%** (`.coveragerc` omit `user.py`) |
| **Related AC** | AC-FR-01-01 (FR-01 / BR-01, PRD §8.1 `INVALID_SIZE`) |
| **Related Tests** | `tests/boundary/test_validator_shape_ac_fr_01_01.py`, `tests/control/test_resolve_shape_guard_ac_fr_01_01.py` |

> **Note:** `src/entity/models/user.py`는 마방진 범위 밖 연습 스캐폴드이며 `.coveragerc`에서 omit 합니다.  
> NFR-01 Domain **≥95%** 는 Entity rules 구현(Track B / FR-01~05) 후 전체 스위트로 재측정합니다.

---

## Defect Register

| ID | Severity | AC ID | 상태 | 수정 요약 |
|---|---|---|---|---|
| DEF-001 | Critical | AC-FR-01-01 | ✅ 해소 | `src/boundary/` 스캐폴드 (`validator.py`, `errors.py`) — **G-01** |
| DEF-002 | Critical | AC-FR-01-01 | ✅ 해소 | `src/control/use_cases/resolve_magic_square.py` — **G-05** |
| DEF-003 | Critical | AC-FR-01-01 | ✅ 해소 | `grid=None` → `ValidationFailure(INVALID_SIZE)` — **G-01** |
| DEF-004 | Critical | AC-FR-01-01 | ✅ 해소 | validator 선행, shape 실패 시 `resolve()` 미호출 — **G-05** |
| DEF-005 | High | AC-FR-01-01 | ✅ 해소 | `grid=[]` → `INVALID_SIZE` — **G-02** |
| DEF-006 | High | AC-FR-01-01 | ✅ 해소 | `[[]]*4` ragged → `INVALID_SIZE` — **G-04** |
| DEF-007 | High | AC-FR-01-01 | ✅ 해소 | 3×4 / 4×3 / 5×5 → `INVALID_SIZE` — **G-03** |
| DEF-008 | High | AC-FR-01-01 | ✅ 해소 | `INVALID_SIZE_MESSAGE` 상수 — **G-01** |
| DEF-009 | Medium | AC-FR-01-01 | ✅ 해소 | `ValidationFailure` pydantic 모델 — **G-01** |
| DEF-010 | Medium | AC-FR-01-01 | ✅ 해소 | `validate(None)` 예외 없이 실패 반환 — **G-01** |
| DEF-011 | Critical | AC-FR-01-01 | ✅ 해소 | invalid shape 전체 Domain 격리 — **G-06** |
| DEF-012 | Medium | AC-FR-01-01 | ✅ 해소 | cov 재측정 — Boundary **100%**, in-scope **94%**, gate **≥85% PASS** |

---

## Coverage Gate (DEF-012)

| Layer | Target (NFR) | Measured | Gate |
|---|---|---|---|
| `src/boundary` | ≥ 85% | **100%** | ✅ PASS |
| `src/control/use_cases` | ≥ 80% (권장) | **87%** | ✅ PASS |
| in-scope `src` (omit `user.py`) | ≥ 90% (README) | **94%** | ✅ PASS |
| `src/entity` rules (NFR-01) | ≥ 95% | 미구현 | ⏳ Track B GREEN 후 |

### 측정 명령

```bash
# AC-FR-01-01 품질 게이트 (fail-under 85)
python -m pytest tests/boundary/test_validator_shape_ac_fr_01_01.py tests/control/test_resolve_shape_guard_ac_fr_01_01.py \
  --cov=src/boundary --cov=src/control/use_cases --cov-report=term-missing --cov-report=html --cov-fail-under=85

# Boundary 단독
python -m pytest tests/boundary/test_validator_shape_ac_fr_01_01.py tests/control/test_resolve_shape_guard_ac_fr_01_01.py \
  --cov=src/boundary --cov-report=term-missing
```

### 미커버 라인 (의도적 — AC-FR-01-01 범위 밖)

| 파일 | 라인 | 사유 |
|---|---|---|
| `resolve_magic_square.py` | 26, 29 | validation 성공 시 Domain 진입 경로 — shape suite 미검증 (FR-01~05 GREEN 시 커버) |
| `validator.py` | 29 (`NotImplementedError`) | shape guard 이후 검증 — `.coveragerc` `exclude_lines` |

---

## 회귀 확인 기준 (결함 종료)

- [x] AC-FR-01-01 shape suite **30/30 PASS**
- [x] `grid=None` → `INVALID_SIZE` + `resolve()` **0회**
- [x] Boundary coverage **≥85%** (실측 **100%**)
- [x] in-scope TOTAL **≥90%** (실측 **94%**)
- [x] README 결함·커버리지 체크 반영
- [ ] NFR-01 Domain **≥95%** — Entity rules 구현 후 (프로젝트 게이트)

---

## References

- `docs/test_plan.md` — TP-AC-FR-01-01 §7~8
- `docs/PRD_MagicSquare.md` — FR-01, §13, NFR-01/02
- `.coveragerc` — omit `user.py`, `NotImplementedError` exclude
- `README.md` — AC-FR-01-01 GREEN 로드맵·품질 게이트
