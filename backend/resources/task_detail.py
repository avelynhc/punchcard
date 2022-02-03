from flask_restful import Resource
from models.task_detail import TaskDetailModel
from flask_jwt_extended import jwt_required, get_jwt_identity
import time
from db.migrations.create_table import db

# this post will be only used when user posts first task
class TaskDetail(Resource):
    @jwt_required()
    def get(self, task_name):
        current_user = TaskDetailModel.find_current_user()
        task_detail = TaskDetailModel.find_by_name(task_name)
        if task_detail is None:
            return {"message": "Task name with task '{}' not found".format(task_name)}, 404
        task = TaskDetailModel.query.filter_by(task_name=task_detail.task_name).all()
        try:
            if current_user and task:
                return task_detail.json()
        except:
            return {"message": "An error occured getting the task"}, 500

    @jwt_required()
    def post(self, task_name):
        current_user = get_jwt_identity()
        task_detail = TaskDetailModel.find_by_name(task_name)
        print(task_detail)
        if task_detail and not TaskDetailModel.is_task_finished():
            return {"message": "You need to finish task '{}' first to be able to start a new project".format(task_name)}, 404
        task_detail = TaskDetailModel(current_user, task_name, int(time.time()))
        try:
            task_detail.save_to_db()
        except:
            return {"message": "An error occured creating a new task"}, 500
        return task_detail.json()

class TaskDetailWithFinish(Resource):
    @jwt_required()
    def post(self, task_name):
        current_user = TaskDetailModel.find_current_user()
        task_detail = TaskDetailModel.find_by_name(task_name)
        if current_user and task_detail is None:
            return {"message": "You first need to start the task '{}'".format(task_name)}, 404
        try:
            task_detail.finish_time = int(time.time())
            db.session.commit()
        except:
            return {"message": "An error occured adding a finish time"}, 500
        return task_detail.json()


class TaskDetailList(Resource):
    @jwt_required()
    def get(self):
        current_user = TaskDetailModel.find_current_user()
        task_lists = [item.json() for item in TaskDetailModel.query.filter_by(user_id=current_user.id).all()]
        try:
            if current_user:
                return {"Task detail" : task_lists}, 200
        except:
            return {"message": "Log in to access the list of your project"}, 200
