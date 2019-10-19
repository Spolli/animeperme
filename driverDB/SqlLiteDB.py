import sqlite3

def create_tables(dbname):
    db=sqlite3.connect(dbname)
    db.execute("CREATE TABLE log (slot INT PRIMARY KEY, data TEXT)")
    db.execute("CREATE TABLE metadata (metakey TEXT, metavalue INT)")
    db.execute("INSERT INTO metadata VALUES('nextslot',0)")
    db.commit()
    db.close()

def appendlogmessage(db, msg):
    'Add a message to the log in the next slot.'
    # get next slot
    cur = db.cursor()
    cur.execute("SELECT metavalue FROM metadata WHERE metakey='nextslot'")
    nextslot = cur.fetchone()[0]
    # add the message at that slot location
    return addlogmessage(db, nextslot, msg)