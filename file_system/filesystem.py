from file_system.directory import Directory
from file_system.file import File


class FileSystem:
    def __init__(self):
        self.root = Directory("Root")
        self.current = self.root

    def ls(self):
        output = []
        for node in self.current.children:
            output.append(node.name)
        return output
    
    def mkdir(self, dirname):
        if self.current.get_child(dirname) is None:
            new_dir = Directory(dirname)
            self.current.add_child(new_dir)
            return f"directory {dirname} created"
        return f"directory {dirname} already exists"
    
    def touch(self, filename):
        if self.current.get_child(filename) is None:
            new_file = File(filename)
            self.current.add_child(new_file)
            return f"file {filename} created"
        return f"file {filename} already exists"
    
    def cd(self, dirname):
        if dirname == '..':
            if self.current.parent is not None:
                self.current = self.current.parent
                return True
            return False
        else:
            child = self.get_child(dirname)
            if child and isinstance(child, Directory):
                self.current = child
                return True
            return False
            