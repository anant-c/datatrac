from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .routers import datasets

app = FastAPI(
    title="DataTrac API",
    description="An API for discovering, managing, and tracing data files.",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Include dataset router
app.include_router(datasets.router)

# Path to your React build
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "web")

# Mount static files
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

# Serve index.html at root and catch-all
@app.get("/")
async def serve_root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """
    Catch-all route to serve React's index.html
    so React Router works with client-side routes.
    """
    index_file = os.path.join(frontend_path, "index.html")
    return FileResponse(index_file)
