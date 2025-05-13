from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from .views import (
    connect_client,
    disconnect_client,
    create_chat_message,
    get_chat_message_by_id,
    get_chat_messages_between_users,
    update_chat_message,
    delete_chat_message
)
from .model import ChatMessageCreate, ChatMessageUpdate, ChatMessageFull
from app.middleware.dependecy import get_current_user

chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await connect_client(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            chat_message = ChatMessageCreate(**data)
            await create_chat_message(chat_message)
    except WebSocketDisconnect:
        await disconnect_client(user_id)

@chat_router.post("/messages", response_model=str)
async def create_chat_message_endpoint(chat_message: ChatMessageCreate):
    return await create_chat_message(chat_message)

@chat_router.get("/messages/{chat_message_id}", response_model=ChatMessageFull)
async def get_chat_message_by_id_endpoint(chat_message_id: str):
    chat_message = await get_chat_message_by_id(chat_message_id)
    if not chat_message:
        raise HTTPException(status_code=404, detail="Chat message not found")
    return chat_message

@chat_router.get("/messages/{sender_id}/{receiver_id}", response_model=list[ChatMessageFull])
async def get_chat_messages_between_users_endpoint(sender_id: str, receiver_id: str):
    return await get_chat_messages_between_users(sender_id, receiver_id)

@chat_router.put("/messages/{chat_message_id}", response_model=None)
async def update_chat_message_endpoint(chat_message_id: str, chat_message_data: ChatMessageUpdate):
    await update_chat_message(chat_message_id, chat_message_data)

@chat_router.delete("/messages/{chat_message_id}", response_model=None)
async def delete_chat_message_endpoint(chat_message_id: str):
    await delete_chat_message(chat_message_id)