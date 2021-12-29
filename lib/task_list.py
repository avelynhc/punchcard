from typing import List

from lib.record import TaskRecord

import time


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

    def is_task_finished(self) -> bool:
        for record in self.records:
            if record.finished is None:
                return False
        return True

    def start_new_task(self):
        if not self.is_task_finished():
            raise Exception(self.start_err_msg)
        new_record = TaskRecord(int(time.time()))
        self.records.append(new_record)

    def finish_task(self):
        if self.is_task_finished() or len(self.records) == 0:
            raise Exception(self.finish_err_message)
        last_index = len(self.records) - 1
        self.records[last_index].finished = int(time.time())

    def cancel_task(self):
        if self.is_task_finished():
            raise Exception(self.cancel_err_message)
        for record in self.records:
            if record.start > 0:
                self.records.pop()

    def get_duration(self, from_ts: int, to_ts: int) -> str:
        time_diff = 0
        for record in self.records:
            if record.start >= from_ts and record.finished <= to_ts:
                time_diff += record.get_duration()*1000
        if time_diff > 0:
            sec = (time_diff/1000) % 60
            min = (time_diff/(1000*60)) % 60
            hr = (time_diff/(1000*60*60)) % 24
            return "{} hr {} min {} sec".format(int(hr), int(min), int(sec))
        return "0 hr 0 min 0 sec"


