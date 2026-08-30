from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analysis import router as analysis_router
from app.routes.career_guidance import router as career_guidance_router
from app.routes.health import router as health_router
from app.routes.history import router as history_router

app = FastAPI(title="AI Resume & Job Matcher API")

# Vite's local development server runs on port 5173 by default.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to the AI Resume & Job Matcher API"}


app.include_router(health_router)
app.include_router(analysis_router)
app.include_router(career_guidance_router)
app.include_router(history_router)
