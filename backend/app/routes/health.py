from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple status response for local checks."""
    return {"status": "ok", "message": "API is running"}
