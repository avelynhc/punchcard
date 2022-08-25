from flask import request
from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
                            type=inputs.regex("^\w{6,30}[0-9]*_*-*$"),
                            required=True,
                            help="- Username must contain only letters, numbers, underscore or dash - Username must be betwen 6 & 30 characters"
                        )
_user_parser.add_argument("password",
                            type=inputs.regex("^\w{10,20}[0-9]+[!,@,#,$,%,^,&,*,(,),_,+,=,/,?]$"),
                            required=True,
                            help="- Password must contain letters, numbers and one special chracter - Password must be betwen 10 & 20 characters"
                        )

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"messsage": "A user with that username already exists"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully"}, 201


class UserLogin(Resource):
    @classmethod
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        bcrypt = Bcrypt()
        if user and bcrypt.check_password_hash(user.password, data["password"]):
            access_token = create_access_token(
                identity=user.id
            )
            return {
                    "access_token": access_token
            }, 200
        return {"message": "Invalid credentials"}, 401

class RetrieveUser(Resource):
    @classmethod
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            if not user_id:
                raise Exception({"code": "authorization_header_missing",
                                "description": "Authorization header is expected"}, 401)
            current_user = UserModel.find_by_id(user_id)
            if current_user is None:
                raise Exception("not able to find user_id in our database")
            return {'me': user_id}, 200

        except Exception as E:
            print(E)
