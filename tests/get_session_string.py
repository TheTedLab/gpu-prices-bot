from telethon.sync import TelegramClient
from telethon.sessions import StringSession


api_id = input("Enter your api_id: ")
api_hash = input("Enter your api_hash: ")
with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("Your session string is:", client.session.save())
