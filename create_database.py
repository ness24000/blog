import sqlite3

con = sqlite3.connect("posts.db")
cur = con.cursor()

with open('./sql_scripts/create_database.sql', mode = 'r') as sql_script:
    cur.executescript(str(sql_script.read()))

fake_posts = [
    (1, 'first_test_title','2015-01-01','The content of the article 1'),
    (2, 'second_test_title','2015-01-01','The content of the article 2'),
]

cur.executemany("INSERT INTO posts VALUES (?,?,?,?)",fake_posts)
con.commit()
