import json
import unittest
import time

from lib.task_manager import TaskManager
from lib.task_list import TaskList
from lib.record import TaskRecord


class TestManagerClass(unittest.TestCase):
    def test_initialization(self):
        test_task_manager = TaskManager()

        self.assertDictEqual(test_task_manager.tasks, {})

    def test_manager_start_task(self):
        task_name = "testing"
        test_task_manager = TaskManager()
        start_msg = test_task_manager.start_task(task_name)

        self.assertIn(task_name, test_task_manager.tasks.keys())
        self.assertEqual(len(test_task_manager.tasks[task_name].records), 1)
        self.assertEqual(
            start_msg,
            test_task_manager.start_success_msg.format(task_name)
        )

    def test_manager_start_task_failure(self):
        task_name = "testing"
        test_task_manager = TaskManager()
        test_task_manager.start_task(task_name)
        start_msg = test_task_manager.start_task(task_name)

        self.assertEqual(start_msg, "Error: {}".format(TaskList.start_err_msg))

    def test_manager_finish_task(self):
        task_name = "testing"
        test_task_manager = TaskManager()
        test_task_manager.start_task(task_name)
        finish_msg = test_task_manager.finish_task(task_name)

        test_record = test_task_manager.tasks[task_name].records
        self.assertIn(task_name, test_task_manager.tasks.keys())
        self.assertEqual(len(test_record), 1)
        self.assertIsNotNone(test_record[0].finished)
        self.assertEqual(
            finish_msg,
            test_task_manager.finish_success_msg.format(task_name)
        )

    def test_manager_finish_task_failure_not_started(self):
        task_name = "testing"
        test_task_manager = TaskManager()
        finish_msg = test_task_manager.finish_task(task_name)

        self.assertEqual(
            finish_msg,
            test_task_manager.task_not_found_msg.format(task_name)
        )

    def test_manager_finish_task_failure_already_finished(self):
        task_name = "testing"
        test_task_manager = TaskManager()
        test_task_manager.start_task(task_name)
        test_task_manager.finish_task(task_name)
        finish_msg = test_task_manager.finish_task(task_name)

        self.assertEqual(
            finish_msg,
            "Error: {}".format(TaskList.finish_err_message)
        )

    def test_manager_cancel_task(self):
        task_name = "testing"
        test_task_manager = TaskManager()
        test_task_manager.start_task(task_name)
        cancel_msg = test_task_manager.cancel_task(task_name)

        self.assertIn(task_name, test_task_manager.tasks.keys())
        self.assertEqual(len(test_task_manager.tasks[task_name].records), 0)
        self.assertEqual(
            cancel_msg,
            test_task_manager.cancel_success_msg.format(task_name)
        )

    def test_manager_cancel_task_failure_not_started(self):
        task_name = "testing"
        test_task_manager = TaskManager()
        cancel_msg = test_task_manager.cancel_task(task_name)

        self.assertEqual(
            cancel_msg,
            test_task_manager.task_not_found_msg.format(task_name)
        )

    def test_manager_cancel_task_failure_already_finished(self):
        task_name = "testing"
        test_task_manager = TaskManager()
        test_task_manager.start_task(task_name)
        test_task_manager.finish_task(task_name)
        cancel_msg = test_task_manager.cancel_task(task_name)

        self.assertEqual(
            cancel_msg,
            "Error: {}".format(TaskList.cancel_err_message)
        )

    def test_manager_get_task(self):
        task_name = "testing"
        test_task_manager = TaskManager()
        test_task_manager.start_task(task_name)
        time.sleep(1)
        test_task_manager.finish_task(task_name)
        get_msg = test_task_manager.get_task(task_name, 0, 9999999999)

        self.assertNotEqual(get_msg, "0 hr 0 min 0 sec")

    def test_manager_get_task_failure(self):
        task_name = "testing"
        test_task_manager = TaskManager()
        get_msg = test_task_manager.get_task(task_name, 0, 9999999999)

        self.assertEqual(
            get_msg,
            test_task_manager.task_not_found_msg.format(task_name)
        )

    def test_manager_parse_data(self):
        test_json_dict = {
            "tasks": {
                "test": [],
                "manage": [
                    {
                        "start": 1640747299,
                        "finish": 1640747304
                    },
                    {
                        "start": 1640747299
                    }
                ],
            }
        }
        test_task_manager = TaskManager()
        test_task_manager.parse_data(test_json_dict)

        self.assertEqual(len(test_task_manager.tasks), 2)

        for task_name in test_json_dict["tasks"]:
            self.assertTrue(task_name in test_task_manager.tasks)

            current_task = test_task_manager.tasks[task_name]
            self.assertIsInstance(current_task, TaskList)
            self.assertEqual(
                len(current_task.records),
                len(test_json_dict["tasks"][task_name])
            )
            for record in test_task_manager.tasks[task_name].records:
                self.assertIsInstance(record, TaskRecord)

    def test_manager_to_json(self):
        test_json_dict = {
            "tasks": {
                "test": [],
                "manage": [
                    {
                        "start": 1640747299,
                        "finish": 1640747304
                    },
                    {
                        "start": 1640747299
                    }
                ],
            }
        }
        test_task_manager = TaskManager()
        test_task_manager.parse_data(test_json_dict)
        self.assertEqual(
            test_task_manager.to_json(),
            test_json_dict
        )


if __name__ == '__main__':
    unittest.main()
