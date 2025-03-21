import unittest
import random
from src.file_system.constants import ROOT
from src.file_system.filesystem import FileSystem

class TestFileSystem(unittest.TestCase):

    def setUp(self):
        self.fs = FileSystem()

    def test_mkdir_and_cd(self):
        # Create a random directory structure
        dir_names = [f"dir_{i}" for i in range(5)]
        for dir_name in dir_names:
            self.fs.mkdir(dir_name)
            self.assertIn(dir_name, self.fs.ls(recurse=True))

        # Navigate into each directory
        for dir_name in dir_names:
            self.assertTrue(self.fs.cd(dir_name))
            self.assertEqual(self.fs.current.name, dir_name)
            self.assertTrue(self.fs.cd('..'))  # Navigate back to root

    def test_touch_and_ls(self):
        # Create random files in the root directory
        file_names = [f"file_{i}.txt" for i in range(5)]
        for file_name in file_names:
            self.fs.touch(file_name)
            self.assertIn(file_name, self.fs.ls())

    def test_nested_directories_and_files(self):
        # Create a nested directory structure with files
        self.fs.mkdir('parent_dir')
        self.fs.cd('parent_dir')
        sub_dirs = [f"sub_dir_{i}" for i in range(3)]
        for sub_dir in sub_dirs:
            self.fs.mkdir(sub_dir)
            self.fs.cd(sub_dir)
            # Create random files in each subdirectory
            for j in range(2):
                file_name = f"file_{j}.txt"
                self.fs.touch(file_name)
                self.assertIn(file_name, self.fs.ls())
            self.fs.cd('..')
        self.fs.cd('..')  # Return to root

    def test_random_navigation(self):
        # Create a complex directory structure
        structure = {
            'dir_a': ['file_a1.txt', 'file_a2.txt'],
            'dir_b': {
                'sub_dir_b1': ['file_b1_1.txt'],
                'sub_dir_b2': []
            },
            'dir_c': []
        }

        def create_structure(base, struct):
            for name, content in struct.items():
                if isinstance(content, list):
                    base.mkdir(name)
                    base.cd(name)
                    for file_name in content:
                        base.touch(file_name)
                    base.cd('..')
                elif isinstance(content, dict):
                    base.mkdir(name)
                    base.cd(name)
                    create_structure(base, content)
                    base.cd('..')

        create_structure(self.fs, structure)

        

        # Randomly navigate the structure
        all_dirs = ['~', '~/dir_a', '~/dir_b', '~/dir_b/sub_dir_b1', '~/dir_b/sub_dir_b2', '~/dir_c']
        for _ in range(10):
            path = random.choice(all_dirs)
            self.assertTrue(self.fs.cd(path))
            self.assertEqual(self.fs.current.name, path.split('/')[-1] if path != '~' else ROOT)

if __name__ == '__main__':
    unittest.main()
