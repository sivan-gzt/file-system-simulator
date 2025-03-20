import unittest
from src.file_system.filesystem import FileSystem

class TestFileSystem(unittest.TestCase):

    def setUp(self):
        # Initialize a new file system before each test.
        self.fs = FileSystem()

    # def test_mkdir_and_ls(self):

    # def test_touch_and_ls(self):


    # def test_cd_and_navigation(self):


    # def test_cd_invalid(self):


if __name__ == '__main__':
    unittest.main()
