#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cassandra.cluster import Cluster

class DBdriver:
    def __init__(self, dbname):
        self.dbname = dbname
        cluster = Cluster()
        self.session = cluster.connect(dbname)
            
    def create_index(self, field):
        self.db.profiles.create_index([(field, pymongo.ASCENDING)], unique=True)

    def add_record(self, name):
        return self.session.execute(f'INSERT INTO anime (name) VALUES ({name}))

    def find_record(self, name):
        return self.session.execute(f'SELECT name FROM anime WHERE name={name}')
        