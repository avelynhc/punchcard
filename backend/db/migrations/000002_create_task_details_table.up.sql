CREATE TABLE IF NOT EXISTS "task_details" (
    "id"          SERIAL PRIMARY KEY,
    "task_name"   VARCHAR NOT NULL,
    "start_time"  BIGINT  NOT NULL,
    "finish_time" BIGINT,
    "user_id"     SERIAL  NOT NULL,
    CONSTRAINT task_details_user_id FOREIGN KEY (user_id) REFERENCES "users" (id)
);
