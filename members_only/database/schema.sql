CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY,
    username        TEXT UNIQUE NOT NULL,
    password        TEXT NOT NULL
);
