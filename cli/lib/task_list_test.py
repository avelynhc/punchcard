from datetime import datetime
import unittest

from lib.record import TaskRecord
from lib.task_list import TaskList


class TestTaskListClass(unittest.TestCase):
    def test_initialization(self):
        test_task_list = TaskList()

        self.assertListEqual(test_task_list.records, [])

    def test_initialization_with_records(self):
        record = TaskRecord(10, 20)
        test_records = [record]
        test_task_list = TaskList(test_records)

        self.assertListEqual(test_task_list.records, test_records)

    def test_is_task_finished(self):
        record_one = TaskRecord(10, 20)
        record_two = TaskRecord(30, 40)
        test_records = [record_one, record_two]
        test_task_list = TaskList(test_records)

        self.assertTrue(test_task_list.is_task_finished())

    def test_is_task_finished_false(self):
        record_one = TaskRecord(10)
        test_records = [record_one]
        test_task_list = TaskList(test_records)

        self.assertFalse(test_task_list.is_task_finished())

    def test_start_new_task(self):
        test_task_list = TaskList()
        test_task_list.start_new_task()

        self.assertEqual(len(test_task_list.records), 1)
        self.assertIsNotNone(test_task_list.records[0].start)
        self.assertIsNone(test_task_list.records[0].finished)
        self.assertFalse(test_task_list.is_task_finished())

    def test_start_new_task_failure(self):
        with self.assertRaises(Exception) as context:
            test_task_list = TaskList()
            test_task_list.start_new_task()
            test_task_list.start_new_task()
        self.assertTrue(TaskList.start_err_msg in str(context.exception))

    def test_finish_task(self):
        test_task_list = TaskList()
        test_task_list.start_new_task()
        test_task_list.finish_task()

        self.assertIsNotNone(test_task_list.records[0].start)
        self.assertIsNotNone(test_task_list.records[0].finished)
        self.assertTrue(test_task_list.is_task_finished())

    def test_finish_task_failure(self):
        with self.assertRaises(Exception) as context:
            test_task_list = TaskList()
            test_task_list.finish_task()
        self.assertTrue(TaskList.finish_err_message in str(context.exception))

    def test_cancel_task(self):
        test_task_list = TaskList()
        test_task_list.start_new_task()
        test_task_list.cancel_task()

        self.assertEqual(len(test_task_list.records), 0)

    def test_cancel_task_failure(self):
        test_task_list = TaskList()
        test_task_list.start_new_task()
        test_task_list.finish_task()
        with self.assertRaises(Exception) as context:
            test_task_list.cancel_task()
        self.assertTrue(TaskList.cancel_err_message in str(context.exception))

    def test_get_duration(self):
        test_task_list = TaskList()
        test_task_list.records.append(TaskRecord(1637897745, 1637899545))

        from_ts = datetime.strptime("2021/01/01", "%Y/%m/%d")
        from_ts = from_ts.replace(hour=12, minute=0).timestamp()
        to_ts = datetime.strptime("2022/01/10", "%Y/%m/%d")
        to_ts = to_ts.replace(hour=12, minute=0).timestamp()
        duration = test_task_list.get_duration(int(from_ts), int(to_ts))

        self.assertEqual(duration, "0 hr 30 min 0 sec")

    def test_get_duration_fail(self):
        test_task_list = TaskList()

        from_ts = datetime.strptime("2021/01/01", "%Y/%m/%d")
        from_ts = from_ts.replace(hour=12, minute=0).timestamp()
        to_ts = datetime.strptime("2022/01/10", "%Y/%m/%d")
        to_ts = to_ts.replace(hour=12, minute=0).timestamp()
        duration = test_task_list.get_duration(int(from_ts), int(to_ts))

        self.assertEqual(duration, "0 hr 0 min 0 sec")


if __name__ == '__main__':
    unittest.main()
