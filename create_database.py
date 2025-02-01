import sqlite3

con = sqlite3.connect("posts.db")
cur = con.cursor()

with open('./sql_scripts/create_database.sql', mode = 'r') as sql_script:
    cur.executescript(str(sql_script.read()))

con.commit()
