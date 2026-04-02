# AIME Engine V2: Heritage 90 Synthesis System

This directory contains the core logic for the **V2 AIME Synthesis Engine**, a Multi-Agent System (MAS) designed to generate competition-grade mathematical problems through atomic deconstruction and neuro-symbolic verification.

## 📂 Directory Structure

```text
backend/engine_v2/
├── agents/             # MAS Role Definitions (Architect, Writer, Verifier)
├── modules/            # Heritage 90 Knowledge Atoms
│   ├── algebra/        # Roots of Unity, Polynomials, etc.
│   ├── geometry/       # Synthetic and Analytic methods
│   ├── combinatorics/  # Extremal, Invariants, etc.
│   └── meta/           # Tier 0 Strategist (Symmetry Breaker, Trace Removal)
├── scripts/            # Deployment & Orchestration Scripts
└── iipc_validator.py   # Neuro-Symbolic Consistency Checker
```

## 🚀 Key Orchestrator

The primary entry point for high-rigor problem synthesis is:
`scripts/aime_high_rigor_orchestrator.py`

Execute this script to orchestrate a full synthesis pipeline for AIME #15 level problems:
```bash
python -m backend.engine_v2.scripts.aime_high_rigor_orchestrator
```

## 🧠 The 'Heritage 90' Atom System

V2 deconstructs mathematical intelligence into 90 granular "atoms." By recombining these atoms under the guidance of a **Tier 0 Strategist**, the engine avoids the "determinism trap" of V1 and generates structurally novel variants that test true mathematical intuition rather than pattern recognition.

---
**Core Engine V2 Architect: Siyoul Jung**
