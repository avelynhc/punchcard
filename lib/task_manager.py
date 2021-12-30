import json
from typing import Dict

from lib.record import TaskRecord
from lib.task_list import TaskList


class TaskManager:
    start_success_msg = "successfully started {}"
    finish_success_msg = "successfully finished {}"
    task_not_found_msg = "Error: no task named {} found"
    cancel_success_msg = "successfully cancelled {}"

    tasks: Dict[str, TaskList]

    def __init__(self, json_data=None):
        self.tasks = {}
        if json_data is None:
            json_data = {}
        self.parse_data(json_data)

    def to_json(self) -> str:
        return json.dumps({}, indent=2)

    def parse_data(self, raw_data: Dict):
        self.tasks = {}
        if "tasks" in raw_data:
            for task_name in raw_data["tasks"]:
                self.tasks[task_name] = TaskList()
                for record in raw_data["tasks"][task_name]:
                    current_record = self.tasks[task_name].records
                    if "finish" in current_record:
                        current_record.append(TaskRecord(record["start"],record["finish"]))
                    else:
                        current_record.append(TaskRecord(record["start"]))


    def start_task(self, task_name: str) -> str:
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
        if task_name not in self.tasks.keys():
            return self.task_not_found_msg.format(task_name)
        try:
            task_list = self.tasks[task_name]
            task_list.finish_task()
        except Exception as err:
            return "Error: {}".format(err)
        return self.finish_success_msg.format(task_name)

    def cancel_task(self, task_name: str) -> str:
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
