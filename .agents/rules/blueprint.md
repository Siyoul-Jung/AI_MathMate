# blueprint: AI MathMate V2 아키텍처 명세

## 1. 기술 스택 (Tech Stack)

### 코어 백엔드
- **Runtime**: Python 3.10+ / FastAPI + Uvicorn (ASGI)
- **수학 엔진 (Ground Truth)**: 순수 Python `AtomicModule` (결정론적 Solver)
- **LLM 오케스트레이션**: `OpenAI GPT-4o-mini` (Writer/Architect) + `Google Gemini 2.0 Pro` (Evaluator, TikZ 생성)

### 데이터베이스
- **운영 DB**: `SQLite` → `amc_factory_v2.db` (variants, blueprints, mas_logs, daps_scores)
- **호환성 캐시**: `module_compatibility` 테이블 (ModuleRegistry 자동 관리)
- **참신성 검증 (Novelty Check)**: `Vector DB` — **ChromaDB** (로컬, Docker 친화적) 또는 `SQLite-VSS` (경량)

### 프론트엔드
- **Framework**: Next.js 14 (App Router) + TypeScript
- **스타일링**: Tailwind CSS + Glassmorphism 다크 테마
- **수식 렌더링**: KaTeX (모든 LaTeX 표현의 최종 렌더러)

### 미래 기술 스택 (Roadmap)
- **프롬프트 최적화**: `DSPy` — `mas_logs` 300개 이상 축적 후 Writer 에이전트 파일럿 도입
- **기하 작도**: `TikZ / Asymptote` → SVG 렌더링 파이프라인 (GEOMETRY 모듈 전용)

---

## 2. 디렉토리 구조 (Directory Structure)

```
AI_MathMate/
├── backend/
│   ├── engine_v2/              # V2 MAS 파이프라인 (핵심)
│   │   ├── pipeline_v2.py      # Architect → Writer → Evaluator → Judge 총괄
│   │   ├── module_registry.py  # AtomicModule 등록 및 호환성 자동 테스트
│   │   ├── config.py           # DAPS 임계값, DB 경로, 파이프라인 상수
│   │   ├── agents/             # MAS 에이전트
│   │   │   ├── architect.py    # 목표 DAPS에 맞는 모듈 조합 선택
│   │   │   ├── writer.py       # seed → LaTeX 지문 서술 (혁신의 저주 방지 지시)
│   │   │   ├── evaluator.py    # 지문 역추론 (Zero-Context Solving)
│   │   │   └── judge.py        # BEq 최종 판정 (Pure Python, LLM 없음)
│   │   └── modules/            # Atomic Modules (47개 수학 원자 단위)
│   │       ├── algebra/
│   │       ├── geometry/
│   │       ├── number_theory/
│   │       └── combinatorics/
│   ├── amc_engine/             # V1 Solver 레거시 (운영 중)
│   │   └── exams/2025/AIME1/{CHALLENGER,EXPERT,MASTER}/P01-P15/
│   ├── app/                    # FastAPI 라우터 (REST API)
│   └── scripts/                # 유지보수 스크립트
├── frontend/
│   ├── app/                    # Next.js App Router 페이지
│   └── components/             # UI 컴포넌트 (ProblemViewer, DrillBridge 등)
└── .agents/
    ├── rules/                  # AI 에이전트 핵심 가이드라인
    └── workflows/              # 반복 작업 표준 절차
```

---

## 3. 핵심 아키텍처 원칙 (Core Principles)

### 2.1 DAPS 공식 (V2 비선형 시너지 모델)

$$Total\_DAPS = (\sum_{i=1}^{n} \text{module}_i.daps) \times \text{Synergy}(cat_1, cat_2, ...) + \text{LogicLeap}(\gamma)$$

| 도메인 결합 (예시) | 시너지 계수 (Synergy) | 특성 |
|:---:|:---:|---|
| NT $\times$ Geometry | **1.4x** | 가장 이질적인 결합, 난이도 급상승 |
| Algebra $\times$ NT | **1.2x** | 고전적 융합 테마 |
| Single Domain | **1.0x** | 기본 가법성 유지 |

**주의:** 초기 가동 시 모든 시너지 계수는 **1.0**으로 시작하며, `combination_metrics` 데이터 축적에 따라 실측치로 수렴함.

### 2.2 허용 오차(Tolerance) 필터
- 목표 DAPS 대비 **±1.5** 이내의 조합만 최종 후보군에 진입 가능.
- MASTER급(13.5) 타겟 시 12.0~15.0 범위 엄격 준수.

### 2.3 설계 결정론: Deterministic Scoring
Architect(LLM)에게 후보를 넘기기 전, Python 레이어에서 다음 공식으로 순위를 확정함:
$Score = (P_{daps} \times S_{coeff} \times R_{pass}) - \text{min}(\sum W_{fail}, 45)$
- **$R_{pass}$**: 성공률 (데이터 부족 시 초기값 **0.7** 부여)
- **$W_{fail}$**: 실패 감점 상한은 **-45점**으로 제한하여 좋은 조합의 영구 매장 방지.
Judge (Pure Python)       → BEq 판정 → PASS시에만 DB 저장

### 3.2 참신성 검증 레이어 (Novelty Check)
새로운 문항 생성 시 다음 두 계층에서 중복을 차단합니다:
1. **Seed 레이어 (Highest Priority)**: 모듈 ID + 핵심 파라미터 해시 비교 → 수치 클론 차단. 동일 Seed는 Narrative가 달라도 반려함.
2. **Narrative 레이어 (Supplementary)**: 지문 임베딩 → 코사인 유사도 0.85 이상이면 반려. (단, 수학적 도약점이 다름이 증명되면 예외 허용 가능)

### 3.3 설계 자가 학습 (Feedback Loop)
시스템은 생성 과정에서 발생하는 모든 현상을 데이터베이스화하여 Architect의 판단을 보정합니다.
- **성능 기록**: `combination_metrics` 테이블을 통해 모듈 조합별 성공/실패율을 영구 추적.
- **결정론적 점수제**: Python 레이어에서 점수를 계산하여 상위 후보만 Architect에게 전달함으로써 선택 품질을 보장.

### 3.4 비동기 처리 원칙
모든 LLM 호출은 비동기(`async/await`) FastAPI 엔드포인트를 통해 처리하여,
문항 생성이 사용자 요청을 블로킹하지 않습니다.
