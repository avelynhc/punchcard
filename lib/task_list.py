from typing import List

from lib.record import TaskRecord


class TaskList:
    start_err_msg = "you have to finish an existing task first"
    finish_err_message = "you have already finished this task or" \
                         " have not started a task"
    cancel_err_message = "you have not started this task yet"

    records: List[TaskRecord]

    def __init__(self, records: List[TaskRecord] = None):
        if records is None:
            self.records = []
        else:
            self.records = records

    def start_new_task(self):
        if not self.is_task_finished():
            raise Exception(self.start_err_msg)

    def finish_task(self):
        if self.is_task_finished() or len(self.records) == 0:
            raise Exception(self.finish_err_message)

    def cancel_task(self):
        if self.is_task_finished():
            raise Exception(self.cancel_err_message)

    def get_duration(self, from_ts: int, to_ts: int) -> str:
        return "{} hr {} min {} sec".format(len(self.records), from_ts, to_ts)

    def is_task_finished(self) -> bool:
        return len(self.records) > 0
