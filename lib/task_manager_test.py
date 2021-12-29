import unittest
import time

from lib.task_manager import TaskManager
from lib.task_list import TaskList


class TestManagerClass(unittest.TestCase):
    def test_initialization(self):
        test_task_manager = TaskManager("data.json")

        self.assertEqual(test_task_manager.data_file_path, "data.json")
        self.assertDictEqual(test_task_manager.tasks, {})

    def test_manager_start_task(self):
        task_name = "testing"
        test_task_manager = TaskManager("data.json")
        start_msg = test_task_manager.start_task(task_name)

        self.assertIn(task_name, test_task_manager.tasks.keys())
        self.assertEqual(len(test_task_manager.tasks[task_name].records), 1)
        self.assertEqual(
            start_msg,
            test_task_manager.start_success_msg.format(task_name)
        )

    def test_manager_start_task_failure(self):
        task_name = "testing"
        test_task_manager = TaskManager("data.json")
        test_task_manager.start_task(task_name)
        start_msg = test_task_manager.start_task(task_name)

        self.assertEqual(start_msg, "Error: {}".format(TaskList.start_err_msg))

    def test_manager_finish_task(self):
        task_name = "testing"
        test_task_manager = TaskManager("data.json")
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
        test_task_manager = TaskManager("data.json")
        finish_msg = test_task_manager.finish_task(task_name)

        self.assertEqual(
            finish_msg,
            test_task_manager.task_not_found_msg.format(task_name)
        )

    def test_manager_finish_task_failure_already_finished(self):
        task_name = "testing"
        test_task_manager = TaskManager("data.json")
        test_task_manager.start_task(task_name)
        test_task_manager.finish_task(task_name)
        finish_msg = test_task_manager.finish_task(task_name)

        self.assertEqual(
            finish_msg,
            "Error: {}".format(TaskList.finish_err_message)
        )

    def test_manager_cancel_task(self):
        task_name = "testing"
        test_task_manager = TaskManager("data.json")
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
        test_task_manager = TaskManager("data.json")
        cancel_msg = test_task_manager.cancel_task(task_name)

        self.assertEqual(
            cancel_msg,
            test_task_manager.task_not_found_msg.format(task_name)
        )

    def test_manager_cancel_task_failure_already_finished(self):
        task_name = "testing"
        test_task_manager = TaskManager("data.json")
        test_task_manager.start_task(task_name)
        test_task_manager.finish_task(task_name)
        cancel_msg = test_task_manager.cancel_task(task_name)

        self.assertEqual(
            cancel_msg,
            "Error: {}".format(TaskList.cancel_err_message)
        )

    def test_manager_get_task(self):
        task_name = "testing"
        test_task_manager = TaskManager("data.json")
        test_task_manager.start_task(task_name)
        time.sleep(1)
        test_task_manager.finish_task(task_name)
        get_msg = test_task_manager.get_task(task_name, 0, 9999999999)

        print(test_task_manager.tasks[task_name].records[0].start)
        print(test_task_manager.tasks[task_name].records[0].finished)
        self.assertNotEqual(get_msg, "0 hr 0 min 0 sec")

    def test_manager_get_task_failure(self):
        task_name = "testing"
        test_task_manager = TaskManager("data.json")
        get_msg = test_task_manager.get_task(task_name, 0, 9999999999)

        self.assertEqual(
            get_msg,
            test_task_manager.task_not_found_msg.format(task_name)
        )


if __name__ == '__main__':
    unittest.main()
