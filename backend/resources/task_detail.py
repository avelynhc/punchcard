from flask_restful import Resource
from models.task_detail import TaskDetailModel

class TaskDetail(Resource):
    def get(self, task_name):
        task_detail = TaskDetailModel.find_by_id(task_name)
        if task_detail:
            return task_detail.json()
        return {"message": "Task name with task '{}' not found".format(task_detail)}, 404
    
    def post(self, task_name):
        if TaskDetailModel.find_by_id(task_name) and TaskDetailModel.finish_time is None:
            return {"message": "You need to finish '{}' first to be able to start a new task".format(task_name)}, 404
        task_detail = TaskDetailModel(task_name)
        try:
            task_detail.save_to_db()
        except:
            return {"message": "An error occured creating a new task"}, 500
        return task_detail.json()
    
class TaskDetailList(Resource):
    def get(self):
        return {"Task detail": [task_detail.json() for task_detail in  TaskDetailModel.find_all()]}
