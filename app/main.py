from fastapi import FastAPI
from app.routers.api_router import router
from app.exceptions.custom_exceptions import custom_validation_exception_handler
from app.exceptions import CustomValidationException
from app.db import init

app = FastAPI()
app.add_exception_handler(CustomValidationException, custom_validation_exception_handler)
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await init()
