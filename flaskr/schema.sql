-- DROP TABLE IF EXISTS users;

-- CREATE TABLE users (
--   username TEXT PRIMARY KEY NOT NULL,
--   password TEXT NOT NULL,
-- );

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS person_chat;

CREATE TABLE user (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT PRIMARY KEY NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE person_chat (
    recipient1 TEXT NOT NULL,
    recipient2 TEXT NOT NULL,
    chat_file TEXT NOT NULL,
    PRIMARY KEY(recipient1, recipient2)
);