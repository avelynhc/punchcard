from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# CREATE TABLE users (
#    id SERIAL PRIMARY KEY,
#    provider_id TEXT UNIQUE NOT NULL
# );

# CREATE TABLE task_details (
#     id SERIAL PRIMARY KEY,
#     user_id TEXT UNIQUE NOT NULL,
#     start_time BIGINT NOT NULL,
#     finish_time BIGINT,
#     FOREIGN KEY (user_id)
#         REFERENCES users (id)
# );

