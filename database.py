import sqlite3

def get_db():
    conn = sqlite3.connect("rgx_esports.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS players (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT
    );

    CREATE TABLE IF NOT EXISTS tournaments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        game TEXT NOT NULL,
        mode TEXT NOT NULL,
        max_players INTEGER NOT NULL,
        status TEXT DEFAULT 'OPEN'
    );

    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tournament_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        team_name TEXT,
        UNIQUE(tournament_id, user_id),
        FOREIGN KEY(tournament_id) REFERENCES tournaments(id),
        FOREIGN KEY(user_id) REFERENCES players(user_id)
    );

    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tournament_id INTEGER NOT NULL,
        match_title TEXT NOT NULL,
        status TEXT DEFAULT 'PENDING',
        FOREIGN KEY(tournament_id) REFERENCES tournaments(id)
    );

    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER NOT NULL,
        winner_user_id INTEGER,
        score TEXT,
        verified INTEGER DEFAULT 0,
        FOREIGN KEY(match_id) REFERENCES matches(id)
    );
    """)
    conn.commit()
    conn.close()
    print("RGX ESPORTS DATABASE READY")

if __name__ == "__main__":
    init_db()
