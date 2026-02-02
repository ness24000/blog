import sqlite3

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
