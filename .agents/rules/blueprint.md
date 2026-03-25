# blueprint: AI MathMate Architecture

## Technical Stack
- **Backend**: Python 3.10+ with FastAPI. Uvicorn as the ASGI server.
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS.
- **Database**: SQLite (local `amc_factory.db` and `problem_factory.db`) using standard `sqlite3` library.
- **AI Integration**: OpenAI GPT-4o-mini for problem narrative synthesis and validation.

## Directory Structure
- `/backend`: Core logic, API endpoints, and database management.
  - `/amc_engine`: Specialized logic for competition math (AIME/AMC).
  - `/kmath_engine`: Korean curriculum adaptation.
- `/frontend`: User interface and interactive modules.
  - `/app`: Next.js App Router pages.
  - `/components`: Reusable UI components (ProblemViewer, Dashboard, etc.).

## Core Principles
1. **DNA-Driven Generation**: Separate mathematical logic (Python seeds) from narrative (LLM).
2. **Strict Schema**: All LLM outputs must be validated against a JSON schema.
3. **Low Latency**: Use asynchronous FastAPI endpoints for AI inference bridging.
