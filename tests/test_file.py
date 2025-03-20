import unittest
import time
from src.file_system.file import File
from src.file_system.exceptions import InvalidNameError

class TestFile(unittest.TestCase):

    def test_create_valid_file(self):
        """Test creating a file with a valid name"""
        file = File("test_file")
        self.assertEqual(file.name, "test_file")
        self.assertEqual(file.content, "")
        self.assertEqual(file.size, 0)

    def test_write_content(self):
        """Test writing content to the file"""
        file = File("test_file")
        file.write("Hello")
        self.assertEqual(file.content, "Hello")
        self.assertEqual(file.size, 5)

    def test_append_content(self):
        """Test appending content to the file"""
        file = File("test_file")
        file.write("Hello")
        file.append(" World")
        self.assertEqual(file.content, "Hello World")
        self.assertEqual(file.size, 11)

    def test_mtime_updates_on_write(self):
        """Test that modifying content updates the modification time"""
        file = File("test_file")
        initial_mtime = file.mtime
        time.sleep(0.01)
        file.write("Updated Content")
        self.assertGreater(file.mtime, initial_mtime)

    def test_mtime_updates_on_append(self):
        """Test that appending updates the modification time"""
        file = File("test_file")
        initial_mtime = file.mtime
        time.sleep(0.01)
        file.append("More data")
        self.assertGreater(file.mtime, initial_mtime)





if __name__ == "__main__":
    unittest.main()
