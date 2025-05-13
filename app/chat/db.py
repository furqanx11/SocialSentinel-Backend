from app.db.db import db
from bson import ObjectId
from .model import ChatMessageCreate, ChatMessageUpdate, ChatMessageFull

chat_messages_collection = db['chat_messages']

async def create_chat_message(chat_message: ChatMessageCreate):
    chat_message_dict = chat_message.dict()
    result = await chat_messages_collection.insert_one(chat_message_dict)
    return str(result.inserted_id)

async def get_chat_message_by_id(chat_message_id: str):
    chat_message = await chat_messages_collection.find_one({"_id": ObjectId(chat_message_id)})
    if chat_message:
        chat_message['id'] = str(chat_message['_id'])
        return ChatMessageFull(**chat_message)

async def get_chat_messages_between_users(sender_id: str, receiver_id: str):
    chat_messages = []
    async for chat_message in chat_messages_collection.find({
        "$or": [
            {"sender_id": sender_id, "receiver_id": receiver_id},
            {"sender_id": receiver_id, "receiver_id": sender_id}
        ]
    }):
        chat_message['id'] = str(chat_message['_id'])
        chat_messages.append(ChatMessageFull(**chat_message))
    return chat_messages

async def update_chat_message(chat_message_id: str, chat_message_data: ChatMessageUpdate):
    await chat_messages_collection.update_one(
        {"_id": ObjectId(chat_message_id)},
        {"$set": chat_message_data.dict(exclude_unset=True)}
    )

async def delete_chat_message(chat_message_id: str):
    await chat_messages_collection.delete_one({"_id": ObjectId(chat_message_id)})