import random
import unittest
from src.file_system.directory import Directory
from src.file_system.file import File
from src.file_system.constants import ROOT, PATH_DELIMITER

class TestDirectoryBig(unittest.TestCase):
    def setUp(self):
        # Start with a root directory for each test.
        self.root = Directory(ROOT)

    def test_add_many_children(self):
        """Test adding a large number of children (files) to the root directory."""
        num_children = 1000
        for i in range(num_children):
            f = File(f"file_{i}")
            self.root.add_child(f)
        self.assertEqual(self.root.children.length, num_children)
        
        # Check a middle file exists.
        mid_file = self.root.find_child("file_500")
        self.assertIsNotNone(mid_file)
        self.assertEqual(mid_file.name, "file_500")

    def test_remove_many_children(self):
        """Test removing children after adding many files."""
        num_children = 1000
        for i in range(num_children):
            self.root.add_child(File(f"file_{i}"))
        self.assertEqual(self.root.children.length, num_children)
        
        # Remove every 10th file.
        removed = 0
        for i in range(0, num_children, 10):
            self.assertTrue(self.root.remove_child(f"file_{i}"))
            removed += 1
        
        self.assertEqual(self.root.children.length, num_children - removed)

    def test_deep_nesting(self):
        """Test a deeply nested directory structure."""
        depth = 1000
        current_dir = self.root
        for i in range(depth):
            new_dir = Directory(f"dir_{i}")
            current_dir.add_child(new_dir)
            current_dir = new_dir
        
        abs_path = current_dir.get_absolute_path()
        # Expect components: root plus 'depth' directories.
        self.assertEqual(len(abs_path.split(PATH_DELIMITER)), depth + 1)

    def test_list_output_format(self):
        """Test that the tree-formatted output is correct."""
        # Build a simple hierarchy.
        sub_dir = Directory("sub")
        file1 = File("foo")
        file2 = File("bar")
        file3 = File("baz")
        self.root.add_child(file1)
        self.root.add_child(sub_dir)
        self.root.add_child(file3)
        sub_dir.add_child(file2)
        
        output = self.root.list(recurse=True)
        # Check for proper tree branch characters.
        self.assertIn("├──", output)
        self.assertIn("└──", output)
        self.assertTrue(output.startswith(ROOT))
        print("\nTree listing output:\n", output)

    def test_random_structure(self):
        """
        Build a random directory structure where each new file or directory is added 
        to a randomly chosen directory from a pool, simulating diverse structures.
        """
        pool = [self.root]  # Start with root in our pool.
        file_count = 0
        dir_count = 1   # Count root as one directory.
        num_operations = 200  # Total additions
        
        for i in range(num_operations):
            # 50% chance for a file, 50% for a directory.
            if random.random() < 0.5:
                new_file = File(f"file_{file_count}")
                file_count += 1
                parent = random.choice(pool)
                parent.add_child(new_file)
            else:
                new_dir = Directory(f"dir_{dir_count}")
                dir_count += 1
                parent = random.choice(pool)
                parent.add_child(new_dir)
                pool.append(new_dir)
        
        # Print the tree for visual inspection.
        output = self.root.list(recurse=True)
        print("\nRandom tree listing output:\n", output)
        
        # Verify that total nodes count in the tree equals the sum of added files and directories (excluding root).
        total_nodes = 0
        def traverse(directory: Directory):
            nonlocal total_nodes
            for _, child in directory.children.enumrate():
                total_nodes += 1
                if hasattr(child, "children"):
                    traverse(child)
        traverse(self.root)
        self.assertEqual(total_nodes, file_count + (dir_count - 1))

if __name__ == '__main__':
    unittest.main()
