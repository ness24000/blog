import sqlite3

con = sqlite3.connect("../posts.db")
cur = con.cursor()

with open('./new_post.txt', mode = 'r') as new_post:
    content_third_article = new_post.read()

    
fake_posts = [
    (1, 'first_test_title','2015-01-01','The content of the article 1'),
    (2, 'second_test_title','2015-01-01','The content of the article 2'),
    (3, 'third_test_title', '2015-01-01', content_third_article)]



cur.executemany("INSERT INTO posts VALUES (?,?,?,?)",fake_posts)
con.commit()
