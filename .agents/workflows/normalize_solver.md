---
description: V2 MAS 파이프라인 기반의 신규 AtomicModule 또는 V1 Solver를 표준화하는 절차
---

# AIME 문항 모듈 표준화 워크플로우 (V2 기준)

이 워크플로우는 기출 문항 분석부터 MAS 파이프라인 배포까지의 전체 표준 절차입니다.
V1 Solver `normalize_solver` 작업과 V2 `AtomicModule` 신규 작성 모두에 적용됩니다.

---

## Phase 1: 수학적 감사 (Mathematical Audit)

### 1단계: 원형 문항 해부 (Deconstruction)
- 원형 AIME 문항의 공식 해설을 분석하여 핵심 정리(Lemma)와 계산 과정을 분해합니다.
- **고정 요소(Constants)** vs **가변 요소(Seeds)**를 구분합니다.
- `δ(Heuristic/Trap)` 값을 사전 추정합니다:
  - `δ=0`: 표준 절차로 풀림
  - `δ=1`: 하나의 비자명한 치환 필요
  - `δ=2`: 함정이 설계에 포함됨
  - `δ=3`: 역발상이 핵심 메커니즘

### 2단계: DAPS 목표 설정
원형 문항의 전체 DAPS를 추정하고 분해합니다:
```
예시) AIME 2025 P12: DAPS ≈ 13.5
  α(Computational) = 3.5
  β(LogicalDepth)  = 4.0
  γ(Category)      = 2.0  (Algebra × NT)
  δ(Heuristic)     = 4.0  → Master 등급 확정
```

---

## Phase 2: 시각적 감사 (Visual Audit)

### 3단계: 이미지 필요성 판별
다음 기준으로 `has_image` 값을 결정합니다:
1. GEOMETRY 도메인이거나 삼각형/원 등 공간 대상인가? → True
2. 지문에 좌표, 길이, 각도 등 공간적 배치가 포함되는가? → True
3. 원형 AIME 문제에 다이어그램이 포함되었는가? → True
4. 드릴(L1/L2)에서 시각화가 학습에 필수적인가? → True

**렌더러 선택:**
- 일반/기초: `matplotlib`
- AIME 수준 기하: `TikZ / Asymptote` → SVG

---

## Phase 3: DNA 모델링 (DNA Modeling)

### 4단계: AtomicModule META 정의
```python
class META:
    module_id = "algebra.polynomials.vieta"          # 도메인.주제.세부주제
    name = "Vieta's Formulas — Polynomial Roots"
    category = "ALGEBRA"
    domain = "integer"                               # "integer" | "real"
    namespace = "algebra_vieta"                      # 전역 고유 (충돌 방지)
    logic_depth = 3                                  # β 계산 기준
    daps_contribution = 4.5                          # 단독 기여 DAPS
    min_difficulty = 10                              # 최소 AIME 번호
    exam_types = ["AIME", "AMC12"]
```

**context_type 결정 기준:**
- `abstract`: 원형이 순수 수학 언어 (수식, 정수, 집합) → 테마 주입 절대 금지
- `narrative`: 원형이 상황 중심 (동전, 상자, 사람 이름)

---

## Phase 4: 수학적 안전 범위 설정 (Safety Bounds)

### 5단계: SEED_CONSTRAINTS 정의
```python
SEED_CONSTRAINTS = {
    "n": {"min": 3, "max": 12},
    "k": {"min": 2, "max": 8},
}
```

**필수 패턴 — 100회 Fallback 보장:**
```python
def generate_seed(self, difficulty_hint: float = 13.0) -> dict:
    for _ in range(100):
        # constraint 내에서 랜덤 샘플링
        n = random.randint(self.SEED_CONSTRAINTS["n"]["min"], ...)
        answer = self._compute(n)
        if 0 <= answer <= 999:                       # AIME 정답 범위
            return {"n": n, "answer": answer}
    return {"n": 5, "answer": self._compute(5)}      # FALLBACK_SEED
```

### 6단계: BEq 사전 검증 (로컬 테스트)
```python
# 배포 전 필수 검증
module = MyModule()
seed = module.generate_seed(difficulty_hint=13.0)
answer = module.execute(seed)
valid, reason = module.validate_answer(answer)
assert valid, f"안전 범위 위반: {reason}"
print(f"정답: {answer}, 유효성: {valid}")
```

---

## Phase 5: 교육적 로직 설계 (Pedagogy)

### 7단계: Logic Steps 작성
`get_logic_steps(seed)`는 Writer 에이전트의 서술 로드맵이자
학습자의 해설 이정표입니다. **킬러 로직은 반드시 독립된 단계**로 설계합니다:

```python
def get_logic_steps(self, seed: dict) -> list[str]:
    return [
        f"[관찰] n={seed['n']}인 다항식의 비에타 공식 적용 → 근의 합 확인",
        f"[핵심 치환] 대칭 함수 변환으로 e₂를 제거 (이 문제의 핵심 트릭)",
        f"[계산] 최종 값 = {seed['answer']} 도출 후 0-999 범위 확인",
    ]
```

### 8단계: 드릴 계층화 설계 (Drill Scaffolding)
- **Drill L1 (Atomic)**: 해당 문항의 '핵심 개념 하나'만 단독 문제화
  - 예: "비에타 공식으로 두 근의 곱 계산하기 ($n ≤ 5$)"
- **Drill L2 (Intermediate)**: 원형 논리 유지하되 수치를 단순화 (DAPS ≈ 6–9)
- **Drill L3 / Mock**: 원형과 동일한 난이도 (DAPS 12+), `δ` 완전 재현

---

## Phase 6: 최종 검증 Checklist ✅

배포 전 다음 7항목을 모두 통과해야 합니다:

- [ ] **L1 Concept Test**: `generate_drill_seed(1)`이 의도한 기초 수치를 반환하는가?
- [ ] **L2 Scaling Test**: 파라미터가 작아졌음에도 수학적 원리가 깨지지 않는가?
- [ ] **L3 Distribution Test**: 10회 생성 시 정답이 편향 없이 분포하는가?
- [ ] **Safety Bounds**: 모든 시드에서 정답이 0–999 범위 내에 있는가?
- [ ] **Narrative Integrity**: `context_type=abstract`일 때 테마 누출이 없는가?
- [ ] **Module Registry**: `ModuleRegistry.register(module)` 성공 + 기존 모듈과 호환성 테스트 통과
- [ ] **BEq 파이프라인 테스트**: `pipeline_v2.generate_problem()` 실행 후 `verdict=PASS` 확인
