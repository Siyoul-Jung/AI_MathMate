# AI_MathMate: Solver-Centric AIME Mock/Drill Platform

AI_MathMate is a sophisticated mathematical education platform designed to elevate AIME (American Invitational Mathematics Examination) preparation. It combines custom-coded mathematical solvers with LLM-based narrative generation to provide an infinite supply of rigorous, verified, and pedagogically sound practice problems.

## 🚀 Key Features

- **Solver-Driven Pipeline**: Unlike traditional RAG systems, AI_MathMate uses deterministic Python solvers to define the "Mathematical DNA" of a problem, which is then used by Gemini to weave complex narratives.
- **Two-Track Learning**:
  - **Final Mock**: Simulates the real AIME experience with 15 problems ranging from Challenger to Master levels.
  - **Drill Workshop (Drill Bridge)**: When a student struggles, the "Drill Bridge" offers targeted practice on foundational concepts (LV1-LV3) relevant to the specific AIME problem.
- **Visual Intelligence**: Automatically generates geometric and combinatorial illustrations using custom `matplotlib` logic.
- **Zero-Hallucination Architecture**: Every answer is verified by local solver execution before being served to the user.

## 🛠 Tech Stack

- **Frontend**: Next.js 15 (App Router), Tailwind CSS, Framer Motion.
- **Backend**: FastAPI (Python), SQLite, SQLAlchemy.
- **AI/LLM**: Google Gemini API, Custom Solver-to-Prompt Pipeline.
- **DevOps**: Docker, Docker Compose.

## 🐳 Quick Start with Docker

Ensure you have Docker and Docker Compose installed.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/AI_MathMate.git
   cd AI_MathMate
   ```

2. **Set Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Run with Docker Compose**:
   ```bash
   docker compose up --build
   ```

4. **Access the Application**:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8088`

## 📂 Project Structure

- `/frontend`: Next.js application and UI components.
- `/backend`: FastAPI server and engine services.
- `/backend/amc_engine`: The core math engine containing solvers and the generation pipeline.
- `/backend/amc_factory.db`: Pre-generated and verified problem variants.

---
Developed as a high-impact engineering portfolio project.