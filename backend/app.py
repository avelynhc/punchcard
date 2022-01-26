import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db.migrations.create_table import db
from models.task_detail import ItemModel
from resources.user import UserRegister, UserLogin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    default="postgresql://punchcard:password@localhost:55432/punchcard",
)
app.secret_key = "avelyn"
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route("/ping", methods=["GET"])
def ping_pong():
    return "pong"

api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    db.init_app(app)
    app.run(
        debug=os.environ.get("DEBUG", default="true") == "true",
        host="0.0.0.0",
        port=os.environ.get("PORT", default=4000),
    )
