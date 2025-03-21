from __future__ import annotations
from itertools import count

from file_system import INDENT_STR

class _LinkedListNode:
    __ids = count(1)
    """
    Node in a linked list
    """    
    def __init__(self, data: any, prev: _LinkedListNode=None):
        """
        Constructs a linked list node

        Args:
            data (any): the data to be stored in the node
            prev (LinkedListNode, optional): The previous node in the list. Defaults to None.
        """ 
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
    
    def __bfs(self):
        pass

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def reversed(self):
        current = self.tail
        while current:
            yield current.data
            current = current.prev

    def enumrate(self):
        """
        Special enumration method for linked list

        Yields:
            (bool, any): tuple. first return is True for the last node
        """
        current = self.head
        if current is None:
            return
        while current.next:
            yield False, current.data
            current = current.next
        yield True, current.data

    def find(self, value: any, key=lambda x: x) -> _LinkedListNode | None:
        """
        Traverse each node, find node with data = value (or data.key = value if given)

        Args:
            value (any): the value to be matched against.
            key (callable, optional): function to extract comparison key from data. Defaults to identity.

        Returns:
            _LinkedListNode: The node found or None
        """        
        current = self.head
        while current:
            if key(current.data) == value:
                return current
            current = current.next

    def append(self, *data: any) -> int:
        """
        Adds node for each argument in *data to the end of the list

        Returns:
            int: new length of list
        """          
        new_node = None
        for datum in data:
            new_node = _LinkedListNode(datum, prev=self.tail)
            if self.head is None:
                # first append to list will go here
                self.head = new_node
            
            self.tail = new_node
            self.length += 1

        return len(self)



    def remove(self, value: any, key=lambda x: x):
        node = self.find(value, key=key)
        if node is None:
            return None
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
    
    def list(self, indent=0, formatter=lambda x: str(x)):
        """
        Lists the contents of the linked list with optional indentation and formatting.

        Args:
            indent (int): The indentation level for each item.
            formatter (callable): A lambda function to format each item's string representation.

        Returns:
            str: A formatted string representation of the linked list.
        """
        current = self.head
        buffer = ""
        while current:
            buffer += f"{INDENT_STR(indent)}{formatter(current.data)}\r\n"
            current = current.next
        return buffer.lstrip()
    

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