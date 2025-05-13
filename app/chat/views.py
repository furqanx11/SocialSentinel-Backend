from datetime import datetime
from fastapi import WebSocket
from .db import (
    create_chat_message as db_create_chat_message,
    get_chat_message_by_id as db_get_chat_message_by_id,
    get_chat_messages_between_users as db_get_chat_messages_between_users,
    update_chat_message as db_update_chat_message,
    delete_chat_message as db_delete_chat_message
)
from .model import ChatMessageCreate, ChatMessageUpdate

connected_clients = {}

async def connect_client(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connected_clients[user_id] = websocket

async def disconnect_client(user_id: str):
    if user_id in connected_clients:
        await connected_clients[user_id].close()
        del connected_clients[user_id]

async def send_message_to_user(user_id: str, message: dict):
    if user_id in connected_clients:
        serialized_message = {
            key: (value.isoformat() if isinstance(value, datetime) else value)
            for key, value in message.items()
        }
        await connected_clients[user_id].send_json(serialized_message)

async def create_chat_message(chat_message: ChatMessageCreate):
    message_id = await db_create_chat_message(chat_message)
    message = {**chat_message.dict(), "id": message_id}
    await send_message_to_user(chat_message.receiver_id, message)
    return message_id

async def get_chat_message_by_id(chat_message_id: str):
    return await db_get_chat_message_by_id(chat_message_id)

async def get_chat_messages_between_users(sender_id: str, receiver_id: str):
    return await db_get_chat_messages_between_users(sender_id, receiver_id)

async def update_chat_message(chat_message_id: str, chat_message_data: ChatMessageUpdate):
    await db_update_chat_message(chat_message_id, chat_message_data)

async def delete_chat_message(chat_message_id: str):
    await db_delete_chat_message(chat_message_id)