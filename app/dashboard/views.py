from .db import dashboard_count, detected_content_over_weeks, warnings_count
from app.utils.responses import success_response, error_response, not_found_response


async def get_dashboard_counts():
    try:
        counts = await dashboard_count()
        if not counts:
            return not_found_response(msg="Dashboard counts not found")
        return success_response("Dashboard counts fetched successfully", data=counts)
    except Exception as e:
        return error_response(str(e))

async def get_warnings_count():
    try:
        counts = await warnings_count()
        if not counts:
            return not_found_response(msg="Warnings count not found")
        return success_response("Warnings count fetched successfully", data=counts)
    except Exception as e:
        return error_response(str(e))

async def get_detected_content_over_weeks():
    try:
        counts = await detected_content_over_weeks()
        if not counts:
            return not_found_response(msg="Detected content over weeks not found")
        return success_response("Detected content over weeks fetched successfully", data=counts)
    except Exception as e:
        return error_response(str(e))