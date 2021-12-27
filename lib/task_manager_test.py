import unittest

from lib.task_manager import TaskManager


class TestManagerClass(unittest.TestCase):
    def test_initialization(self):
        test_manager = TaskManager("data.json")

        self.assertEqual(test_manager.data_file_path, "data.json")
        self.assertDictEqual(test_manager.tasks, {})


if __name__ == '__main__':
    unittest.main()
