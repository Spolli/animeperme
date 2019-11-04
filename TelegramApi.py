#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telethon import TelegramClient
import os
from progress.bar import Bar
from src.config import API_ID, API_HASH, SESSION_NAME, TOKEN_API

bot = TelegramClient(SESSION_NAME, API_ID, API_HASH).start(bot_token=TOKEN_API)

#client.send_message('spolli', 'Hello! Talking to you from Telethon')


async def main():
    file_size = os.path.getsize('./src/video/Kandagawa-Jet-Girls.mp4') / 512
    prog_bar = Bar('\t\tUploading: File\t\t', max=file_size)
    file_id = await bot.send_file(
        entity='spolli',
        file=open('./src/video/Kandagawa-Jet-Girls.mp4', 'rb'),
        caption='Sample',
        supports_streaming=True,
        part_size_kb=512,
        progress_callback=prog_bar.next()
    )
    prog_bar.finish()
    print('Finish Uploading...')
    print(file_id.stringify())


async def main2():
    print('Start Uploading...')
    file_id = await bot.upload_file(
        file=open('./src/video/Kandagawa-Jet-Girls.mp4', 'rb'),

        file_name='sample'
    )
    print('Finish Uploading...')
    print(file_id.stringify())

with bot:
    bot.loop.run_until_complete(main())
