import os

from flask import Flask

from db.migrations.create_table import db
from models.task_detail import ItemModel
from models.user import UserModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    default="postgresql://punchcard:password@punchcard-db:5432/punchcard",
)

@app.before_first_request
def create_table():
    db.create_all()

@app.route("/ping", methods=["GET"])
def ping_pong():
    return "pong"

if __name__ == "__main__":
    db.init_app(app)
    app.run(
        debug=os.environ.get("DEBUG", default="true") == "true",
        host="0.0.0.0",
        port=os.environ.get("PORT", default=4000),
    )
