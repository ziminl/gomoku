CREATE TABLE IF NOT EXISTS wins
(id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
win_count INTEGER)