import unittest
from file_system.node import FSNode

class TestNode(unittest.TestCase):
    def setUp(self):
        self.parent_node = FSNode('parent')
        self.child_node = FSNode('child', self.parent_node)

    def test_get_parent(self):
        self.assertEqual(self.child_node.get_parent(), self.parent_node)

if __name__ == '__main__':
    unittest.main()