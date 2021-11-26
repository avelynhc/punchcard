from typing import Dict
import json

from lib.task_list import TaskList


class TaskManager:
    data_file_path: str
    tasks: Dict[str, TaskList]

    def read_data(self):
        self.tasks = {}

    def save_data(self):
        with open(self.data_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path
        self.tasks = {}

    def start_task(self, task_name: str) -> str:
        self.save_data()
        return "successfully started {}".format(task_name)

    def finish_task(self, task_name: str) -> str:
        if not self.has_task(task_name):
            raise Exception("no task named {} found".format(task_name))
        self.save_data()
        return "successfully finished {}".format(task_name)

    def cancel_task(self, task_name: str) -> str:
        if not self.has_task(task_name):
            raise Exception("no task named {} found".format(task_name))
        self.save_data()
        return "successfully canceled {}".format(task_name)

    def get_task(self, task_name: str, from_ts: int, to_ts: int) -> str:
        if not self.has_task(task_name):
            raise Exception("no task named {} found".format(task_name))
        return self.tasks[task_name].get_duration(from_ts, to_ts)

    def has_task(self, task_name):
        return True
