#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.model.animeforce import Enforcer
from src.model.SqlLiteDB import sqliteDriver
from src.config import TOKEN_API, TIME_INTERVAL
import requests
from telegram.ext import Updater, CommandHandler
import logging
import time
import os
from progress.bar import Bar

folder_path = {
    'video': './src/video'
}
db = sqliteDriver()


def delete_file(filename):
    try:
        if os.path.isfile(filename):
            os.unlink(filename)
    except Exception as e:
        print(e)


def send_video_telegram(context, update, episode, filename):
    print('Sending video to Telegram...')
    context.bot.send_video(
        chat_id=update.message.chat.id,
        video=open(filename, 'rb'),
        caption=f'#{episode.name} | Episode: {episode.number}',
        timeout=30000,
        supports_streaming=True
    )


def download_video(context, update, episode):
    if not episode.link is None:
        url = episode.download_link()
        name = '-'.join(episode.name.split(' '))
        filename = f'{folder_path["video"]}/{name}.mp4'
        if not os.path.isfile(filename):
            chunk_size = 512
            r = requests.get(url, stream=True)
            file_len = int(requests.head(
                url).headers['content-length']) / chunk_size
            with open(filename, "wb") as f:
                prog_bar = Bar(
                    f'\t\tDownloading: {episode.name}\t\t', max=file_len)
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    prog_bar.next()
                prog_bar.finish()
        send_video_telegram(context, update, episode, filename)
        db.add_record(episode)
        delete_file(filename)


def start(update, context):
    print('Start main')
    enforcer = Enforcer()
    while True:
        anime_list = enforcer.last_episode_list()
        for anime in anime_list:
            if anime.episode < 30:
                last_episode = anime._get_last_episode()
                if db.find_record(last_episode) is None:
                    download_video(context, update, last_episode)
        time.sleep(TIME_INTERVAL)


def animelist(update, context):
    rows = db.get_animeList()
    msg = 'Anime List: \n'
    print(rows)
    if rows:
        for r in rows:
            msg += f'#{r}\n'
    else:
        msg = 'Nessun anime trovato'
    update.message.reply_text(msg)


def main():
    updater = Updater(token=TOKEN_API, use_context=True, request_kwargs={
        'read_timeout': 50, 'connect_timeout': 50})
    print('Starting telegram bot...')
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    dp.add_handler(CommandHandler("start", start, pass_args=False))
    dp.add_handler(CommandHandler("animelist", animelist, pass_args=False))
    # Start the Bot
    updater.start_polling()
    print('Telegram bot start')
    # updater.start_webhook(listen='127.0.0.1', port=5002, url_path=TOKEN_API)
    updater.idle()


if __name__ == '__main__':
    start(None, None)
    # main()
