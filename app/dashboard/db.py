from app.db.db import db
from datetime import datetime, timedelta

users_collection = db['users']
detected_words_collection = db['detected_words']

async def dashboard_count():
    try:
        total_reported_count = await detected_words_collection.count_documents({})
        total_users_count = await users_collection.count_documents({})
        total_banned_count = await users_collection.count_documents({"is_banned": True})
        return {
            "total_reported_count": total_reported_count,
            "total_users_count": total_users_count,
            "total_banned_count": total_banned_count
        }
    except Exception as e:
        raise ValueError(f"Error counting dashboard data: {str(e)}")

async def warnings_count():
    try:
        zero_warnings = await users_collection.count_documents({"warnings": 0})
        one_warning = await users_collection.count_documents({"warnings": 1})
        two_warnings = await users_collection.count_documents({"warnings": 2})
        more_than_two_warnings = await users_collection.count_documents({"warnings": {"$gt": 2}})
        return {
            "zero_warnings": zero_warnings,
            "one_warning": one_warning,
            "two_warnings": two_warnings,
            "more_than_two_warnings": more_than_two_warnings
        }
    except Exception as e:
        raise ValueError(f"Error counting warnings data: {str(e)}")
    
async def detected_content_over_weeks():
    try:
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "$isoWeek": {
                            "$ifNull": ["$detected_at", None]
                        }
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id": 1}
            },
            {
                "$project": {
                    "week": "$_id",
                    "count": 1,
                    "_id": 0
                }
            }
        ]
        result = await detected_words_collection.aggregate(pipeline).to_list(length=None)
        return result
    except Exception as e:
        raise ValueError(f"Error fetching detected content over weeks: {str(e)}")