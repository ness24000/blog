# script intended to be used by make command
# create_database. Otherwise, the paths get a bit messy.

import sqlite3

con = sqlite3.connect("./posts.db")
cur = con.cursor()

with open("./scripts/create_database.sql", mode="r") as sql_script:
    cur.executescript(str(sql_script.read()))

con.commit()
