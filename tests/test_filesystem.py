# tests/test_filesystem.py
import unittest
from file_system.filesystem import FileSystem

class TestFileSystem(unittest.TestCase):

    def setUp(self):
        # Initialize a new file system before each test.
        self.fs = FileSystem()

    def test_mkdir_and_ls(self):
        # Initially, ls should return an empty list.
        self.assertEqual(self.fs.ls(), [])
        # Create a new directory.
        result = self.fs.mkdir("dir1")
        self.assertEqual(result, "Directory 'dir1' created.")
        # ls should now show 'dir1'.
        self.assertEqual(self.fs.ls(), ["dir1"])
        # Attempt to create the same directory again.
        result = self.fs.mkdir("dir1")
        self.assertEqual(result, "Directory 'dir1' already exists.")

    def test_touch_and_ls(self):
        # Initially, ls should be empty.
        self.assertEqual(self.fs.ls(), [])
        # Create a new file.
        result = self.fs.touch("file1.txt")
        self.assertEqual(result, "File 'file1.txt' created.")
        self.assertEqual(self.fs.ls(), ["file1.txt"])
        # Attempt to create the same file again.
        result = self.fs.touch("file1.txt")
        self.assertEqual(result, "File 'file1.txt' already exists.")

    def test_cd_and_navigation(self):
        # Create a directory and change to it.
        self.fs.mkdir("subdir")
        result = self.fs.cd("subdir")
        self.assertEqual(result, "Moved to directory 'subdir'.")
        # In the new directory, ls should be empty.
        self.assertEqual(self.fs.ls(), [])
        # Create a file inside 'subdir'.
        result = self.fs.touch("inside.txt")
        self.assertEqual(result, "File 'inside.txt' created.")
        self.assertEqual(self.fs.ls(), ["inside.txt"])
        # Navigate back to the root directory.
        result = self.fs.cd("..")
        self.assertEqual(result, "Moved to directory 'root'.")
        # Root should show the 'subdir'.
        self.assertEqual(self.fs.ls(), ["subdir"])

    def test_cd_invalid(self):
        # Try changing to a directory that doesn't exist.
        result = self.fs.cd("nonexistent")
        self.assertEqual(result, "Directory 'nonexistent' not found.")
        # Create a file and try using cd on it.
        self.fs.touch("file.txt")
        result = self.fs.cd("file.txt")
        self.assertEqual(result, "Directory 'file.txt' not found.")

if __name__ == '__main__':
    unittest.main()
