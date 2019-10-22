import os
file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
db_path = os.path.join(folder_path, "database.db")

import sqlite3
conn = sqlite3.connect(db_path)
conn.isolation_level = None # autocommit
cursor = conn.cursor()

def _create_insert_query(table, columns):
    structure = "INSERT INTO {} ({}) VALUES ({})"
    column_names = ", ".join(columns)
    value_slots = ("?, " * len(columns))[:-2]
    return structure.format(table, column_names, value_slots)

def add_post(data):
    columns = ["title", "ieddit_id", "reddit_id", "ieddit_url", "reddit_url", "subieddit", "subreddit", "image_url", "timestamp"]
    query = _create_insert_query("posts", columns)

    if len(data) != len(columns):
        raise Exception("number of columns and number of provided values does not match up.")
    
    cursor.execute(query, data)

def submission_reposted(subieddit, reddit_id):
    query = "SELECT * FROM posts WHERE subieddit = ? AND reddit_id = ?"
    params = (subieddit, reddit_id)
    cursor.execute(query, params)
    return cursor.fetchone() is not None

def table_exists(name):
    query = "SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = ?"
    params = (name,)
    cursor.execute(query, params)
    return cursor.fetchone()[0] > 0

def init():

    if not table_exists("posts"):
        cursor.execute("""
            CREATE TABLE "posts" (
                "id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                "title"         TEXT,
                "ieddit_id"	    INTEGER UNIQUE,
                "reddit_id"	    TEXT,
                "ieddit_url"	TEXT,
                "reddit_url"	TEXT,
                "subieddit"	    TEXT,
                "subreddit"	    TEXT,
                "image_url"     TEXT,
                "timestamp"	INTEGER
            );""")