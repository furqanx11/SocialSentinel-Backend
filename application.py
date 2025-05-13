from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import user_router
from app.comments.routes import comment_router
from app.post.routes import post_router
from app.chat.routes import chat_router
from app.dashboard.routes import dashboard_router
from pydantic import BaseModel
from script import detect_abuse
from app.middleware.dependecy import get_current_user

app = FastAPI(__name__="SocialSentinel")

class TextInput(BaseModel):
    text: str


@app.post("/detect")
async def detect(input_data: TextInput, update: bool = Query(False), user_id: str = Depends(get_current_user)):  
    print(update,"update")
    result, reason, score = await detect_abuse(input_data.text, user_id, update=update)
    return {"flagged": result, "reason": reason, "score": score}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return "Hello World!"


app.include_router(router=user_router)
app.include_router(router=comment_router)
app.include_router(router=post_router)
app.include_router(router=chat_router)
app.include_router(router=dashboard_router)
