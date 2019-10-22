import os
file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
db_path = os.path.join(folder_path, "database.db")

import sqlite3
conn = sqlite3.connect(db_path)
conn.isolation_level = None # autocommit
cursor = conn.cursor()

def table_exists(name):
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = ?", (name,))
    return cursor.fetchone()[0] > 0


def init():

    if not table_exists("posts"):
        cursor.execute("""
            CREATE TABLE "posts" (
                "id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                "ieddit_id"	INTEGER UNIQUE,
                "reddit_id"	TEXT UNIQUE,
                "ieddit_url"	TEXT,
                "reddit_url"	TEXT,
                "ieddit_sub"	TEXT,
                "reddit_sub"	TEXT,
                "timestamp"	INTEGER
            );""")