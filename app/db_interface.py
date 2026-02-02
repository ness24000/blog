import sqlite3
from app.utils import get_date

def add_post_to_db(
    title: str,
    date: str,
    preview_md: str,
    content_md: str,
    preview_html: str,
    content_html: str,
    path_to_db: str,
):

    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    cur.execute(
        "INSERT INTO posts(title, date, preview_md, content_md, preview_html, content_html) VALUES (?,?,?,?,?,?)",
        (title, date, preview_md, content_md, preview_html, content_html),
    )
    con.commit()


def update_post_in_db(
    post_id: int,
    title: str,
    preview_md: str,
    content_md: str,
    preview_html: str,
    content_html: str,
    path_to_db: str,
):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    cur.execute(
        "UPDATE posts SET (title, preview_md, content_md, preview_html, content_html) = (?,?,?,?,?) where id = ?",
        (title, preview_md, content_md, preview_html, content_html, post_id),
    )

    con.commit()


def delete_post_in_db(post_id: int, path_to_db: str):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    cur.execute("delete from posts where id = ?;", (post_id,))

    con.commit()


def add_email_to_db(email: str, path_to_db: str):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    date = get_date()
    confirmed = False

    cur.execute(
        "INSERT INTO email(date, email_address, confirmed) VALUES (?,?,?)",
        (date, email, confirmed),
    )
    con.commit()


def check_email_exists_in_db(email_address: str, path_to_db: str):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    rows_with_email_count = cur.execute(
        "select id from email where email_address=?;", (email_address,)
    ).fetchall()

    if len(rows_with_email_count) > 0:
        return True
    return False


def email_confirmation_in_db(email_address: str, path_to_db: str):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    cur.execute(
        "UPDATE email SET (confirmed) = (?) where email_address = ?",
        (True, email_address),
    )

    con.commit()


def remove_email_from_db(email_address: str, path_to_db: str):

    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    cur.execute("DELETE FROM email WHERE email_address=?;", (email_address,))
    con.commit()


def get_confirmed_emails_in_db(path_to_db: str):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    confirmed_email_addresses = cur.execute(
        "SELECT email_address FROM email WHERE confirmed=1;"
    ).fetchall()

    list_confirmed_email_addresses = [row[0] for row in confirmed_email_addresses]

    return list_confirmed_email_addresses
