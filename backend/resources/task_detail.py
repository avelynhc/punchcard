from flask_restful import Resource
from models.task_detail import TaskDetailModel
from flask_jwt_extended import jwt_required, get_jwt_identity
import time

class TaskDetail(Resource):
    @jwt_required()
    def post(self, task_name):
        user_id = get_jwt_identity()
        isDup = TaskDetailModel.find_by_name(task_name)
        if isDup:
            return {"message": "You need to finish task '{}' first to be able to start a new project".format(task_name)}, 404
        task_detail = TaskDetailModel(task_name,int(time.time()),user_id)
        try:
            task_detail.save_to_db()
        except:
            return {"message": "An error occured creating a new task"}, 500
        return task_detail.json()
    
    @jwt_required()
    def get(self, task_name):
        TaskDetailModel.find_current_user()
        task_detail = TaskDetailModel.find_by_name(task_name)
        if task_detail is None:
            return {"message": "Task name with task '{}' not found".format(task_name)}, 404
        task = TaskDetailModel.query.filter_by(task_name=task_detail.task_name).first()
        try:
            if task:
                return task_detail.json()
        except:
            return {"message": "An error occured getting the task"}, 500


class TaskDetailList(Resource):
    @jwt_required()
    def get(self):
        current_user = TaskDetailModel.find_current_user()
        task_lists = [item.json() for item in TaskDetailModel.query.filter_by(user_id=current_user.id).all()]
        try:
            if task_lists is not None:
                return {"Task detail" : task_lists}, 200
        except:
            return {"message": "Log in to access the list of your project"}, 200
