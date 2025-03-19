from file_system.node import FSNode
from file_system.file import File

class LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = LinkedListNode(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def find(self, name):
        current = self.head
        while current:
            if current.data.name == name:
                return current.data
            current = current.next
        return None
    
    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

class Directory(FSNode):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.children = LinkedList()

    def add_child(self, node):
        if self.children.find(node.name) is None:
            self.children.append(node)
            node.parent = self
            return True
        return False
    
    def get_child(self, name):
        return self.children.find(name)