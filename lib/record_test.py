from datetime import datetime
import unittest

from lib.record import TaskRecord


class TestRecordClass(unittest.TestCase):
    def test_initialization(self):
        test_record = TaskRecord(12, 24)

        self.assertEqual(test_record.start, 12)
        self.assertEqual(test_record.finished, 24)

    def test_start_only_initialization(self):
        test_record = TaskRecord(12)

        self.assertEqual(test_record.start, 12.12)
        self.assertEqual(test_record.finished, None)

    def test_get_duration(self):
        test_record = TaskRecord(12, 24)
        duration = test_record.get_duration()

        self.assertEqual(duration, 12.12)

    def test_start_only_get_duration(self):
        test_record = TaskRecord(12)
        duration = test_record.get_duration()

        self.assertEqual(duration, 0)

    def test_is_timestamp_in_between(self):
        start_ts = datetime.strptime("2021/11/02", "%Y/%m/%d").timestamp()
        finished_ts = datetime.strptime("2021/11/05", "%Y/%m/%d").timestamp()
        test_record = TaskRecord(int(start_ts), int(finished_ts))

        from_ts = datetime.strptime("2021/11/01", "%Y/%m/%d")
        from_ts = from_ts.replace(hour=12, minute=0).timestamp()
        to_ts = datetime.strptime("2021/11/10", "%Y/%m/%d")
        to_ts = to_ts.replace(hour=12, minute=0).timestamp()
        is_in_between = test_record.is_timestamp_in_range(
            int(from_ts),
            int(to_ts),
        )

        self.assertTrue(is_in_between)

    def test_start_only_is_timestamp_in_between(self):
        start_ts = datetime.strptime("2021/11/02", "%Y/%m/%d").timestamp()
        test_record = TaskRecord(int(start_ts))

        from_ts = datetime.strptime("2021/11/01", "%Y/%m/%d")
        from_ts = from_ts.replace(hour=12, minute=0).timestamp()
        to_ts = datetime.strptime("2021/11/10", "%Y/%m/%d")
        to_ts = to_ts.replace(hour=12, minute=0).timestamp()
        is_in_between = test_record.is_timestamp_in_range(
            int(from_ts),
            int(to_ts),
        )

        self.assertFalse(is_in_between)


if __name__ == '__main__':
    unittest.main()
