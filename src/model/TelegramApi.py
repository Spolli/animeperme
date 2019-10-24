#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telethon.sync import TelegramClient
from src.config import API_ID, API_HASH, SESSION_NAME, TOKEN_API

bot = TelegramClient(SESSION_NAME, API_ID, API_HASH).start(bot_token=TOKEN_API)

#client.send_message('spolli', 'Hello! Talking to you from Telethon')

async def main():
    print('Start Uploading...')
    file_id = await bot.send_file(
        entity='spolli', 
        file=open('./src/video/BokutachiWaBenkyouGaDekinai.mp4', 'rb'), 
        caption='Sample', 
        supports_streaming=True
    )
    print('Finish Uploading...')
    print(file_id.stringify())

async def main2():
    print('Start Uploading...')
    file_id = await bot.upload_file(
        file=open('./src/video/BokutachiWaBenkyouGaDekinai.mp4', 'rb'),
        part_size_kb=512,
        file_name='sample'
    )
    print('Finish Uploading...')
    print(file_id.stringify())

with bot:
    bot.loop.run_until_complete(main2())
