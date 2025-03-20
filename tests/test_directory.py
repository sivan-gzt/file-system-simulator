import unittest
from src.file_system.exceptions import DuplicateNameError
from src.file_system.file import File
from src.file_system.directory import Directory


class TestDirectory(unittest.TestCase):
    def setUp(self):
        self.directory = Directory()
        self.directory.add_child(File('foo'))
        self.directory.add_child(Directory('hello'))
        self.directory.get_child('hello').add_child(File('world'))

    def test_root(self):
        self.assertIn('~', self.directory.name)

    def test_get_absolute_path(self):
        print(self.directory.list())
        print(self.directory.get_child('hello').list())
        print(self.directory.get_child('hello').get_child('world').get_absolute_path())

    def test_add_child(self):
        """Test adding child"""
        self.assertEqual(self.directory.count, 2)
        """Sanity check - 2 nodes from setUp"""
        child = Directory('dir1')
        self.directory.add_child(child)
        """add_child"""
        self.assertEqual(self.directory.count, 3)
        """Sanity check - 3 nodes now"""
        child.add_child(File('hello'))
        self.assertEqual(self.directory.count, 3)
        with self.assertRaises(DuplicateNameError) as cm:
            child.add_child(Directory('hello'))
            
        print(self.directory.list(recurse=True))
        
      
    def test_remove_child_file(self):
        self.directory.remove_child('hello')

    def test_remove_child_directory(self):
        success = self.directory.remove_child('hello')
        self.assertEqual(self.directory.count, 1)