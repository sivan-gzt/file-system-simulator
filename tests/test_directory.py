import unittest
from src.file_system.exceptions import DuplicateNameError
from src.file_system.file import File
from src.file_system.directory import Directory


class TestDirectory(unittest.TestCase):
    def setUp(self):
        self.directory = Directory()
        self.directory.add_child(File('foo', 'hello world'))
        self.directory.add_child(Directory('hello'))
        sub_directory = self.directory.find_child('hello')
        sub_directory.add_child(File('world'))
        self.directory.add_child(File('baz'))

    def test_size(self):
        """Test the size of the directory."""
        self.assertGreater(self.directory.size, 0)

    def test_root(self):
        """Test that the root directory has the correct name."""
        self.assertEqual(self.directory.name, '~')

    def test_get_absolute_path(self):
        """Test getting the absolute path of a file."""
        absolute_path = self.directory.find_child('hello').find_child('world').get_absolute_path()
        self.assertEqual(absolute_path, '~/hello/world')

    def test_add_child(self):
        """Test adding a child to the directory."""
        self.assertEqual(self.directory.count, 3)  # Initial count from setUp
        child = Directory('dir1')
        self.directory.add_child(child)
        self.assertEqual(self.directory.count, 4)
        child.add_child(File('hello'))
        self.assertEqual(child.count, 1)

        # Test adding a duplicate name
        with self.assertRaises(DuplicateNameError):
            child.add_child(Directory('hello'))

    def test_remove_child_file(self):
        """Test removing a file from the directory."""
        self.directory.remove_child('foo')
        self.assertIsNone(self.directory.find_child('foo'))
        self.assertEqual(self.directory.count, 2)

    def test_remove_child_directory(self):
        """Test removing a directory."""
        self.directory.remove_child('hello')
        self.assertIsNone(self.directory.find_child('hello'))
        self.assertEqual(self.directory.count, 2)

    def tearDown(self):
        """Clean up after tests."""
        print("Finished\n" + self.directory.list(recurse=True))
        super().tearDown()