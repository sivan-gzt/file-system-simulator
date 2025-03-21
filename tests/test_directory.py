import unittest
from src.file_system.exceptions import DuplicateNameError
from src.file_system.file import File
from src.file_system.directory import Directory


class TestDirectory(unittest.TestCase):
    def setUp(self):
        directory = Directory()
        self.directory = directory
        directory.add_child(File('foo'))
        directory.add_child(Directory('hello'))
        sub_directory = directory.find_child('hello')
        sub_directory.add_child(File('world'))
        directory.add_child(File('baz'))
        print(self.directory.list(recurse=True))

    def test_size(self):
        print(self.directory.size)

    def test_root(self):
        self.assertIn('~', self.directory.name)

    def test_get_absolute_path(self):
        print(self.directory.list(recurse=True))
        print(self.directory.find_child('hello').list())
        print(self.directory.find_child('hello').find_child('world').get_absolute_path())

    def test_add_child(self):
        """Test adding child"""
        self.assertEqual(self.directory.count, 3)
        """Sanity check - 2 nodes from setUp"""
        child = Directory('dir1')
        self.assertIsNone(self.directory.add_child(child))
        self.assertEqual(self.directory.count, 4)
        child.add_child(File('hello'))
        self.assertEqual(child.count, 1)

        self.assertEqual(self.directory.count, 4) # cant add file with existing name in directory
        with self.assertRaises(DuplicateNameError) as cm:
            child.add_child(Directory('hello'))
            
        
      
    def test_remove_child_file(self):
        self.directory.remove_child('hello')

    def test_remove_child_directory(self):
        success = self.directory.remove_child('hello')
        self.assertEqual(self.directory.count, 2)

    def tearDown(self):
        
        print("Finished\n" + self.directory.list(recurse=True))
        return super().tearDown()