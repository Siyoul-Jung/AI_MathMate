# math_engine_standard: AI MathMate 엔지니어링 표준 (V2)

이 문서는 AI MathMate V2 문항 생성 엔진의 설계 및 유지보수에 관한 핵심 규칙을 정의합니다.
모든 AI 모델과 개발자는 이 규칙을 준수해야 합니다.

---

## 1. 핵심 철학: 두 가지 역할의 엄격한 분리

```
[수학적 진실]  Python AtomicModule.execute(seed) → correct_answer (결정론적, 100% 신뢰)
      ↓
[서사적 표현]  LLM Writer → narrative (LaTeX 지문, BEq로 반드시 검증)
```

**혁신의 저주(Innovation Curse) 방지 원칙:**
LLM은 수학 계산의 주체가 될 수 없습니다. Writer는 `seed`와 `logic_steps`를 받아 **서술만** 합니다.
창의적 표현을 위해 수학적 조건을 임의로 추가하거나 변형하는 행위는 **즉각 BEq 실패**로 처리합니다.

---

## 2. 난이도 체계: DAPS (Dynamic Difficulty Assessment & Prediction Score)

### 2.1 DAPS 공식 (V2 확장판)

$$DAPS = \alpha(Computational) + \beta(LogicalDepth) + \gamma(CategoryCombination) + \delta(Heuristic/Trap)$$

| 변수 | 의미 | 범위(점) |
|:---:|---|:---:|
| α | 계산 복잡도 (브루트 포스 불가 수준) | 0–5 |
| β | 논리적 깊이 (보조 정리 연쇄 수) | 0–5 |
| γ | 카테고리 결합 (2개 이상 도메인 혼합) | 0–3 |
| **δ** | **인지적 함정/발상의 전환 (Heuristic/Trap)** | **0–3** |

**δ 정량화 기준:**
- `δ=0`: 풀이 경로가 선형적이고 예측 가능함
- `δ=1.0`: 하나의 비자명한(non-trivial) 치환 또는 관찰이 필요함
- `δ=2.0`: 일반적 접근 전략이 실패하도록 설계된 함정 존재
- `δ=3.0`: 역발상이 핵심 메커니즘 (예: "구하는 값을 직접 구하지 않음")

**δ 값이 높은 문제는 계산량이 적어도 MASTER 등급으로 분류될 수 있습니다.**

### 2.2 난이도 밴드 기준

| 밴드 | DAPS 범위 | 특성 |
|---|---|---|
| Challenger | 6.0–9.0 | 단일 도메인, α+β 중심 |
| Expert | 9.0–12.0 | 복합 도메인, γ 존재 |
| Master | 12.0–16.0 | 높은 δ(함정), 모든 변수 활성 |

### 2.3 레거시 호환 (Level 1/2/3)
V1 DB와의 호환성을 위해 다음 매핑을 유지합니다:
- Level 1 (Concept) ≈ DAPS 3.0 이하 단일 Atomic Module
- Level 2 (Intermediate) ≈ DAPS 6.0–9.0 수동 계산 가능
- Level 3 (Master/Mock) ≈ DAPS 12.0+ 원형 재현

---

## 3. MAS 파이프라인 표준 (Multi-Agent System)

### 3.1 에이전트 역할 정의

| 에이전트 | 역할 | LLM 사용 |
|---|---|:---:|
| **Architect** | 목표 DAPS에 맞는 호환 모듈 조합 선택 | ✅ |
| **Writer** | seed + logic_steps → LaTeX 지문 서술 | ✅ |
| **Evaluator** | 지문만 보고 역추론으로 정답 도출 | ✅ |
| **Judge** | Evaluator 정답 vs 원본 정답 BEq 판정 | ❌ (Pure Python) |

### 3.2 BEq (Bidirectional Equivalence) 검증 프로토콜

BEq는 이 시스템의 **수학적 진실의 유일한 기준**입니다.

```
Python Solver.execute(seed) → answer_A (Ground Truth)
          ↓
LLM Writer.run(seed) → narrative
          ↓
LLM Evaluator.run(narrative) → answer_B (역추론)
          ↓
Judge: answer_A == answer_B ? → PASS : FIX_REQUIRED / FAIL
```

**BEq 판정 기준:**
1. 수학적 정확성: `answer_A == answer_B` (필수)
2. Evaluator 신뢰도: `confidence != "LOW"` (필수)
3. 지문 모호성: `ambiguity == ""` (권장)
4. 조건 추출 최소 기준: `len(conditions) >= 2` (필수)

### 3.3 Circuit Breaker & Fallback 로직 ⚡

**무한 루프(Deadlock) 방지는 파이프라인의 안정성을 보장하는 핵심입니다.**

```python
# 표준 패턴: Fix History 누적으로 국소 수렴(Local Convergence) 방지
fix_history = []
for attempt in range(1, max_loop + 1):     # max_loop = 3 (기본값)
    writer_res = writer.run(..., fix_history=fix_history)
    judge_res = judge.run(...)

    if judge_res.verdict == "PASS":
        break
    elif judge_res.verdict == "FAIL":       # 수학 오류: 즉시 종료
        break
    else:                                   # FIX_REQUIRED
        fix_history.append(judge_res.fix_instruction)  # 이전 실패 이력 누적

# Circuit Breaker: 3회 초과 시 Fallback
if not success:
    # 옵션 1: 현재 Seed 폐기 후 새 Seed 재생성
    # 옵션 2: Architect에게 반환 → DAPS를 -1.5 하향 재설계
```

---

## 4. 원자 모듈 표준 (Atomic Module Standard)

### 4.1 필수 구현 인터페이스

```python
class MyModule(AtomicModule):
    class META:
        module_id: str          # 예: "algebra.polynomials.vieta"
        namespace: str          # 고유 변수 네임스페이스 (충돌 방지)
        daps_contribution: float # 이 모듈의 기본 DAPS 기여도
        logic_depth: int        # 논리 단계 수 (β 계산 기준)
        exam_types: list[str]   # ["AIME", "AMC12"] 등

    def generate_seed(self, difficulty_hint: float) -> dict: ...
    def execute(self, seed: dict) -> int: ...              # 0–999 보장
    def validate_answer(self, answer: int) -> tuple: ...
    def get_logic_steps(self, seed: dict) -> list[str]: ...
    def get_daps_contribution(self, seed: dict) -> float: ...
```

### 4.2 시드 안전 범위 (Safety Bounds)

```python
SEED_CONSTRAINTS = {
    "param_n": {"min": 2, "max": 20},   # 예시
}
# 필수: while 루프 + 100회 Fallback
for _ in range(100):
    seed = _sample_seed()
    if 0 <= execute(seed) <= 999:
        return seed
return FALLBACK_SEED  # 안전 시드로 반환
```

---

## 5. 픽스 데이터 표준 (Visuals)

### 5.1 시각화 필요성 판별
다음 중 하나 이상 해당 시 `has_image: True` 설정 필수:
1. **Domain**: GEOMETRY 도메인 또는 삼각형/원 등 공간 대상
2. **Spatial**: 좌표, 길이, 각도 등 공간적 배치 포함
3. **History**: 원형 AIME 문제에 다이어그램 포함
4. **Pedagogy**: Logic Step 설명에 시각화가 절실한 경우

### 5.2 렌더러 선택 기준

| 상황 | 권장 렌더러 |
|---|---|
| 데이터 플롯, 수열 그래프 | `matplotlib` (현재 표준) |
| AIME 수준 기하 작도 | **TikZ / Asymptote** → SVG (권장) |
| 동적 수학 시각화 | `Manim` (Docker 친화적 대안) |

**Drill 정책:**
- **Mock / Level 3**: 원형 전통 100% 준수 (그림 없으면 제공 안 함)
- **Drill L1 / L2**: 학습 효과를 위해 보조 이미지 적극 생성
- **Solution Phase**: 모든 레벨에서 Logic Step별 이미지 열람 지원

---

## 6. 코드 품질 기준

- **Base Inheritance**: 모든 Solver는 `BaseAIMESolver` 또는 `AtomicModule`을 상속
- **DNA 스키마**: 모든 메타데이터는 `DNAModel` Pydantic 클래스 기반
- **Zero Hallucination 원칙**: LaTeX 렌더링 및 수식 계산에서 LLM 단독 출력은 절대 신뢰하지 않음
- **Validation First**: 신규 모듈 배포 전 수치 스케일링 테스트 + BEq 검증 필수
