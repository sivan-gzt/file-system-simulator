
import unittest
from src.file_system.exceptions import InvalidNameError
from src.file_system.node import FSNode 


class TestNode(unittest.TestCase):
    def setUp(self):
        self.node = FSNode('node')

    def test_rename_invalid(self):
        """Test renaming a node with an invalid name"""
        with self.assertRaises(InvalidNameError):
            self.node.rename("///invalid")

    def test_rename_valid(self):
        """Test renaming a node with a valid name"""
        self.node.rename("new_name")
        self.assertEqual(self.node.name, "new_name")

    def test_get_absolute_path(self):
        """Test absolute path of several types"""
        node = FSNode('a')
        child = FSNode('b', node)
        child2 = FSNode('c', child)
        child3 = FSNode('d', child)
        child4 = FSNode('e', node)

        self.assertEqual('/a/b', child.get_absolute_path())
        self.assertEqual('/a/b/c', child2.get_absolute_path())
        self.assertEqual('/a/b/d', child3.get_absolute_path())
        self.assertEqual('/a/e', child4.get_absolute_path())



if __name__ == '__main__':
    unittest.main()