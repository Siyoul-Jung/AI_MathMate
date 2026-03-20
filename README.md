# AI MathMate: Adaptive AI Engine for AIME Excellence

AI MathMate is an advanced full-stack educational platform designed to generate and validate high-competition mathematical problems. By engineering a specialized pipeline around Large Language Models(LLMs), this project transforms abstract mathematical logic into highly structured, predictable educational content.

## Key Engineering Features

### LLM Output Control and Strict JSON Structuring
Unlike simple prompt wrappers, AI MathMate enforces strict output schemas. The backend logic relies on advanced NLP prompts to ensure the LLM consistently returns complex mathematical narratives, hints, and solutions in highly predictable, parsed JSON formats.

### DNA-Driven Problem Generation Pipeline
The system separates mathematical logic from narrative synthesis. Core mathematical seeds are algorithmically generated and verified for solvability using Python before being processed by the LLM. This pipeline ensures absolute factual accuracy and eliminates hallucinations in the core mathematical concepts.

### Full-Stack Architecture and Low-Latency APIs
Built with a robust FastAPI backend and a Next.js frontend, the system handles real-time AI inferences efficiently. RESTful APIs connect the backend with the frontend, ensuring reliable data flow and bridging complex backend processing with an intuitive user interface.

### Adaptive Scaffolding System
The platform features a Drill Bridge that provides a seamless transition from complex AIME problems to targeted conceptual practice. The system dynamically serves Level 1 to 3 drills to isolate specific concepts, demonstrating strong algorithmic state management.

## Technical Stack

### Backend Architecture
- **Language**: Python
- **Framework**: FastAPI with Uvicorn for asynchronous performance
- **AI Integration**: OpenAI GPT-4o-mini
- **Database**: SQLite for stable problem storage and variant management

### Frontend Experience
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript for robust state management
- **Styling**: Tailwind CSS and Vanilla CSS for a premium glassmorphism aesthetic
- **Math Rendering**: KaTeX for high-performance inline and block equation display

## System Architecture Pipeline

```plaintext
[AIME SOLVER DNA] -> [PYTHON SEED GENERATOR] -> [NARRATIVE LLM]
                                                |
[JSON SCHEMA VALIDATION] <----------------------+
|
[FASTAPI ENDPOINT (backend/app)] <-> [SQLITE DB]
|
[NEXT.JS FRONTEND UI (frontend/app)]
```

## Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/Siyoul-Jung/AI_MathMate.git
cd AI_MathMate
# Install backend dependencies
cd backend
pip install -r requirements.txt
# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Environment Configuration
Create a `.env` file in the `backend/` directory:
```bash
cd backend
cp .env.example .env
```
Edit `backend/.env` to include your OpenAI API Key:
```
OPENAI_API_KEY=your_key_here
```

**Frontend Environment:**
Create a `.env.local` file in the `frontend/` directory (optional if using default localhost:8001):
```bash
cd ../frontend
cp .env.local.example .env.local
```

### 3. Running the Platform
**Start Backend API:**
```bash
cd backend
python main.py
```
**Start Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Running Tests (Optional)
To verify the backend installation and core logic:
```bash
cd backend
python -m pytest tests/
```

## Future Roadmap

The AI MathMate engine is designed with modularity at its core, allowing for seamless expansion into broader mathematical disciplines:

- **AMC Series Integration**: Expanding the DNA-driven generator to support AMC 8, 10, and 12 problem sets.
- **K-Math Curriculum Adaptivity**: Incorporating local K-math (Korean curriculum) standards for broader accessibility.
- **Enhanced Scaffolding Architecture**: Developing a "Peer-to-Peer" AI tutoring module for more nuanced step-by-step guidance.
- **Multi-Modal Problem Generation**: Integrating visual geometry recognition and generation using multimodal LLM capabilities.

## License & Copyright
This project is for educational purposes. 
The mathematical structures are inspired by the AIME 2025 I exam. 
Original AIME problems are copyright © [Mathematical Association of America (MAA)](https://www.maa.org/).

---
*Developed as a high-fidelity demonstration of AI-driven pedagogy.*