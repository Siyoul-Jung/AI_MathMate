# Implementation Plan: Initial MathMate System

## 1. Architecture Overview

### Backend (Python/FastAPI)
- **Core Engine**: `BaseTMaster` class for standardized problem generation.
- **Math Utilities**: `MathUtils` for number theory and algebra, `GeometryUtils` for SVG generation.
- **Curriculum Modules**: Hierarchical organization (`curriculum/kr/middle/...`).
- **AI Service**: `LLMService` wrapping OpenAI API for diagnosis and advice.
- **Analytics**: `AnalyticsService` using SQLite for tracking student progress.
- **API Server**: FastAPI exposing endpoints for generation, diagnosis, and analytics.

### Frontend (Next.js/React)
- **UI Components**: `ProblemViewer`, `Dashboard` for modular UI.
- **State Management**: React hooks for managing problem state and user interaction.
- **Math Rendering**: `react-katex` for LaTeX rendering.
- **API Integration**: Fetch API for communicating with the backend.

## 2. Data Models

### Problem Object (JSON)
```json
{
  "id": "T-Code",
  "question": "LaTeX formatted string",
  "answer": "String",
  "options": ["Array of strings"],
  "explanation": "String or Array",
  "logic_steps": [
    { "step_id": 1, "description": "...", "target_expr": "...", "concept_id": "..." }
  ],
  "image": "SVG string (optional)"
}
```

### Student Log (SQLite)
- `student_step_log`: Stores each attempt (success/fail) per standard.

## 3. Implementation Phases

### Phase 1: Core Engine & Basic Generation
- [x] Implement `BaseTMaster` and `MathUtils`.
- [x] Implement `ProblemManager` for dynamic module loading.
- [x] Create initial curriculum modules (Middle 1-1).

### Phase 2: Frontend & Interaction
- [x] Setup Next.js project.
- [x] Implement `ProblemViewer` with KaTeX support.
- [x] Connect Frontend to Backend API.

### Phase 3: AI & Analytics
- [x] Implement `LLMService` for diagnosis.
- [x] Implement `AnalyticsService` and SQLite integration.
- [x] Create `Dashboard` component for visualization.

### Phase 4: Content Expansion & Refinement
- [x] Expand curriculum to Middle 2-1 and High School Common Math.
- [x] Refine `logic_steps` for better hinting (remove answer leakage).
- [x] Apply LaTeX formatting across all modules.
- [x] Implement theme differentiation for categories.

## 4. Complexity Tracking
- **Module Loading**: Dynamic loading via `manifest.json` allows decoupling of content from the engine.
- **LaTeX Parsing**: Custom regex in `ProblemViewer` handles mixed text/math content.
- **Hint Generation**: Fallback logic in `BaseTMaster` ensures hints exist even if not explicitly defined, though explicit definition is preferred.