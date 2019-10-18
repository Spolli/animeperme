#!/usr/bin/env python
# -*- coding: utf-8 -*-

from anime_enforce import Enforcer
import requests
import DBdriver

folder_path={
    'video': './src/video'
}
dbname = 'animeperme'
db = DBdriver(dbname)

def download_video(url, file_name):
    chunk_size = 256
    r = requests.get(url, stream=True)
    with open(f'{folder_path["video"]}/{file_name}.mp4', "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)

def main():
    enforcer = Enforcer()
    anime_list = enforcer.last_episode_list()
    for anime in anime_list:
        last_episode = anime._get_last_episode()
        download_video(last_episode.download_link(), '-'.join(anime.name.split(' ')))

if __name__ == '__main__':    
    main()
    

