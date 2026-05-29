# PRD — Magic Square 4x4 TDD Practice

## 1. Executive Summary

Magic Square 4x4 프로젝트는 알고리즘 구현 자체보다 불변식 기반 사고, 입력/출력 계약 고정, Dual-Track TDD(Track A: Boundary Contract, Track B: Domain Invariant) 훈련을 목표로 한다. 본 PRD는 구현 전 기준 문서로서 요구사항, 도메인 규칙, 실패 정책, 검증 계획, 추적성 매트릭스를 통해 설계 → 테스트 → 구현 → 리팩토링 흐름의 일관성을 보장한다.

## 2. Background

현재 문제의 핵심은 "마방진을 만든다"가 아니라, 4x4 격자 입력이 규칙을 만족하는지 명시된 기준으로 일관되게 판정하고 재현 가능하게 유지하는 것이다. 학습 과정에서 빈번하게 발생하는 구현 선행, 기준 없는 테스트, 경계와 도메인 책임 혼합을 방지하기 위해 PRD 수준에서 계약과 불변식을 먼저 고정한다.

## 3. Problem Statement

문제는 4x4 입력(`int[][]`)과 출력(`int[6]`) 계약을 중심으로, 검증 가능한 도메인 불변식을 만족하는 결과를 산출하는 것이다. 따라서 해결 대상은 "결과 생성"이 아니라 "규칙 만족 판정과 계약 준수"이며, 입력 검증 실패와 도메인 실패를 구분해 처리해야 한다.

## 4. Why Now / Why Chain

- 구현부터 시작하면 테스트 기준이 사후 정의되어 회귀 안정성이 낮아진다.
- 입력/출력 계약이 불명확하면 기능별 책임 분리가 무너진다.
- Boundary와 Domain이 섞이면 실패 원인 분리가 불가능해진다.
- 리팩토링 이후 계약 검증 기준이 없으면 동작 보장이 어렵다.

따라서 지금 PRD로 기준을 고정해 개발 중 의사결정 비용과 품질 리스크를 선제적으로 줄인다.

## 5. Target Users

| 사용자 | 목표 |
|---|---|
| TDD 학습자 | RED-GREEN-REFACTOR를 계약 중심으로 학습 |
| 코드 리뷰어 | 규칙/계약/검증 누락 여부를 객관적으로 점검 |
| ECB/Clean Architecture 학습 개발자 | Boundary/Control/Domain 분리 원칙 적용 |

사용 환경은 콘솔/테스트 실행 중심이며 UI, DB, Web은 본 범위 밖이다.

## 6. Vision & Epic Goal

- Epic Goal: **불변식 기반 사고 훈련 시스템 구축**
- Vision:
  - 입력/출력 계약 우선
  - 검증 가능한 도메인 규칙 우선
  - Dual-Track TDD 병행 진행
  - 요구사항-검증-컴포넌트 간 추적성 보장

## 7. Persona

- TDD를 학습 중이며 테스트 실패를 통해 요구사항을 구체화하려는 개발자
- 계층 분리와 의존 방향을 실무 수준으로 연습하려는 개발자
- 정답 코드보다 설계·계약·검증 흐름을 우선시하는 사용자

## 8. User Journey Summary

| 단계 | Pain Point | Learning Outcome |
|---|---|---|
| 문제 인식 | 목표가 "완성"인지 "검증"인지 혼동 | 문제를 계약/불변식으로 재정의 |
| 계약 정의 | 입력/출력 형식 불명확 | 고정 계약으로 경계 명확화 |
| 도메인 분리 | 검증/포맷/오류 처리가 섞임 | Boundary/Domain 책임 분리 |
| Dual-Track TDD | 한 트랙 선행으로 병목 발생 | Track A/B 병행 RED-GREEN 운영 |
| 회귀 보호 | 리팩토링 후 동작 불확실 | 추적성 기반 회귀 안전망 확보 |

## 9. Scope

### 9.1 In-Scope

- 빈칸 좌표 탐색
- 누락 숫자 탐색
- 마방진 판정
- 두 조합 시도 및 결과 반환
- Boundary 입력 검증
- 출력 계약 검증
- Dual-Track TDD를 위한 검증 가능 요구사항 정의

### 9.2 Out-of-Scope

- UI 화면 개발
- DB 저장/검색
- Web/API 서버 개발
- N×N 일반화
- 완전한 마방진 생성 알고리즘 확장
- 사용자 인증/권한
- 네트워크 오류 처리
- QR 스캔
- 외부 서비스 연동

## 10. Functional Requirements

### FR-01 Input Verification
- Description: 입력 보드 계약을 검증한다.
- Layer: Boundary
- Input: `int[][]`
- Processing Rules: 4x4 크기, 빈칸 2개, 값 범위, 0 제외 중복 금지 검증
- Output: 유효 시 Domain 호출 허용, 무효 시 오류 응답
- Acceptance Criteria: 위 규칙 위반 시 즉시 실패 처리
- Error / Exception Policy: 오류 코드 기반 실패 반환
- Related Business Rules: BR-01, BR-02, BR-03, BR-04
- Related Test Direction: 형식/범위/중복/빈칸 개수 경계 테스트
- Component Candidate: BoundaryValidator

### FR-02 Blank Coordinate Discovery
- Description: row-major 기준 첫/둘째 빈칸 좌표를 식별한다.
- Layer: Domain
- Input: 유효성 검증 통과 보드
- Processing Rules: 행 우선 순서로 `0` 좌표 탐색
- Output: 빈칸 좌표 2개
- Acceptance Criteria: 첫 번째 빈칸 정의가 row-major와 일치
- Error / Exception Policy: 빈칸 규칙 위반은 FR-01에서 선처리
- Related Business Rules: BR-05
- Related Test Direction: 좌표 순서 일관성 테스트
- Component Candidate: BlankFinder

### FR-03 Missing Number Discovery
- Description: 1..16 기준 누락 숫자 2개를 찾는다.
- Layer: Domain
- Input: 유효성 검증 통과 보드
- Processing Rules: `0` 제외 값 집합 대비 차집합 계산, 오름차순 정렬
- Output: 누락 숫자 `[small, large]`
- Acceptance Criteria: 누락 숫자 2개 정확 반환 및 오름차순 유지
- Error / Exception Policy: 입력 계약 위반은 FR-01에서 처리
- Related Business Rules: BR-06, BR-07
- Related Test Direction: 정상/경계 누락 숫자 계산 테스트
- Component Candidate: MissingNumberFinder

### FR-04 Magic Square Validation
- Description: 완성 보드가 마방진 불변식을 만족하는지 검증한다.
- Layer: Domain
- Input: 완성된 4x4 보드
- Processing Rules: 행/열/대각선 합을 마방진 상수 34와 비교
- Output: valid/invalid 판정
- Acceptance Criteria: 모든 관련 선 합이 34일 때만 valid
- Error / Exception Policy: invalid 반환
- Related Business Rules: BR-08, BR-09
- Related Test Direction: 행/열/대각선 실패 및 전체 성공 케이스
- Component Candidate: MagicSquareValidator

### FR-05 Two-Combination Solver and Result Formatting
- Description: small-first 우선 규칙으로 두 조합을 시도하고 결과를 포맷한다.
- Layer: Domain + Boundary Output Contract
- Input: 빈칸 좌표 2개, 누락 숫자 2개
- Processing Rules:
  - Attempt 1: small→first blank, large→second blank
  - Attempt 2: 반대 조합
- Output: 성공 시 `[r1,c1,n1,r2,c2,n2]` (1-index)
- Acceptance Criteria: Attempt 1 성공 시 해당 순서, 실패 후 Attempt 2 성공 시 반대 순서 반환
- Error / Exception Policy: 두 조합 모두 실패 시 정의된 실패 응답 반환
- Related Business Rules: BR-10, BR-11
- Related Test Direction: small-first 성공/실패 후 reverse 성공/양쪽 실패 테스트
- Component Candidate: Solver, ResultFormatter

## 11. Business Rules / Domain Rules

| ID | 규칙 |
|---|---|
| BR-01 | 입력은 항상 4x4 정수 행렬이어야 한다. |
| BR-02 | 빈칸 `0`은 항상 정확히 2개여야 한다. |
| BR-03 | 입력 값은 항상 `0` 또는 `1..16` 범위여야 한다. |
| BR-04 | `0`을 제외한 숫자는 항상 중복되지 않아야 한다. |
| BR-05 | 첫 번째 빈칸은 항상 row-major 스캔 기준으로 결정한다. |
| BR-06 | 누락 숫자는 항상 정확히 2개여야 한다. |
| BR-07 | 누락 숫자 쌍은 항상 오름차순 `[small, large]`로 정의한다. |
| BR-08 | 마방진 상수는 항상 34다. |
| BR-09 | 유효한 마방진은 항상 모든 행/열/대각선 합이 34여야 한다. |
| BR-10 | 출력 좌표는 항상 1-index여야 한다. |
| BR-11 | 성공 출력 형식은 항상 `int[6] = [r1,c1,n1,r2,c2,n2]`여야 한다. |

## 12. Input / Output Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code |
|---|---|---|---|---|---|
| board | `int[4][4]` | 4x4 고정 | 4행 4열 정수 행렬 | 3x4, 4x3 | E_INVALID_SHAPE |
| blank count | integer | `0` 개수 = 2 | 두 칸만 0 | 0이 1개 또는 3개 | E_INVALID_BLANK_COUNT |
| value range | integer cell | 값은 0 또는 1..16 | 0, 1, 16 | -1, 17 | E_INVALID_VALUE_RANGE |
| non-zero uniqueness | set rule | 0 제외 중복 금지 | 1..16 중 일부 결손, 중복 없음 | 동일 숫자 2회 | E_DUPLICATE_NON_ZERO |
| result | `int[6]` | `[r1,c1,n1,r2,c2,n2]` | `[1,2,5,3,4,12]` | 길이 5/7 배열 | E_INVALID_RESULT_FORMAT |
| coordinates | integer pair | 1-index (1..4) | r=1,c=4 | r=0,c=3 | E_INVALID_RESULT_COORDINATE |

## 13. Error / Failure Policy

| Error Code | Message | Layer | Domain resolver 호출 여부 | Related Acceptance Criteria |
|---|---|---|---|---|
| E_INVALID_SHAPE | 입력은 4x4 행렬이어야 합니다. | Boundary | No | FR-01 |
| E_INVALID_BLANK_COUNT | 빈칸(0)은 정확히 2개여야 합니다. | Boundary | No | FR-01 |
| E_INVALID_VALUE_RANGE | 값은 0 또는 1~16 범위여야 합니다. | Boundary | No | FR-01 |
| E_DUPLICATE_NON_ZERO | 0을 제외한 값은 중복될 수 없습니다. | Boundary | No | FR-01 |
| E_UNSOLVABLE_COMBINATION | 두 조합 모두 마방진을 만족하지 않습니다. | Domain/Boundary response mapping | Yes (검증 수행 후) | FR-05 |

정책:
- 입력 검증 실패 시 Domain resolver는 호출하지 않는다.
- 두 조합 실패는 입력 오류가 아니며 도메인 실패로 분류한다.

## 14. Non-Functional Requirements

| ID | 요구사항 |
|---|---|
| NFR-01 | Domain Logic 테스트 커버리지는 95% 이상이어야 한다. |
| NFR-02 | Boundary Validation 테스트 커버리지는 85% 이상이어야 한다. |
| NFR-03 | 동일 입력은 항상 동일 출력을 반환해야 한다(결정성). |
| NFR-04 | 입력 행렬 변경 정책을 명시해야 하며, 기본 정책은 입력 불변(원본 변경 금지)으로 정의한다. |
| NFR-05 | 4x4 기준 단일 실행은 목표 50ms 이내여야 한다. |
| NFR-06 | Boundary/Domain 책임 분리를 유지해야 한다. |
| NFR-07 | 하드코딩 상수와 설명 없는 매직 넘버 사용을 금지한다. |

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD
- 입력 검증 규칙 검증
- 출력 형식/좌표 계약 검증
- 실패 응답 코드 검증
- 입력 오류 시 Domain 미호출 검증

### 15.2 Track B — Domain / Logic TDD
- 빈칸 탐색 검증
- 누락 숫자 탐색 검증
- 마방진 판정 검증
- small-first 성공 검증
- small-first 실패 후 reverse 성공 검증
- 두 조합 모두 실패 검증

### 15.3 Parallel Progression Rules
- UI RED와 Logic RED를 분리한다.
- UI GREEN과 Logic GREEN을 각각 최소 구현 원칙으로 진행한다.
- 구조 개선은 REFACTOR 단계에서만 수행한다.
- Domain 전부 선구현 후 Boundary 연결 방식은 금지한다.
- 테스트 약화/삭제로 통과시키는 방식은 금지한다.

## 16. Test Plan / QA

### 16.1 Normal Scenarios
- small-first 성공
- small-first 실패 후 reverse 성공

### 16.2 Exception Scenarios
- 4x4가 아닌 입력
- 빈칸 개수 오류
- 값 범위 오류
- 중복 숫자 오류
- 두 조합 모두 실패

### 16.3 Boundary Scenarios
- 최소값 1, 최대값 16 처리
- 0은 빈칸 의미로만 처리
- 출력 좌표 1-index 유지
- 반환 배열 길이 6 유지

### 16.4 Representative Test Data
- small-first 성공 행렬
- reverse 성공 행렬
- invalid size 행렬
- invalid blank count 행렬
- duplicate value 행렬
- invalid range 행렬

## 17. Architecture Overview, High-Level

- Boundary Layer:
  - 입력 검증
  - 오류 응답 매핑
  - 출력 계약 포맷 보장
- Domain Layer:
  - 빈칸 탐색, 누락 숫자 탐색, 마방진 판정, 조합 시도
  - 불변식 검증
- Control / Application Layer:
  - Boundary와 Domain 흐름 조정

의존 방향:
- Boundary → Control → Domain
- Domain은 Boundary를 몰라야 한다.
- Domain은 UI/DB/Web/FileSystem에 의존하지 않아야 한다.

## 18. Component Candidates

| Component | Responsibility | Layer | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| BoundaryValidator | 입력 계약 검증 | Boundary | `int[][]` | valid/에러 | FR-01 | 입력 오류 케이스 |
| BlankFinder | row-major 빈칸 좌표 탐색 | Domain | validated board | blank coords | FR-02 | 좌표 순서 검증 |
| MissingNumberFinder | 누락 숫자 계산(오름차순) | Domain | validated board | missing pair | FR-03 | 누락 숫자 검증 |
| MagicSquareValidator | 행/열/대각선 합 검증 | Domain | completed board | valid/invalid | FR-04 | 합 규칙 검증 |
| Solver | 두 조합 시도 및 선택 | Domain | blanks + missing pair | solved assignment/unsolved | FR-05 | A/B/실패 시나리오 |
| ResultFormatter | `int[6]` 계약 포맷 생성 | Boundary/Control | solved assignment | `int[6]` | FR-05 | 출력 계약 검증 |

## 19. Risks & Ambiguities

| Risk | Impact | Decision / Mitigation |
|---|---|---|
| 1-index vs 0-index 혼동 | 출력 계약 불일치 | 출력 계약에 1-index 고정, 검증 항목 분리 |
| row-major 첫 빈칸 정의 누락 | 결과 비결정성 | BR-05로 명시 및 테스트 방향 고정 |
| small-first/reverse 데이터 혼동 | 오탐/누락 검증 발생 | 대표 데이터셋을 시나리오별 분리 |
| 입력 행렬 변경 여부 불명확 | 부작용/회귀 리스크 | 입력 불변 정책(NFR-04) 명시 |
| 두 조합 실패 정책 누락 | 런타임 처리 불일치 | E_UNSOLVABLE_COMBINATION 고정 |
| 34 상수 하드코딩 남용 | 변경 취약성/가독성 저하 | 명명 상수 정책 및 금지 규칙 적용 |
| Boundary/Domain 책임 혼합 | 테스트 난이도 상승 | 계층 책임 체크리스트 운영 |

## 20. Engineering Principles

- PEP8 준수
- 함수 파라미터/반환 타입 힌트 필수
- pytest 기반 테스트 설계
- AAA 패턴 준수
- 커버리지 목표: Domain 95%+, Boundary 85%+
- ECB 계층 분리 준수
- RED-GREEN-REFACTOR 엄격 준수
- production 코드에서 `print()` 금지
- bare `except` 금지
- 테스트 약화/삭제 금지
- 설명 없는 magic number 금지

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4x4 입력 | BR-01 | FR-01 | 4x4 외 입력 즉시 실패 | invalid shape | BoundaryValidator |
| 빈칸 2개 | BR-02 | FR-01 | 0 개수 2개만 허용 | invalid blank count | BoundaryValidator |
| 값 범위 0/1..16 | BR-03 | FR-01 | 범위 위반 입력 실패 | invalid range | BoundaryValidator |
| 중복 금지 | BR-04 | FR-01 | 0 제외 중복 입력 실패 | duplicate value | BoundaryValidator |
| row-major 첫 빈칸 | BR-05 | FR-02 | 첫 좌표 결정 규칙 일치 | first blank order | BlankFinder |
| 누락 숫자 2개 | BR-06 | FR-03 | 누락 수 2개 계산 정확 | missing count | MissingNumberFinder |
| 누락 숫자 오름차순 | BR-07 | FR-03 | `[small, large]` 유지 | ordering check | MissingNumberFinder |
| 마방진 상수 34 | BR-08 | FR-04 | 상수 기준 판정 | constant validation | MagicSquareValidator |
| 행/열/대각선 합 | BR-09 | FR-04 | 모두 34일 때만 valid | line-sum checks | MagicSquareValidator |
| small-first 시도 | BR-09/BR-11 | FR-05 | Attempt 1 성공 시 즉시 반환 | small-first success | Solver |
| reverse 시도 | BR-09/BR-11 | FR-05 | Attempt 1 실패 후 Attempt 2 수행 | reverse success | Solver |
| int[6] 반환 | BR-11 | FR-05 | 길이/순서 계약 유지 | output format | ResultFormatter |
| 1-index 좌표 | BR-10 | FR-05 | 좌표 1..4 유지 | coordinate index check | ResultFormatter |

## 22. Open Questions / Decision Needed

- Decision Needed: 두 조합 실패 시 처리 방식(실패 응답 객체 vs 예외)을 현재 PRD에서는 오류 코드 기반 실패 응답으로 고정했으나, 팀 런타임 정책과 완전 일치 여부 최종 확인 필요.
- Decision Needed: 성능 목표(50ms)는 4x4 단일 실행 기준 제안값이며, 실행 환경(로컬/CI)별 공통 측정 프로토콜 확정 필요.

## 23. Appendix

### 참고 문서
- `Report/01.MagicSqure_Problem-Definition-Report.md`
- `Report/02.MagicSquare_4x4_Dual-Track-TDD-CleanArchitecture-Report.md`
- `Report/03.MagicSquare_CursorRules-Entity-Implementation-Report.md`
- `Report/06.MagicSquare_Level1-5-Scenario-Verification-Report.md`
- `.cursorrules`
- `.cursor/rules/magicsquare-project.mdc`
- `.cursor/rules/magicsquare-ecb-architecture.mdc`
- `.cursor/rules/magicsquare-tdd-testing.mdc`
- `.cursor/rules/magicsquare-python-code-style.mdc`
- `.cursor/rules/magicsquare-forbidden.mdc`

### Cursor Rules 요약
- 프로젝트/아키텍처/테스트/코드스타일/금지패턴 규칙 분리 적용
- TDD 흐름 및 커버리지 기준 명시
- 금지 패턴(`print`, bare except, 하드코딩 상수) 명확화

### 대표 Gherkin Scenario 요약
- 정상: small-first 성공, reverse 성공
- 예외: 입력 형상 오류, 빈칸 개수 오류, 값 범위 오류, 중복 오류, unsolvable

### 향후 RED Test ID 후보
- TRED-BND-001~004 (입력 계약 검증)
- TRED-DOM-001~006 (도메인 핵심 규칙 검증)
- TRED-SLV-001~003 (조합 시도/실패 정책 검증)
