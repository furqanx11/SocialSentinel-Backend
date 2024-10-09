from fastapi import APIRouter
from app.routers import users, posts, detections
router = APIRouter()

router.include_router(users.router, prefix="/user", tags=["user"])
router.include_router(posts.router, prefix="/post", tags=["user"])
router.include_router(detections.router, prefix="/flagged-content", tags=["user"])