from typing import Dict
import json

from lib.task_list import TaskList


class TaskManager:
    start_success_msg = "successfully started {}"
    finish_success_msg = "successfully finished {}"
    task_not_found_msg = "Error: no task named {} found"
    cancel_success_msg = "successfully cancelled {}"

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
        # self.save_data()
        if task_name in self.tasks.keys():
            try:
                task_list = self.tasks[task_name]
                task_list.start_new_task()
            except Exception as err:
                return "Error: {}".format(err)
        else:
            new_task_list = TaskList()
            new_task_list.start_new_task()
            self.tasks[task_name] = new_task_list
        return self.start_success_msg.format(task_name)

    def finish_task(self, task_name: str) -> str:
        # self.save_data()
        if task_name not in self.tasks.keys():
            return self.task_not_found_msg.format(task_name)
        try:
            task_list = self.tasks[task_name]
            task_list.finish_task()
        except Exception as err:
            return "Error: {}".format(err)
        return self.finish_success_msg.format(task_name)

    def cancel_task(self, task_name: str) -> str:
        # self.save_data()
        if task_name not in self.tasks.keys():
            return self.task_not_found_msg.format(task_name)
        try:
            task_list = self.tasks[task_name]
            task_list.cancel_task()
        except Exception as err:
            return "Error: {}".format(err)
        return self.cancel_success_msg.format(task_name)

    def get_task(self, task_name: str, from_ts: int, to_ts: int) -> str:
        if task_name not in self.tasks.keys():
            return self.task_not_found_msg.format(task_name)
        return self.tasks[task_name].get_duration(from_ts, to_ts)
