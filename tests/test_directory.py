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

    def test_overwrite_file_in_directory(self):
        """Test overwriting a file in a directory and updating size."""
        # Initial setup
        self.directory.add_child(File('test_file', 'initial content'))
        initial_size = self.directory.size

        # Overwrite the file with new content
        self.directory.add_child(File('test_file', 'new content'), overwrite=True)
        self.assertEqual(self.directory.find_child('test_file').content, 'new content')

        # Verify size update
        new_size = self.directory.size
        self.assertNotEqual(initial_size, new_size)
        self.assertEqual(new_size, initial_size - len('initial content') + len('new content'))

    def test_overwrite_file_with_same_content(self):
        """Test overwriting a file with the same content does not change size."""
        # Initial setup
        self.directory.add_child(File('test_file', 'same content'))
        initial_size = self.directory.size

        # Overwrite the file with the same content
        self.directory.add_child(File('test_file', 'same content'), overwrite=True)
        self.assertEqual(self.directory.find_child('test_file').content, 'same content')

        # Verify size remains unchanged
        self.assertEqual(self.directory.size, initial_size)

    def tearDown(self):
        """Clean up after tests."""
        print("Finished\n" + self.directory.list(recurse=True))
        super().tearDown()


if __name__ == "__main__":
    unittest.main()