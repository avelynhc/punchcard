from flask import request
from flask_restful import Resource
from models.task_detail import TaskDetailModel
from flask_jwt_extended import jwt_required
import time

# this post will be only used when user posts first task
class TaskDetail(Resource):
    @jwt_required()
    def get(self, task_name):
        try:
            current_user = TaskDetailModel.find_current_user()
        except:
            return {"message": "not able to verify user_id"}, 401
        try:
            task_detail = TaskDetailModel.find_by_user_id(current_user.id, task_name)
            if task_detail:
                args = request.args
                duration = 0
                from_ts = args.get("from", default=int(task_detail[0].start_time), type=int)
                to_ts = args.get("to", default=int(time.time()), type=int)
                duration = to_ts - from_ts
                return {"duration": duration}, 200
            return {"message": "you do not have task '{}' in your task list".format(task_name)}, 404
        except:
            return {"message": "an error occured to get the task detail"}, 500

    @jwt_required()
    def post(self, task_name):
        try:
            current_user = TaskDetailModel.find_current_user()
        except:
            return {"message": "not able to verify user_id"}, 401
        try:
            task_detail = TaskDetailModel.find_unfinished_by_user_id(current_user.id, task_name)
        except:
            return {"message": "an error occured to get the task detail"}, 500
        if task_detail is not None:
            return {"message": "you need to finish task '{}' first to be able to start a new project".format(task_name)}, 404
        new_task = TaskDetailModel(current_user.id, task_name, int(time.time()))
        new_task.save_to_db()
        return new_task.json()


class TaskDetailWithFinish(Resource):
    @jwt_required()
    def post(self, task_name):
        try:
            current_user = TaskDetailModel.find_current_user()
        except:
            return {"message": "not able to verify user_id"}, 401
        try:
            task_detail = TaskDetailModel.find_unfinished_by_user_id(current_user.id, task_name)
        except:
            return {"message": "an error occured to get the task detail"}, 500
        if task_detail is None:
            return {"message": "you do not have unfinished task named '{}'".format(task_name)}, 404
        task_detail.finish_time = int(time.time())
        task_detail.save_to_db()
        return task_detail.json()

class TaskDetailWithCancel(Resource):
    @jwt_required()
    def post(self, task_name):
        try:
            current_user = TaskDetailModel.find_current_user()
        except:
            return {"message": "not able to verify user_id"}, 401
        try:
            task_detail = TaskDetailModel.find_unfinished_by_user_id(current_user.id, task_name)
            if task_detail is None:
                return {"message": "you are not authorized to cancel already finished task named '{}'".format(task_name)}, 404
            task_detail.delete_from_db()
            return task_detail.json()
        except:
            return {"message": "internal server error"}, 500


class TaskDetailList(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = TaskDetailModel.find_current_user()
        except:
            return {"message": "Not able to verify user_id"}, 401
        try:
            task_detail = TaskDetailModel.query.filter_by(user_id=current_user.id).all()
        except:
            return {"message": "An error occured to get the task detail"}, 500
        if task_detail:
            task_list = [task.json() for task in task_detail]
            return {"task_detail" : task_list}, 200
        return {"message": "You do not have any task in your list yet"}, 200
