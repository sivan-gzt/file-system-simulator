from __future__ import annotations
from itertools import count

from ..file_system.exceptions import DuplicateNameError
from ..file_system.constants import INDENT_STR, PATH_DELIMITER, ROOT
from ..file_system.node import FSNode
from ..file_system.file import File

class LinkedListNode:
    __ids = count(1)
    """
    Node in a linked list
    """    
    def __init__(self, data: any, prev: LinkedListNode=None, id_key: str='name'):
        """
        Constructs a linked list node

        Args:
            data (any): the data to be stored in the node
            prev (LinkedListNode, optional): The previous node in the list. Defaults to None.
            id_key (str, optional): One of data's attributes, will be used to name the node and perform lookup. Defaults to 'name'.
        """        
        self.name = getattr(data, id_key)
        self.__id = next(self.__ids)
        self.data = data
        self.next = None
        self.prev = prev
        if prev:
            prev.next = self
    
    def last(self):
        """
        Get the last node linked to self, or self if it is the last

        Returns:
            LinkedListNode: The last node in the chain
        """        
        current = self
        while current.next:
            current = current.next
        return current
    
    def get_id(self):
        return self.__id

class LinkedList:
    def __init__(self, *data: any):
        self.head = None
        self.tail = None
        self.length = 0
        self.append(*data)

    def __len__(self):
        return self.length
    
    def __update_length(self):
        self.length = sum(self.head)
        return len(self)

    def find(self, value: any, key: str='name'):
        if len(self) == 0 or len(value) == 0 or (value is None):
            return self.head
        current = self.head
        while current:
            if getattr(current, key) == value:
                return current
            current = current.next

    def append(self, *data: any) -> True:
        new_node = None
        for datum in data:
            new_node = LinkedListNode(datum, prev=self.tail)
            if self.head is None:
                # first append to list will go here
                self.head = new_node
            
            self.length += 1

        self.tail = new_node
        return True

    def remove(self, vararg: str | LinkedListNode):
        node = None
        if isinstance(vararg, LinkedListNode):
            node = vararg
        elif isinstance(vararg, str):
            node = self.find(vararg)
        
        if node is None:
            return False
        
        self.length -= 1
        
        prev = node.prev
        next = node.next
        if prev is None:
            # removing head
            self.head = next
            if next:
                next.prev = None
            return node
        
        prev.next = next
        if next:
            next.prev = prev
            return node
        
        # removing tail
        self.tail = prev
        return node
        # current = self.head
        # while current:
        #     if current.name == name:
        #         if current.prev is None:
        #             # removing head
        #             self.head = current.next
        #             if self.head:
        #                 self.head.prev = None
        #         else:
        #             # removing not head
        #             current.prev.next = current.next
        #             if current.next:
        #                 current.next.prev = current.prev
        #         return True
        #     current = current.next

        # return False
    
    def list(self, indent=0):
        current = self.head
        buffer = ""
        while current:
            buffer += f"{INDENT_STR(indent)}{str(current.data)}\r\n"
            current = current.next
        return buffer.lstrip()
    
    def __bfs(self):
        pass

    def __iter__(self):
        current = self.head
        # last_valid = None
        while current:
            # if current.data is not None:
                # last_valid = current.data
            yield current.data
            current = current.next

        # if last_valid is not None:
        #     yield last_valid

class Stack(LinkedList):
    def __init__(self, *data: any):
        super().__init__(data)

    def pop(self):
        return self.remove(self.tail)
    
    def add(self, *data: any):
        return self.append(*data)

class Queue(LinkedList):
    def __init__(self, *data: any):
        super().__init__(data)

    def dequeue(self):
        return self.remove(self.head)

    def enqueue(self, *data: any):
        return self.append(*data)


class Directory(FSNode):
    def __init__(self, name: str=ROOT, parent: Directory=None): 
        super().__init__(name, parent)
        self.children = LinkedList()
        self.size     = 0
        self.count    = 0
        
    def __str__(self):
        return super().__str__() + PATH_DELIMITER
    
    def get_child(self, name: str) -> Directory | File:
        child = self.children.find(name)
        if child is None:
            return None
        return child.data

    def add_child(self, *children: Directory | File):
        for child in children:
            exist = self.get_child(child.name)
            if exist is None:
                self.children.append(child)
                child.parent = self
                self.count  += 1
                self.size   += child.size
            else:
                raise DuplicateNameError(child.name, self.name)
    
    def remove_child(self, name: str) -> bool:
        node = self.get_child(name)
        if node is None:
            return False
        self.count -= 1
        self.size -= node.size
        self.children.remove(name)

    def list(self, indent=0, recurse=False):
        buffer = f"{INDENT_STR(indent)}{self.name}{PATH_DELIMITER}\n"
        indent = indent + 1
        for child in self.children:
            if recurse and isinstance(child, Directory):
                buffer += child.list(indent)
            else:
                buffer += f"{INDENT_STR(indent)}{str(child)}\n"

        return buffer

    def get_absolute_path(self):
        if self.parent is None:
            return self.name
        
        return super().get_absolute_path()
    