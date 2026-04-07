# AIME-problem-generator: Neuro-Symbolic AIME Problem Generation Engine

> **Multi-Agent System that synthesizes competition-grade mathematics problems with deterministic correctness guarantees**

---

## Project Overview

**AI MathMate** generates novel AIME (American Invitational Mathematics Examination) problems by combining deterministic Python solvers with LLM-powered narrative generation. The engine decomposes 1,065 historical AIME problems into 85 atomic knowledge modules, then recombines them using a Jaccard co-occurrence transition matrix to produce mathematically rigorous, creatively novel problems.

### Key Innovation: Two-Engine Philosophy
```
[Deterministic Engine]  Python AtomicModule.execute(seed) --> correct_answer (100% reliable)
                        AtomicModule.verify_with_sympy(seed) --> Branch B independent verification
        |
[Narrative Engine]      LLM Writer --> LaTeX problem statement (verified by BEq)
                        Writer does NOT know the answer -- must derive it independently
```

**LLMs never perform mathematical computation.** They only write narratives. All math is handled by Python + SymPy.

---

## Architecture

### Multi-Agent System (MAS) Pipeline

```
[Architect]     Selects module combination via Jaccard transition matrix
    |           (Track A: exploitation 80% / Track B: Markov exploration 20%)
    v
[Modules]       Bridge Chain execution: A.bridge_output --> B.seed_with_bridge
    |           Deterministic seed generation + execute() + verify_with_sympy()
    v
[Writer]        Generates LaTeX narrative from seed + logic_steps
    |           Technique names are concealed (no "Vieta's formulas" in text)
    v
[Evaluator]     Solves the problem independently (different company model)
    |           Bias separation: Writer(OpenAI/Anthropic) != Evaluator(Google)
    v
[Judge]         BEq verification: Python answer == Evaluator answer?
    |           DAPS post-measurement: alpha + beta + gamma + delta
    v
[Novelty]       Jaccard(tags) + TF-IDF(narrative) duplicate detection
```

### Module Combination Selection

Instead of random pairing, modules are combined based on **empirical co-occurrence data** from 1,065 historical AIME problems:

- **Jaccard Transition Matrix**: 788 non-zero module pairs with co-occurrence frequencies
- **2-Track Sampling**: Track A (Jaccard-ranked exploitation) + Track B (Markov chain exploration)
- **Bridge Chain**: Modules pass intermediate mathematical values (vertices, radii, primes) to create unified problems
- **DAPS Rejection Sampling**: Only combinations matching target difficulty are accepted

### DAPS (Difficulty Assessment & Prediction Score)

```
DAPS = alpha(Computational) + beta(LogicalDepth) + gamma(Combination) + delta(Heuristic)

alpha: Computational keyword density in Evaluator's solution steps (0-5)
beta:  Number of logical steps x 0.8 (0-5)
gamma: (module_count - 1) x 1.0 (0-3)
delta: Evaluator confidence inverse (HIGH=0, MEDIUM=1.5, LOW=3.0)

Bands: Challenger(6-9) | Expert(9-12) | Master(12-16)
```

---

## Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Math Engine** | Python 3.12, SymPy, Fractions | Deterministic computation, Branch B verification |
| **LLM Orchestration** | OpenAI GPT-4o, Google Gemini 2.5, Anthropic Claude | 3-company bias separation |
| **Data Pipeline** | SQLite (module registry, compatibility, metrics) | Module compatibility cache, co-occurrence matrix |
| **Frontend** | Next.js 15, TypeScript, Tailwind CSS, KaTeX | Problem display, drill workshop |
| **Backend API** | FastAPI, PostgreSQL (optional) | REST endpoints, problem storage |
| **Quality Assurance** | Test Harness, BEq verification, Novelty checker | Batch testing, A/B comparison |

---

## Project Structure

```
AI_MathMate/
├── backend/
│   └── engine_v2/
│       ├── pipeline_v2.py              # MAS pipeline orchestrator
│       ├── module_registry.py          # Module DB, compatibility, Bridge detection
│       ├── co_occurrence_matrix.py     # Jaccard transition matrix + Markov sampling
│       ├── harness.py                  # Test harness for batch evaluation
│       ├── config.py                   # Model assignments, DAPS weights, sampling params
│       ├── agents/
│       │   ├── base_agent.py           # BaseAgent + AgentResult
│       │   ├── architect.py            # Module combination selector (Gemini/GPT)
│       │   ├── writer.py               # LaTeX narrative generator (GPT-4o)
│       │   ├── evaluator.py            # Independent solver (Gemini)
│       │   ├── judge.py                # BEq verdict + DAPS measurement (Python)
│       │   └── novelty_checker.py      # Jaccard + TF-IDF duplicate detection (Python)
│       ├── modules/                    # 85 AtomicModules
│       │   ├── base_module.py          # AtomicModule ABC + ModuleMeta + StrategyMixin
│       │   ├── algebra/               # 21 modules
│       │   ├── geometry/              # 24 modules
│       │   ├── number_theory/         # 15 modules
│       │   ├── combinatorics/         # 17 modules
│       │   └── meta/                  # 8 strategy modules
│       ├── data/
│       │   ├── problem_module_map.json # 1,065 AIME problems -> module mappings
│       │   ├── cross_validation_result.json
│       │   └── modules_master_v3.md    # Module registry documentation
│       ├── scripts/
│       │   └── register_all_85.py      # Batch module registration
│       └── tools/
│           ├── 5_reverse_map_problems.py
│           └── 6_cross_validate_claude.py
├── frontend/                           # Next.js 15 + TypeScript
├── CLAUDE.md                           # Development guide & constraints
└── README.md
```

---

## Quantitative Status

| Metric | Value |
|--------|-------|
| AtomicModules | 85 (21 algebra, 24 geometry, 15 NT, 17 combinatorics, 8 meta) |
| Module compatibility | 3,570 pairs tested, 100% compatible |
| Bridge connections | 30 directional links, 45 unique combinations |
| 3-module chains | 15 verified chains |
| Co-occurrence matrix | 788 non-zero Jaccard pairs from 1,065 AIME problems |
| BEq pass rate (Bridge combos) | ~50% (improving with Writer model upgrades) |
| DAPS measurement accuracy | +/- 0.4 deviation from estimate |
| Pre-computation speed | 0.065s for 3,570-pair ranking (537x optimized) |

---

## Quick Start

### Prerequisites
- Python 3.12+
- API keys: OpenAI, Google Gemini, Anthropic (optional)

### Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your API keys

# Register all 85 modules
python -m engine_v2.scripts.register_all_85

# Generate a single problem
python -c "
from engine_v2.pipeline_v2 import EngineV2Pipeline
pipeline = EngineV2Pipeline()
result = pipeline.generate_problem(target_daps=10.0)
print(result['narrative'])
"
```

### Test Harness
```bash
# Batch generate 10 problems and collect metrics
python -m engine_v2.harness --n 10 --daps 10.0 --tag "baseline"

# Compare two configurations
python -m engine_v2.harness --n 10 --writer gpt-4o-mini --tag "mini"
python -m engine_v2.harness --n 10 --writer gpt-4o --tag "4o"
python -m engine_v2.harness --compare mini 4o
```

---

## Module Interface

Every module implements the `AtomicModule` interface:

```python
class MyModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_triangle_properties",
        domain="integer",
        bridge_output_keys=["side_a", "side_b", "side_c", "circumradius"],
        bridge_input_accepts=["vertices"],
        ...
    )
    
    def generate_seed(self, difficulty_hint: float) -> dict: ...
    def execute(self, seed: dict) -> int: ...           # Must return 0-999
    def verify_with_sympy(self, seed: dict) -> int: ... # Independent verification
    def get_bridge_output(self, seed: dict) -> dict: ... # Pass data to next module
    def generate_seed_with_bridge(self, bridge: dict, difficulty_hint: float) -> dict: ...
```

---

## Roadmap

- [x] 85 AtomicModules with execute + verify_with_sympy
- [x] Module Registry with compatibility testing + Bridge detection
- [x] Jaccard co-occurrence transition matrix from 1,065 AIME problems
- [x] 2-Track sampling (exploitation + Markov exploration)
- [x] Bridge Chain execution (30 connections, 45 combinations)
- [x] E2E pipeline: Architect -> Module -> Writer -> Evaluator -> Judge -> Novelty
- [x] Test Harness with batch execution + A/B comparison
- [x] 537x pre-computation optimization (memory caching)
- [ ] 3-company LLM bias separation (Writer/Evaluator/Architect)
- [ ] Z3 SMT solver integration for pre-Writer constraint validation
- [ ] Bridge expansion to 60+ combinations
- [ ] BEq pass rate optimization to 80%+
- [ ] Frontend problem drill workshop
- [ ] Production deployment with cost-optimized model selection

---

## License

Proprietary. All rights reserved.

---

**Developed by Siyoul Jung** | Mathematical AI Engineering
