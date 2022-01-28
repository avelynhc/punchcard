import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from db.migrations.create_table import db
from models.task_detail import ItemModel
from resources.user import UserRegister, UserLogin, UserModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    default="postgresql://punchcard:password@localhost:55432/punchcard",
)

app.config["JWT_SECRET_KEY"] = "avelyn"
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route("/ping", methods=["GET"])
def ping_pong():
    return "pong"

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    userID = UserModel.find_by_id(current_user)
    if current_user and userID:
        return jsonify({"Logged in as" : current_user,
                        "message": "Found user in our db"
        })
    return jsonify({"Logged in as" : "anonymous user"})

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": "Signature verification failed",
        "error": "Invalid token"
    }), 404

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token",
        "error": "Authorization required"
    }), 404

api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    db.init_app(app)
    app.run(
        debug=os.environ.get("DEBUG", default="true") == "true",
        host="0.0.0.0",
        port=os.environ.get("PORT", default=4000),
    )
