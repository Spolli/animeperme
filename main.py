#!/usr/bin/env python
# -*- coding: utf-8 -*-

from anime_enforce import Enforcer
import requests
'''
import DBdriver
from telegram.ext import Updater, CommandHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
dbname = 'animeperme'
db = DBdriver(dbname)
'''
folder_path={
    'video': './src/video'
}

bot_token = '717436297:AAFK04merXzwjdWlAJg75fz8dmUt-cnuViI'

def send_video_telegram(bot, update, name, filename):
    #bot.send_chat_action(chat_id=update.message.chat.id, action=telegram.ChatAction.UPLOAD_VIDEO)
    bot.send_video(
        chat_id=update.message.chat.id, 
        video=open(filename, 'rb'),
        caption=f'{name} #',
        supports_streaming=True
        )

def download_video(bot, update, episode):
    url = episode.download_link()
    name = '-'.join(anime.name.split(' '))
    chunk_size = 256
    r = requests.get(url, stream=True)
    filename = f'{folder_path["video"]}/{name}.mp4'
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
        send_video_telegram(bot, update, episode.name, filename)

def start():
    enforcer = Enforcer()
    anime_list = enforcer.last_episode_list()
    for anime in anime_list:
        last_episode = anime._get_last_episode()
        print(anime.episode)
        #download_video(bot, update, last_episode)

def main():
    updater = Updater(bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    updater.start_webhook(listen='127.0.0.1', port=5002, url_path=bot_token)
    updater.idle()

if __name__ == '__main__':    
    start()
    #main()
    

