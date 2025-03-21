import unittest
from datetime import datetime, timedelta
from src.file_system.node import FSNode
from src.file_system.validation import InvalidNameError
from time import sleep


class TestFSNode(unittest.TestCase):

    def setUp(self):
        """Set up a basic FSNode instance for testing."""
        self.node = FSNode("test_node")

    def test_initialization(self):
        """Test that FSNode initializes correctly."""
        self.assertEqual(self.node.name, "test_node")
        self.assertEqual(self.node.entity_type, "FSNode")
        self.assertIsInstance(self.node.ctime, datetime)
        self.assertEqual(self.node.ctime, self.node.mtime)

    def test_str_representation(self):
        """Test the string representation of FSNode."""
        self.assertEqual(str(self.node), "test_node")

    def test_modify_updates_mtime(self):
        """Test that modify() updates the mtime."""
        old_mtime = self.node.mtime
        sleep(0.01)
        self.node.modify()
        self.assertGreater(self.node.mtime, old_mtime)
        self.assertLess(self.node.mtime - old_mtime, timedelta(seconds=1))

    def test_validate_valid_name(self):
        """Test that validate() accepts valid names."""
        try:
            self.node.validate("valid_name")
        except InvalidNameError:
            self.fail("validate() raised InvalidNameError unexpectedly!")

    def test_validate_invalid_name(self):
        """Test that validate() raises an error for invalid names."""
        with self.assertRaises(InvalidNameError):
            self.node.validate("///invalid_name")

if __name__ == '__main__':
    unittest.main()