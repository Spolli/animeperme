#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.animeforce import Enforcer
import requests
from model.SqlLiteDB import sqliteDriver
from telegram.ext import Updater, CommandHandler
import logging
import time
from src.config import TOKEN_API
import urllib.request

folder_path={
    'video': './src/video'
}
db = sqliteDriver()

def delete_file(filename):
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

def send_video_telegram(context, update, episode, filename):
    context.bot.send_video(
        chat_id=update.message.chat.id, 
        video=open(filename, 'rb'),
        caption=f'#{episode.name} | Episode: {episode.number}'
        #supports_streaming=True
    )

def downloadVideo(context, update, episode):
    if not episode.link is None:
        url = episode.download_link()
        name = '-'.join(episode.name.split(' '))
        filename = f'{folder_path["video"]}/{name}.mp4'
        print(url)
        urllib.request.urlretrieve(url, filename)
        send_video_telegram(context, update, episode, filename)
        db.add_record(episode)
        delete_file(filename)

def download_video(context, update, episode):
    print(episode.link)
    if not episode.link is None:
        url = episode.download_link()
        name = '-'.join(episode.name.split(' '))
        filename = f'{folder_path["video"]}/{name}.mp4'
        chunk_size = 256
        r = requests.get(url, stream=True)
        
        with open(filename, "wb") as f:
            print('Downloading Video...')
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
            print('Sending video to Telegram...')
            send_video_telegram(context, update, episode, filename)
            db.add_record(episode)
            delete_file(filename)

def start(update, context):
    enforcer = Enforcer()
    while True:
        anime_list = enforcer.last_episode_list()
        for anime in anime_list:
            if anime.episode < 30:
                last_episode = anime._get_last_episode()
                if db.find_record(last_episode) is None:
                    download_video(context, update, last_episode)
        time.sleep(3600)
        

def animelist(update, context):
    rows = db.get_animeList()
    msg = 'Anime List: \n'
    print(rows)
    if not len(rows) == 0:
        for r in rows:
            msg += f'#{r}\n'
        update.message.reply_text(msg)
    else:
        update.message.reply_text('Nessun anime trovato')

def main():
    updater = Updater(token=TOKEN_API, use_context=True)
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    dp.add_handler(CommandHandler("start", start, pass_args=False))
    dp.add_handler(CommandHandler("animelist", animelist, pass_args=False))
    # Start the Bot
    updater.start_polling()
    #updater.start_webhook(listen='127.0.0.1', port=5002, url_path=TOKEN_API)
    updater.idle()

if __name__ == '__main__':
    main()
    

