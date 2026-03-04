# MathMate Constitution

## Article I: Parametric Generation Principle
All math problems MUST be generated algorithmically using parametric templates.
Static database entries for problems are prohibited.
Every problem generator must support variable difficulty levels and multiple question types.

## Article II: Logic-First Architecture
Every problem generation module MUST produce `logic_steps` alongside the question and answer.
These steps serve as the ground truth for:
1. Step-by-step hints for students.
2. AI diagnostic context for error analysis.

## Article III: Clean Answer Guarantee
All generated problems MUST be inversely designed to produce "clean" answers (integers or simple fractions) unless the learning objective specifically requires otherwise (e.g., irrational number concepts).
Random generation without constraints is strictly forbidden.

## Article IV: Hybrid AI Integration
The system utilizes a hybrid approach:
- **Deterministic Logic (SymPy/Python)**: For problem generation and exact answer calculation.
- **Probabilistic AI (LLM)**: For pedagogical interaction, explanation refinement, and error diagnosis.
The LLM shall NEVER be used for calculation or problem generation where exactness is required.

## Article V: Modular Curriculum Structure
The codebase MUST reflect the hierarchical structure of the national curriculum:
`Curriculum` -> `Grade` -> `Standard` -> `Type (T-Code)`
Each standard must be encapsulated in its own module.

## Article VI: Interface Standardization
All problem generators MUST inherit from `BaseTMaster` and implement the standard `generate` interface.
The output format must strictly adhere to the defined JSON schema, including LaTeX formatting for mathematical expressions.

## Article VII: Spec-Driven Workflow
Development follows the Specification-Driven Development (SDD) methodology.
Specifications are the source of truth. Code is the generated artifact.
Changes to logic or behavior must be preceded by updates to the specification.
