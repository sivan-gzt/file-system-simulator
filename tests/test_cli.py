import unittest
from src.file_system.filesystem import FileSystem
from src.file_system.exceptions import FileSystemError, NotADirectoryError, DuplicateNameError

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.fs = FileSystem()

    def test_mkdir_nested(self):
        """Test creating nested directories with a single command."""
        self.fs.mkdir("a/b/c")
        self.assertIsNotNone(self.fs.root.find_child("a"))
        self.assertIsNotNone(self.fs.root.find_child("a").find_child("b"))
        self.assertIsNotNone(self.fs.root.find_child("a").find_child("b").find_child("c"))

    def test_touch_nested(self):
        """Test creating a file in a nested directory."""
        self.fs.mkdir("a/b")
        self.fs.touch("a/b/file.txt", content="Hello, World!")
        file = self.fs.root.find_child("a").find_child("b").find_child("file.txt")
        self.assertIsNotNone(file)
        self.assertEqual(file.content, "Hello, World!")

    def test_ls_with_recurse(self):
        """Test listing directory contents recursively."""
        self.fs.mkdir("a/b/c")
        self.fs.touch("a/file1.txt", content="File 1")
        self.fs.touch("a/b/file2.txt", content="File 2")
        output = self.fs.ls(recurse=True)
        self.assertIn("file1.txt", output)
        self.assertIn("file2.txt", output)
        self.assertIn("c", output)

    def test_cd_and_pwd(self):
        """Test changing directories and printing the current working directory."""
        self.fs.mkdir("a/b/c")
        self.fs.cd("a/b")
        self.assertEqual(self.fs.pwd(recurse=True), "~/a/b")
        self.fs.cd("c")
        self.assertEqual(self.fs.pwd(recurse=True), "~/a/b/c")

    def test_touch_overwrite(self):
        """Test overwriting a file using touch."""
        self.fs.touch("file.txt", content="Initial Content")
        self.fs.touch("file.txt", content="Overwritten Content")
        file = self.fs.root.find_child("file.txt")
        self.assertEqual(file.content, "Overwritten Content")

    def test_del_file(self):
        """Test deleting a file."""
        self.fs.touch("file.txt", content="To be deleted")
        self.fs.del_("file.txt")
        self.assertIsNone(self.fs.root.find_child("file.txt"))

    def test_del_directory_recursive(self):
        """Test deleting a directory recursively."""
        self.fs.mkdir("a/b/c")
        self.fs.del_("a", recurse=True)
        self.assertIsNone(self.fs.root.find_child("a"))

    def test_invalid_mkdir(self):
        """Test creating a directory where a file already exists."""
        self.fs.touch("file.txt")
        with self.assertRaises(NotADirectoryError):
            self.fs.mkdir("file.txt/subdir")

    def test_invalid_touch(self):
        """Test creating a file where a directory already exists."""
        self.fs.mkdir("a")
        with self.assertRaises(DuplicateNameError):
            self.fs.touch("a")

    def test_read_file(self):
        """Test reading a file's content."""
        self.fs.touch("file.txt", content="Read me!")
        content = self.fs.read("file.txt")
        self.assertEqual(content, "Read me!")

    def test_size_command(self):
        """Test getting the size of a file and a directory."""
        self.fs.touch("file1.txt", content="12345")
        self.fs.mkdir("a")
        self.fs.touch("a/file2.txt", content="67890")
        file_size = self.fs.size("file1.txt")
        dir_size = self.fs.size("a")
        self.assertEqual(file_size, 5)
        self.assertEqual(dir_size, 5)

    def test_random_commands(self):
        """Test a sequence of random commands."""
        self.fs.mkdir("dir1")
        self.fs.touch("dir1/file1.txt", content="Hello")
        self.fs.touch("dir1/file2.txt", content="World")
        self.fs.mkdir("dir1/subdir")
        self.fs.touch("dir1/subdir/file3.txt", content="!")
        self.fs.del_("dir1/file1.txt")
        self.fs.cd("dir1")
        self.assertEqual(self.fs.pwd(recurse=True), "~/dir1")
        output = self.fs.ls(recurse=True)
        self.assertIn("file2.txt", output)
        self.assertIn("subdir", output)
        self.assertNotIn("file1.txt", output)

if __name__ == "__main__":
    unittest.main()
