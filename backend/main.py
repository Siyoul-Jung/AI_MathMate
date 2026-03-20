from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys

# Ensure backend directory is in sys.path for internal imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.api.v1.endpoints import problems
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS configuration
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

# Mount static files for images
images_path = os.path.join(backend_dir, 'amc_engine', 'images')
if not os.path.exists(images_path):
    os.makedirs(images_path)
app.mount("/images", StaticFiles(directory=images_path), name="images")

# Include Routers
app.include_router(problems.router, prefix="/api") # Keeping /api prefix for compatibility

@app.get("/")
def read_root():
    return {"message": f"{settings.PROJECT_NAME} is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
