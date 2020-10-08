CREATE DATABASE sparkledb;
CREATE USER sparkle WITH ENCRYPTED PASSWORD 'foobar';
GRANT ALL PRIVILEGES ON DATABASE sparkledb TO sparkle;

\c sparkledb

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    passwd VARCHAR(256)
);

INSERT INTO users (name, passwd) VALUES ('user1', 'passwd1');

GRANT ALL PRIVILEGES ON TABLE users TO sparkle;
