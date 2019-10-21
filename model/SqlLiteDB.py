#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
from src.config import DB_FILE_PATH

class sqliteDriver:
    def __init__(self):
        self.dbname = DB_FILE_PATH
        '''
        if not os.path.exists(db_path):
            create_tables(dbname)
            create_index(dbname)
        '''

    def create_tables(self):
        db=sqlite3.connect(self.dbname)
        cur = db.cursor()
        cur.execute('CREATE TABLE "anime" ("id" INTEGER PRIMARY KEY AUTOINCREMENT,"name"	TEXT NOT NULL, "episode" INTEGER NOT NULL);')
        #db.execute('CREATE TABLE "episodes" ("id" INTEGER PRIMARY KEY AUTOINCREMENT,"episode" INTEGER NOT NULL,"anime" TEXT NOT NULL,FOREIGN KEY("anime") REFERENCES "anime"("name"));')
        db.close()

    def create_index(self):
        db=sqlite3.connect(self.dbname)
        cur = db.cursor()
        cur.execute('CREATE INDEX "anime_index" ON "anime" ("name" ASC);')
        db.close()

    def find_record(self, episode):
        db=sqlite3.connect(self.dbname)
        cur = db.cursor()
        cur.execute(f'SELECT DISTINCT name FROM anime WHERE name = "{episode.name}" AND episode = {episode.number};')
        result = cur.fetchone()
        db.close()
        return result

    def add_record(self, episode):
        db=sqlite3.connect(self.dbname)
        cur = db.cursor()
        cur.execute(f'INSERT INTO "anime" (name, episode) VALUES ({episode.name}, {episode.number});')
        db.close()

    def remove_record(self, episode):
        db=sqlite3.connect(self.dbname)
        cur = db.cursor()
        cur.execute(f'DELETE FROM "anime" WHERE name = "{episode.name}" AND episode = {episode.number};')
        db.close()

    def get_animeList(self):
        db=sqlite3.connect(self.dbname)
        cur = db.cursor()
        cur.execute(f'SELECT DISTINCT name FROM anime;')
        result = cur.fetchall()
        db.close()
        return result
