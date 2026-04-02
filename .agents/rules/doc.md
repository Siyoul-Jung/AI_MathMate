# doc: AI MathMate V2 문서화 표준

이 문서는 AI MathMate V2 프로젝트의 모든 코드, 모듈, 데이터 모델에 적용되는
**문서화 규칙과 주석 표준**을 정의합니다.

---

## 1. 원자 모듈 (Atomic Module) 문서화

모든 `AtomicModule`은 다음 형식의 클래스 Docstring을 포함해야 합니다:

```python
class AlgebraPolynomialsVietaModule(AtomicModule):
    """
    [모듈명] Algebra — 다항식 비에타 공식 (Vieta's Formulas)
    
    [핵심 개념]
    고차 다항식의 근의 합과 곱을 계수 관계로 표현합니다.
    
    [DAPS 기여]
    - daps_contribution: 4.5
    - logic_depth: 3 (비에타 적용 → 대칭 함수 변환 → 값 계산)
    - δ(Heuristic): 0.5 (표준 치환, 비직관적 요소 없음)
    
    [관련 AIME 기출]
    - AIME 2025 I, Problem 4
    
    [Namespace]
    algebra_vieta (충돌 방지: 'vieta_n', 'vieta_sum', 'vieta_product')
    """
```

---

## 2. 프로젝트 문서 관리

### README.md
- **기술 스택**: 현재 사용 중인 LLM 모델명과 버전을 항상 최신 상태로 유지
- **Quick Start**: `pipeline_v2.py` 기준의 로컬 실행 방법 포함
- **DAPS 공식**: 현재 적용 중인 α, β, γ, δ 가중치 값 명시

### 변경 로그 (Change Log)
다음 사항이 변경될 때마다 관련 모듈의 Docstring 또는 `CHANGELOG.md`에 기록합니다:
- DB 스키마 변경 (테이블 추가/컬럼 변경)
- LLM 프롬프트의 구조적 변경
- DAPS 공식의 가중치 조정
- AtomicModule의 SEED_CONSTRAINTS 범위 변경

---

## 3. MAS 로그 (mas_logs) 데이터 규약

BEq 루프의 모든 이력은 `mas_logs` 테이블에 저장됩니다.
각 레코드는 다음을 포함해야 합니다:

| 필드 | 설명 |
|---|---|
| `agent_role` | ARCHITECT / WRITER / EVALUATOR / JUDGE |
| `agent_model` | 호출된 LLM 모델명 또는 "python-logic" |
| `input_sent` | 에이전트에게 전달한 입력 (JSON 직렬화) |
| `output_received` | 에이전트의 출력 (JSON 직렬화) |
| `verdict` | PASS / FAIL / FIX_REQUIRED / null |
| `fix_instruction` | Judge의 수정 지시 (FIX_REQUIRED시) |
| `attempt_number` | BEq 루프 시도 횟수 (1~max_loop) |
| `duration_ms` | LLM 응답 소요 시간 |

**Circuit Breaker 발동 시** `verdict`를 `"CIRCUIT_BREAKER"`로 기록합니다.

---

## 4. 수학 콘텐츠 문서화

### Logic Steps 작성 규칙
`get_logic_steps(seed)`의 출력은 LLM Writer와 사용자 모두가 이해할 수 있어야 합니다:

```python
def get_logic_steps(self, seed: dict) -> list[str]:
    n = seed["n"]
    return [
        f"1단계 [핵심 관찰]: n={n}일 때 비에타 공식으로 근의 합 = {seed['s1']} 확인",
        f"2단계 [변환]: 대칭 함수 e2를 s1²-2s2로 변환",
        f"3단계 [계산]: 최종값 = {seed['answer']} (0~999 범위 확인)",
    ]
```

### 비교 보고서 형식
AIME 기출 vs 생성 문항 비교 시 테이블 형식 사용:

| 항목 | 원형 (AIME 2025) | 생성 변체 |
|---|---|---|
| 핵심 개념 | 비에타 공식 | 비에타 공식 |
| DAPS | 13.5 | 13.2 |
| δ(Heuristic) | 2.0 | 1.5 |
| 정답 범위 | 0–999 | 0–999 ✅ |

---

## 5. 인라인 주석 표준

```python
# ── 섹션 구분 (긴 파일에서 구조 명시) ──────────────────────────
def generate_seed(self, difficulty_hint: float) -> dict:
    """
    DAPS hint를 참고하여 안전한 시드를 생성합니다.
    
    Args:
        difficulty_hint: 목표 DAPS 점수 (Architect 에이전트 제공)
    Returns:
        seed dict — AtomicModule의 namespace 내 변수들
    Raises:
        ValueError: 100회 시도 후 유효한 시드를 찾지 못한 경우
    """
    # SEED_CONSTRAINTS 준수: 100회 Fallback 보장
    for _ in range(100):
        ...
```
