from fastapi import APIRouter, Depends
from app.post.model import PostFull
from .db import dashboard_count, detected_content_over_weeks, warnings_count
from app.post.db import get_posts_for_user
from app.auth.db import get_detected_words_for_user, get_all_detected_words
from app.middleware.dependecy import get_current_user
from app.utils.responses import success_response, error_response, not_found_response

dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@dashboard_router.get("/posts/{user_id}", response_model=list[PostFull])
async def get_all_posts(user_id:str):
    try:
        posts = await get_posts_for_user(user_id)
        if not posts:
            return not_found_response(msg="Posts not found")
        return success_response("Posts fetched successfully", data=posts)
    except Exception as e:
        return error_response(str(e))

@dashboard_router.get("/detected_words", response_model=list[str])
async def get_detected_words(user_id:str = Depends(get_current_user)):
    try:
        words = await get_detected_words_for_user(user_id)
        if not words:
            return not_found_response(msg="No detected words found")
        return success_response("Detected words fetched successfully", data=words)
    except Exception as e:
        return error_response(str(e))

@dashboard_router.get("/detected_words/all", response_model=list[str])
async def get_detected_words():
    try:
        words = await get_all_detected_words()
        if not words:
            return not_found_response(msg="No detected words found")
        return success_response("All detected words fetched successfully", data=words)
    except Exception as e:
        return error_response(str(e))


@dashboard_router.get("/counts", response_model=dict)
async def get_dashboard_counts():
    try:
        counts = await dashboard_count()
        if not counts:
            return not_found_response(msg="Dashboard counts not found")
        return success_response("Dashboard counts fetched successfully", data=counts)
    except Exception as e:
        return error_response(str(e))

@dashboard_router.get("/warnings_count", response_model=dict)
async def get_warnings_count():
    try:
        counts = await warnings_count()
        if not counts:
            return not_found_response(msg="Warnings count not found")
        return success_response("Warnings count fetched successfully", data=counts)
    except Exception as e:
        return error_response(str(e))

@dashboard_router.get("/detected_content_over_weeks", response_model=list[dict])
async def get_detected_content_over_weeks():
    try:
        counts = await detected_content_over_weeks()
        if not counts:
            return not_found_response(msg="Detected content over weeks not found")
        return success_response("Detected content over weeks fetched successfully", data=counts)
    except Exception as e:
        return error_response(str(e))