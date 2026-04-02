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

### 3.1 DNA-Driven 생성 (Ground Truth 분리)
```
AtomicModule.execute(seed) → 정답(Ground Truth, 변경 불가)
                          ↓
LLM Writer                → LaTeX 지문 (서술만 담당)
                          ↓
LLM Evaluator             → 역추론으로 정답 재도출
                          ↓
Judge (Pure Python)       → BEq 판정 → PASS시에만 DB 저장
```

### 3.2 참신성 검증 레이어 (Novelty Check)
새로운 문항 생성 시 다음 두 계층에서 중복을 차단합니다:
1. **Seed 레이어**: 모듈 ID + 핵심 파라미터 해시 비교 → 수치 클론 차단 (우선)
2. **Narrative 레이어**: 지문 임베딩 → 코사인 유사도 0.85 이상이면 반려 (보조)

### 3.3 DAPS 기반 품질 보증
배포되는 모든 문항은 `daps_scores` 테이블에 최종 점수가 기록됩니다.
`δ(Heuristic/Trap)` 가중치가 2.0 이상인 문항은 자동으로 MASTER 밴드로 분류됩니다.

### 3.4 비동기 처리 원칙
모든 LLM 호출은 비동기(`async/await`) FastAPI 엔드포인트를 통해 처리하여,
문항 생성이 사용자 요청을 블로킹하지 않습니다.
