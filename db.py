import sqlite3
con = sqlite3.connect('/home/pi/ams/music.db')
cur = con.cursor()

def init_table():
    cur.execute('''CREATE TABLE tracks(
                    album           TEXT    NOT NULL,
                    artist            TEXT     NOT NULL,
                    title        TEXT  NOT NULL,
                    hashstr     TEXT PRIMARY KEY NOT NULL
                    );''')
    con.commit()

def drop_table():
    cur.execute("DROP TABLE tracks")
    con.commit()

def insert_track(album, artist, title, hashstr):

    cur.execute("SELECT * FROM tracks WHERE hashstr = ?", (hashstr,))
    data=cur.fetchall()
    if len(data) == 0:
        cur.execute("insert into tracks values (?, ?, ?, ?)", (album, artist, title, hashstr))
        con.commit()


def delete_all_tracks():
    cur.execute("DELETE FROM tracks")
    con.commit()

def get_tracks():
    cur.execute("select * from tracks")
    return cur.fetchall()

print(get_tracks())