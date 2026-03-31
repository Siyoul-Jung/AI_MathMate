# AI_MathMate: Neuro-Symbolic AIME Generation Engine

> **Pioneering the Future of Mathematical Reasoning with the 'Heritage 90' MAS Architecture**

---

## 🚀 Project Vision: Beyond Solving, Into Synthesis
**AI_MathMate** is a next-generation mathematical engine designed to bridge the gap between LLM creativity and symbolic rigor. While traditional systems struggle with the "last mile" of mathematical accuracy, AI_MathMate leverages a **Multi-Agent System (MAS)** to synthesize, verify, and deliver competition-grade AIME (American Invitational Mathematics Examination) problems.

### 💎 The V2 Breakthrough: Heritage 90
We have evolved from simple task-specific solvers (V1) to a **Generative Atomic Framework (V2)**. By deconstructing 1,000+ historical problems into 90 granular "Knowledge Atoms," our engine can now compose an infinite variety of novel, high-rigor (AIME 13-15) challenges.

👉 **[Read the Full Technical Migration Report (V1 to V2)](./docs/MIGRATION_V1_TO_V2.md)**

---

## 🧠 Core Architecture

### 1. Heritage 90 Atomic Framework
Math principles are treated as "Logic Bricks." Our library of 90 atoms (Algebra, Geometry, NT, Combo) allows for complex DAG-based problem synthesis.

### 2. Tier 0 Strategist Layer (Anti-Fakesolve)
To prevent "formulaic guessing," our strategist agents apply advanced de-biasing techniques:
- **Trace-Removal**: Masking geometric scaffolding to force intuitive leaps.
- **Symmetry Breaker**: Injecting asymmetric constants to invalidate pattern-based guessing.

### 3. Neuro-Symbolic IIPC Loop
Every problem is validated through our **Iteratively Improved Program Construction (IIPC)** pipeline, ensuring 100% mathematical integrity and a unique answer between 001-999.

---

## 🛠 Tech Stack

- **Reasoning**: Google Gemini 2.5 (Pro/Flash)
- **Symbolic Engine**: SymPy, Z3 Theorem Prover, Custom Python Solvers
- **Frontend**: Next.js 15, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, PostgreSQL (Metadata Management), SQLite (Compatibility Cache)
- **Orchestration**: Custom Multi-Agent Pipeline (Architect, Writer, Verifier)

---

## 📂 Project Structure
- `/backend/engine_v2`: The core V2 generative engine.
- `/backend/engine_v2/modules`: The "Heritage 90" knowledge atoms.
- `/docs`: Technical blueprints and migration reports.
- `/frontend`: Modern learning dashboard & drill workshop.

---

## [KOREAN SUMMARY / 국문 요약]

**AI_MathMate**는 LLM의 창의성과 심볼릭 연산의 엄밀함을 결합한 차세대 수학 문제 생성 엔진입니다. 
- **V2 혁신**: 1:1 솔버 방식(V1)에서 벗어나, 90종의 지식 원자를 합성하는 **'Heritage 90'** 아키텍처를 도입했습니다.
- **주요 기술**: 출제자의 의도를 모사하는 전략 계층(Tier 0), 난이도 정밀 제어(DAPS), 그리고 신경-기호 결합 검증(IIPC)을 통해 AIME 킬러 문항을 무결하게 생성합니다.
- **학습 경험**: 실전 모의고사와 취약 개념을 보완하는 '드릴 워크숍'을 통해 학습 효율을 극대화합니다.

---
Developed as a high-impact engineering portfolio by **Siyoul Jung**.