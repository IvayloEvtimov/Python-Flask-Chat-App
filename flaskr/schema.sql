-- DROP TABLE IF EXISTS users;

-- CREATE TABLE users (
--   username TEXT PRIMARY KEY NOT NULL,
--   password TEXT NOT NULL,
-- );

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS person_chat;
DROP TABLE IF EXISTS group_chat;
DROP TABLE IF EXISTS group_participants;

CREATE TABLE user (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT PRIMARY KEY NOT NULL,
    avatar TEXT,
    password TEXT NOT NULL
);

CREATE TABLE person_chat (
    recipient1 TEXT NOT NULL,
    recipient2 TEXT NOT NULL,
    chat_file TEXT NOT NULL,
    PRIMARY KEY(recipient1, recipient2)
);

-- CREATE TABLE group_chat (
--     chat_file TEXT PRIMARY KEY NOT NULL,
--     group_name TEXT NOT NULL
-- );

-- CREATE TABLE group_participants (
--     user TEXT NOT NULL,
--     group_chat TEXT NOT NULL,
--     FOREIGN KEY(user) REFERENCES user(username),
--     FOREIGN KEY(group_chat) REFERENCES group_chat(chat_file),
--     PRIMARY KEY(user, group_chat)
-- );