import unittest
from src.file_system.linked_list.linked_list import LinkedList

class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.list = LinkedList(1, 2, 3, 'hello world')

    def test_list(self):
        list = self.list
        self.assertEqual(list.length, 4)

    def test_find(self):
        list = self.list
        self.assertIsNotNone(list.find('hello world'))
        self.assertIsNotNone(list.find(2))
        self.assertIsNone(list.find('hello'))
        self.assertIsNone(list.find('3'))

    def test_remove(self):
        list = self.list
        self.assertIsNotNone(list.remove(2))
        self.assertEqual(len(list), 3)
        self.assertIsNone(list.remove(5))
        self.assertIsNotNone(list.remove(1))
        self.assertIsNotNone(list.remove(3))
        self.assertIsNotNone(list.remove('hello world'))
        self.assertEqual(len(list), 0)

    def test_append(self):
        list = self.list
        self.assertEqual(5, list.append('124'))
        self.assertEqual(8, list.append(4, 3, 'test'))
        print(list.list())