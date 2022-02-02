from db.migrations.create_table import db
from models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class TaskDetailModel(db.Model):
    __tablename__ = "task_details"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.BigInteger)
    finish_time = db.Column(db.BigInteger)
    task_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    def __init__(self, task_name, start_time, user_id):
        self.start_time = start_time
        # self.finish_time = finish_time
        self.task_name = task_name
        self.user_id = user_id
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_name(cls, taskName):
        return cls.query.filter_by(task_name=taskName).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "id" : self.id,
            "task_name" : self.task_name,
            "start_time" : self.start_time
        }

    @classmethod
    @jwt_required()
    def find_current_user(cls):
        user_id = get_jwt_identity()
        if user_id is None:
            return {"message": "Not able to retrieve user id"}, 404
        current_user = UserModel.find_by_id(user_id)
        if current_user is None:
            return {"message": "Not able to find user_id in our database"}, 404
        return current_user
