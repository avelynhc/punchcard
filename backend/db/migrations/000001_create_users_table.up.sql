CREATE TABLE IF NOT EXISTS "users" (
    "id"       SERIAL PRIMARY KEY,
    "username" VARCHAR NOT NULL,
    "password" VARCHAR NOT NULL
);
