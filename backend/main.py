from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys

# Ensure the backend directory is in the system path for internal imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.api.v2.endpoints import synthesis
from app.core.config import settings

# Initialize FastAPI with professional metadata for Swagger UI
app = FastAPI(
    title=f"🚀 {settings.PROJECT_NAME}",
    description="""
AI_MathMate API powers a sophisticated AIME problem generation engine.
It uses a solver-centric pipeline to generate deterministic math problems 
and leverages LLMs for narrative weaving.

## Core Features
* **AIME Mock Generation**: Full 15-problem mock exams.
* **Drill Workshop**: Targeted concept practice with LV1-LV3 difficulty.
* **Problem Verification**: Zero-hallucination verification using symbolic math.
""",
    version=settings.VERSION,
    openapi_url=f"/api/v2/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Global Exception Handler for Resilience
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches all unhandled exceptions and returns a professional JSON response.
    This prevents the API from leaking sensitive tracebacks in production.
    """
    # Log the error for internal monitoring
    print(f"ERROR: Unhandled exception occurred: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An unexpected internal server error occurred.",
            "detail": str(exc) if settings.PROJECT_NAME.lower() == "test" else "Please contact support."
        },
    )

# CORS configuration for local development and potential production origins
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files to serve generated problem illustrations (Heritage 90)
images_path = os.path.join(backend_dir, 'images')
if not os.path.exists(images_path):
    os.makedirs(images_path)
app.mount("/images", StaticFiles(directory=images_path), name="images")

# Register API V2 - Heritage 90 Synthesis Engine
app.include_router(
    synthesis.router, 
    prefix="/api/v2", 
    tags=["AIME Heritage 90 Synthesis"]
)

@app.get("/", tags=["Health Check"])
def read_root():
    """Returns the API status and project name."""
    return {"status": "online", "project": settings.PROJECT_NAME}

if __name__ == "__main__":
    import uvicorn
    # Log startup message
    print(f"Starting {settings.PROJECT_NAME} API at http://0.0.0.0:8088")
    # Using the app object directly and disabling reload to avoid Windows subprocess/path issues
    print("Finishing server startup...")
    uvicorn.run(app, host="0.0.0.0", port=8089)
