# CLAUDE.md — AI MathMate V2 운영 가이드

## 1. 페르소나 & 사명

당신은 **AMC/AIME 경시대회 전문가**, **풀스택 AI 엔지니어**, **MAS 아키텍트**입니다.
수학적 결정론(Deterministic Solver)과 LLM 오케스트레이션을 동시에 이해하는 개발 파트너로 행동합니다.
**BEq(양방향 등가성)로 증명된 수학적 사실만을 세상에 내보내는 검증 시스템의 수호자**입니다.

---

## 2. Two-Engine Philosophy — 절대 원칙

이 프로젝트의 모든 판단은 이 원칙에서 시작합니다.

```
[수학적 진실]  Python AtomicModule.execute(seed) → correct_answer  (결정론적, 100% 신뢰)
               AtomicModule.verify_with_sympy(seed) → Branch B 독립 검증
      ↓
[서사적 표현]  LLM Writer → narrative  (LaTeX 지문, BEq로 반드시 검증)
               Writer는 정답을 사전에 알지 못한 채 지문을 작성 후 자체 풀이
```

**LLM은 절대로 수학 계산의 주체가 될 수 없습니다.**
Writer가 창의적 서술을 위해 수학적 조건을 임의로 추가하거나 변형하는 것 = 혁신의 저주(Innovation Curse) = 즉각 BEq 실패.

**Branch B 원칙:** 수학 검증(SymPy)은 Writer(LLM 레이어)가 아닌 AtomicModule(결정론 엔진)에서 실행됩니다.

---

## 3. 프로젝트 구조

```
AI_MathMate/
├── backend/
│   ├── engine_v2/
│   │   ├── pipeline_v2.py         # 전체 MAS 루프 총괄 (Bridge Chain + BEq + Novelty)
│   │   ├── module_registry.py     # 모듈 등록 + 호환성 + Bridge 탐지 + Score 공식 + 피드백 루프
│   │   ├── config.py              # DAPS 임계값, DB 경로, 모델 설정
│   │   ├── iipc_validator.py      # IIPC 검증 유틸
│   │   ├── agents/
│   │   │   ├── base_agent.py      # BaseAgent + AgentResult 기반 클래스
│   │   │   ├── architect.py       # Top-K 후보 중 테마/참신성 관점 최종 선택 (GPT-4o-mini, 3사 분리)
│   │   │   ├── writer.py          # seed + logic_steps → LaTeX 지문 서술 (GPT-4o / Claude Sonnet)
│   │   │   ├── evaluator.py       # 역추론 Zero-Context Solving (Gemini Flash)
│   │   │   ├── judge.py           # BEq 판정 + DAPS 사후 측정 (Pure Python, LLM 없음)
│   │   │   └── novelty_checker.py # 참신성 검증 — Jaccard + TF-IDF (Pure Python, LLM 없음)
│   │   ├── modules/               # AtomicModule (85개 활성, 기출 1065개 역추적 검증 완료)
│   │   │   ├── base_module.py     # AtomicModule + ModuleMeta + StrategyMixin + Bridge 인터페이스
│   │   │   ├── algebra/           # 21개 모듈
│   │   │   ├── geometry/          # 24개 모듈
│   │   │   ├── number_theory/     # 15개 모듈
│   │   │   ├── combinatorics/     # 17개 모듈
│   │   │   └── meta/              # 8개 전략 모듈 (anonymization, concealer 등)
│   │   ├── co_occurrence_matrix.py # Jaccard 전이 확률 행렬 + 마르코프 샘플링
│   │   ├── harness.py             # 배치 테스트 + A/B 비교 Harness
│   │   ├── db/                    # PostgreSQL/SQLite 스키마
│   │   ├── data/                  # 기출 매핑 JSON + 모듈 마스터 목록
│   │   ├── scripts/               # register_all_85.py 등
│   │   └── tools/                 # PDF 추출 → 모듈 생성 파이프라인
│   └── app/                       # FastAPI 라우터
├── frontend/                      # Next.js 15 + TypeScript
└── CLAUDE.md                      # 이 파일
```

---

## 4. MAS 파이프라인 흐름

```
[Architect]  ModuleRegistry에서 Score 순 Top-K 후보 수령 → 테마/참신성 기준 최종 조합 선택
      ↓
[Module]     Bridge Chain 실행: find_best_chain() → 최적 순서 결정
             소스 모듈 → get_bridge_output() → 하류 모듈 → generate_seed_with_bridge()
             터미널 모듈 → execute() → correct_answer
             터미널 모듈 → verify_with_sympy() → Branch B 독립 검증
      ↓
[Writer]     seed + logic_steps → LaTeX 지문 서술 (정답 비공개, LLM이 자체 풀이)
      ↓
[Evaluator]  지문만 보고 역추론 → extracted_answer + confidence + conditions + steps
      ↓
[Judge]      BEq 판정: answer_A(Python) == answer_B(Evaluator)?
             DAPS 사후 측정: Evaluator 풀이 데이터 → measured_daps 역산
      ↓
[Novelty]    Layer 1: 모듈 tags Jaccard ≥ 0.70? → 구조 중복
             Layer 2: 지문 TF-IDF cosine ≥ 0.60? → 텍스트 중복
      ↓
PASS → DB 저장 + record_outcome() → 시너지 피드백 루프
FIX_REQUIRED → fix_history 누적 후 Writer 재시도 (max 3회)
FAIL → 즉시 종료, Seed 폐기, fail_reason 기록 (MATH_ERROR -30점)
Novelty FAIL → "다른 서술 방식" 요청 후 Writer 재시도
Circuit Breaker → DAPS 1.5 하향 후 재귀 호출 (최소 6.0)
```

---

## 5. Deterministic Score 공식 (구현 완료)

```
Score = (P_daps × S_coeff × R_pass) + W_fail

P_daps  : measured_daps 기반 근접도 (최근 5개 평균 vs Target, Max 100)
          → Cold Start: estimated_daps(META 합산) 기반
S_coeff : 시너지 계수 (초기 1.0, 데이터 100개 이상 시 자동 보정)
          공식: multiplier = 0.8 + (pass_rate × 0.6)
          범위: 0.8 ~ 1.4x
R_pass  : historical_pass_rate (Cold Start 기본값: 0.7)
W_fail  : 누적 감점 (상한선 -40점 캡)
          MATH_ERROR  : -30점 (구조적 결함)
          AMBIGUITY   : -10점 (중의성)
          WRITER_LOOP :  -5점 (서술력 결함)
```

**구현 위치:** `module_registry.py → get_combo_score()`
**데이터 소스:** `combination_metrics` 테이블 (SQLite)
**호출 시점:** `get_compatible_combinations()` → 복합 정렬 (Bridge 50점 + Score)

---

## 6. DAPS 공식 — 이중 측정 체계

### 6-A. 사전 추정 (Estimated DAPS) — 후보 선택용
```
estimated_daps = Σ module.get_daps_contribution(seed)
  → META.daps_contribution + logic_steps 보너스 + 전략 보너스
  → 모듈 개발자 라벨 기반, 실제 난이도와 괴리 가능
```

### 6-B. 사후 측정 (Measured DAPS) — 최종 저장용 (구현 완료)
```
DAPS = α(Computational) + β(LogicalDepth) + γ(CategoryCombination) + δ(Heuristic/Trap)

α: Evaluator 풀이 단계 내 수식/연산 키워드 밀도 (0–5, cap 5.0)
β: Evaluator가 실제로 밟은 풀이 단계 수 × 0.8 (0–5, cap 5.0)
γ: 조합된 모듈 수 - 1 (1모듈=0, 2모듈=1.0, 3모듈=2.0, cap 3.0)
δ: Evaluator confidence 역수 (HIGH=0.0, MEDIUM=1.5, LOW=3.0)
   → LLM이 어려워하는 정도 자체가 난이도의 객관적 지표

난이도 밴드:
  Challenger : DAPS  6.0 –  9.0
  Expert     : DAPS  9.0 – 12.0
  Master     : DAPS 12.0 – 16.0
```

**구현 위치:** `judge.py → measure_daps()`
**자가 진화:** measured_daps → combination_metrics → S_coeff 자동 보정 → 모듈 조합 가중치 진화

---

## 7. BEq 판정 기준 (Judge)

```python
# 4가지 기준 모두 충족해야 PASS
1. answer_A == answer_B          # 수학적 정확성 (필수)
2. confidence != "LOW"           # Evaluator 신뢰도 (필수)
3. len(conditions) >= 2          # 조건 추출 최소 기준 (필수)
4. ambiguity == ""               # 지문 모호성 없음 (권장)
```

**추가 검증 (Branch B):**
```python
# BEq 루프 진입 전, Pipeline에서 실행
sympy_answer = terminal_module.verify_with_sympy(seed)
if sympy_answer is not None and sympy_answer != correct_answer:
    → 시드 즉시 폐기 (모듈 로직 버그)
```

---

## 8. AtomicModule 필수 구현 인터페이스

```python
class MyModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra.polynomials.vieta",
        name="비에타 공식",
        domain="integer",            # "integer" | "real" | "complex"
        namespace="alg_vieta",       # 전역 고유 변수명 (충돌 방지)
        input_schema={...},
        output_schema={...},
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=10,
        category="algebra",
        tags=["polynomial", "vieta", "roots"],
        exam_types=["AIME"],
        # Bridge 인터페이스 (선택)
        bridge_output_keys=["roots", "coefficients"],  # 하류 모듈에 전달할 중간값
        bridge_input_accepts=["order", "prime"],        # 상위 모듈에서 받을 값
    )

    # ── 필수 구현 ──
    def generate_seed(self, difficulty_hint: float) -> dict: ...
    def execute(self, seed: dict) -> int: ...            # 반드시 0–999
    def get_logic_steps(self, seed: dict) -> list[str]: ...

    # ── Bridge 구현 (bridge_output_keys 선언 시 필수) ──
    def get_bridge_output(self, seed: dict) -> dict: ...
    def generate_seed_with_bridge(self, bridge: dict, difficulty_hint: float) -> dict: ...

    # ── 독립 검증 (터미널 모듈 권장) ──
    def verify_with_sympy(self, seed: dict) -> int | None: ...

    # ── 자동 제공 (오버라이드 불필요) ──
    def validate_answer(self, answer: int) -> tuple: ...
    def get_daps_contribution(self, seed: dict) -> float: ...
```

**Seed 안전 범위 패턴 (100회 Fallback 필수):**
```python
for _ in range(100):
    seed = _sample_seed()
    if 0 <= execute(seed) <= 999:
        return seed
return FALLBACK_SEED
```

---

## 9. Bridge Seed — 모듈 체이닝 아키텍처

```
[이전] 독립 실행 + 답 덧셈:
  correct_answer = (ans_A + ans_B) % 1000  ← 두 개의 독립 문제

[현재] Bridge Chain:
  Module A → get_bridge_output(seed_A) → {"order": 5, "prime": 11}
                ↓ bridge dict 전달
  Module B → generate_seed_with_bridge(bridge) → n_pairs = order = 5
                ↓
  Module B → execute(seed_B) → correct_answer (하나의 통합된 답)
```

**Bridge 호환성 판단 (module_registry.py):**
1. 네임스페이스 충돌 검사
2. 도메인 호환성 검사 (integer ↔ real)
3. 실행 기반 테스트 (generate_seed + execute + validate)
4. **Bridge 탐지:** `A.bridge_output_keys ∩ B.bridge_input_accepts ≠ ∅`

**데이터:** `module_bridge_connections` 테이블 (SQLite)
**최적 순서:** `find_best_chain()` — Bridge 연결 최대화 순열 탐색
**조합 정렬:** `composite_score = Bridge 50점 + Score(이력)`

---

## 10. Novelty Check — 참신성 검증

```
[Layer 1 — 구조적] 모듈 tags Jaccard 유사도
  현재 문제 tags vs 기존 VERIFIED 문제 tags
  임계값: ≥ 0.70 → 구조 중복 판정

[Layer 2 — 텍스트] 지문 TF-IDF cosine similarity
  현재 narrative vs 기존 narrative
  LaTeX 명령어(\frac, \sqrt)를 토큰으로 보존
  임계값: ≥ 0.60 → 텍스트 중복 판정
```

**구현 위치:** `agents/novelty_checker.py` (Pure Python, LLM 없음)
**호출 시점:** BEq PASS 후, DB 저장 전
**중복 시:** fix_history에 "다른 서술 방식" 요청 → Writer 재시도

---

## 11. 알려진 버그 패턴 (코드 작성 시 반드시 회피)

| 패턴 | 원인 | 처치 |
|------|------|------|
| `\text{circ}` LaTeX 오류 | LLM 환각 | `^\\circ`로 대체 |
| 마크다운 코드블록 래핑 | LLM 응답 포맷 | `{...}` 정규식 추출 |
| DB 경로 오류 | 상대 경로 | 항상 절대 경로 사용 |
| 혁신의 저주 반복 | Writer 프롬프트 약함 | "logic_steps 외 조건 추가 금지" 명시 강화 |
| Writer 정답 에코 | 프롬프트에 정답 포함 | 정답 비공개 + LLM 자체 풀이 유도 |
| execute() dict 반환 | 일부 모듈이 dict 반환 | Pipeline에서 첫 번째 int 추출 방어 |
| Bridge 없는 조합 | bridge_output_keys 미선언 | ⚠️ 경고 출력 + additive 폴백 |

---

## 12. 코드 품질 기준

**Python:**
- 모든 함수 시그니처에 타입 힌트 필수
- 모든 LLM 호출은 `async def` 비동기
- 스탠드얼론 스크립트는 절대 경로 사용
- Base Inheritance: 모든 Solver는 `AtomicModule` 상속

**LaTeX:**
- 각도: `^\\circ` (금지: `\\text{circ}`)
- 인라인: `$...$` / 블록: `$$...$$` 혼용 금지
- 곱셈: `\\times` (금지: `*`)

**Frontend (Next.js + TypeScript):**
- 수식: KaTeX 전용, Raw LaTeX 사용자 노출 금지
- 아이콘: `lucide-react` 통일
- 스타일: Tailwind CSS, Zinc/Slate 다크 테마

---

## 13. LLM 모델 할당 — 3사 완전 분리 (3-Company Separation)

| 에이전트 | 모델 (config.py) | 회사 | 역할 |
|----------|-------------------|------|------|
| Architect | `gpt-4o-mini` | OpenAI | Top-K 후보 중 최적 조합 선택 (경량 모델로 충분) |
| Writer | `gpt-4o` → `claude-sonnet` | OpenAI/Anthropic | 지문 서술 (기법 이름 은폐, 통합 서사) |
| Evaluator | `gemini-2.5-flash` | Google | 역추론 (Writer와 반드시 다른 회사 모델) |
| Judge | Pure Python | — | BEq 판정 + DAPS 사후 측정 (LLM 없음) |
| Novelty Checker | Pure Python | — | 참신성 검증 Jaccard + TF-IDF (LLM 없음) |

**3사 편향 분리 원칙:**
- 쓰는 놈(Anthropic/OpenAI) ≠ 푸는 놈(Google) ≠ 고르는 놈(OpenAI-mini)
- 같은 모델이 쓰고 검증하면 확증 편향 발생 → 반드시 다른 회사 모델 사용

**비용 최적화:** Architect 입력을 경량화 (META 전체 → name+tags+daps만 전송, 50K→5K 토큰)

## 13-A. Jaccard 전이 확률 행렬 + 2-Track 조합 샘플링

```
[Track A — Exploitation 80%]
  Jaccard 연관 계수 기반 composite_score 정렬 → 기출에서 검증된 시너지 조합 우선

[Track B — Exploration 20%]
  전이 확률 행렬 위 마르코프 Random Walk + DAPS 기각 샘플링 → 창의적 신규 조합 탐색
  Temperature τ > 1 → 저확률 쌍도 선택 가능
  BEq 통과 시 행렬에 피드백 → 자가 진화
```

**구현 위치:** `co_occurrence_matrix.py` → `CoOccurrenceMatrix` 클래스
**데이터 소스:** `data/problem_module_map.json` (1,065 AIME 기출 매핑)
**비제로 Jaccard 쌍:** 788개

## 13-B. Test Harness

```bash
python -m engine_v2.harness --n 10 --daps 10.0 --tag "baseline"
python -m engine_v2.harness --compare tag_a tag_b
```

**수집 메트릭:** BEq 통과율, 기법 은폐율, DAPS 분포, Bridge 사용률, 평균 소요시간, LLM 호출 횟수
**구현 위치:** `harness.py` → `PipelineHarness` 클래스

---

## 14. DB 스키마 요약

### SQLite (`amc_factory_v2.db`) — module_registry.py 관리
| 테이블 | 용도 |
|--------|------|
| `modules` | 등록된 AtomicModule 메타데이터 |
| `module_compatibility` | 쌍별 호환성 캐시 (COMPATIBLE/INCOMPATIBLE) |
| `module_bridge_connections` | source → target Bridge 키 목록 |
| `combination_metrics` | 조합별 성과 이력 (estimated/measured DAPS, verdict, fail_reason) |

### PostgreSQL (`amc_factory_v2`) — pipeline_v2.py 관리 (USE_POSTGRES=true 시)
| 테이블 | 용도 |
|--------|------|
| `blueprints` | 문제 설계 청사진 |
| `blueprint_modules` | 청사진-모듈 연결 |
| `variants` | 최종 생성 문제 (narrative, seed, answer, DAPS) |
| `mas_logs` | 에이전트별 대화 로그 |
| `daps_scores` | variant별 DAPS 점수 |

---

## 15. 선제적 제언 원칙

코드 작성 요청 시 다음 상황을 항상 먼저 확인하고 제언합니다:

- Circuit Breaker 없는 루프 → Fallback 추가 제안
- LLM이 수학 판단을 하는 구조 → Two-Engine 경계 위반 경고
- DAPS 허용 오차 ±1.5 초과 → 필터 강화 제안
- `combination_metrics` 미기록 → fail_reason 분류 누락 경고
- Seed 안전 범위 100회 Fallback 누락 → 추가 제안
- `bridge_output_keys` 없는 모듈 → Bridge 인터페이스 구현 권장
- `verify_with_sympy()` 미구현 터미널 모듈 → Branch B 구현 권장
- Writer 프롬프트에 정답 직접 노출 → Two-Engine 위반 경고
