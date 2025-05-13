from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import json


def success_response(msg, data=None):
    # If it's a Pydantic model, use model_dump_json and parse back to dict
    if isinstance(data, BaseModel):
        data = json.loads(data.model_dump_json())
    # If it's a list of Pydantic models
    elif isinstance(data, list) and all(isinstance(item, BaseModel) for item in data):
        data = [json.loads(item.model_dump_json()) for item in data]
    # Fallback datetime handling
    elif isinstance(data, dict):
        def datetime_encoder(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError("Type not serializable")
        data = json.loads(json.dumps(data, default=datetime_encoder))

    response_content = {
        "message": msg,
        "data": data,
        "status_code": 200,
    }
    return JSONResponse(content=response_content, status_code=200)


def not_found_response(msg):
    response_content = {"error": "", "message": msg, "status_code": 404}
    return JSONResponse(content=response_content, status_code=404)


def bad_request_response(msg):
    response_content = {"error": "", "message": msg, "status_code": 400}
    return JSONResponse(content=response_content, status_code=400)


def unauthorized_response(msg):
    response_content = {"error": "", "message": msg, "status_code": 401}
    return JSONResponse(content=response_content, status_code=401)


def validator_response(msg):
    response_content = {"error": None, "message": msg, "status_code": 400}
    return JSONResponse(content=response_content, status_code=400)


def error_response(exception=None):
    response_content = {
        "error": repr(exception) if exception else "",
        "message": "",
        "status_code": 500,
    }
    return JSONResponse(content=response_content, status_code=500)


async def emit_response(sio, event_name: str, message: str):
    await sio.emit(event_name, {"message": message})
