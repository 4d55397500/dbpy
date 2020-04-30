# db.py
"""
 reference database with binary search tree indices
 implementation
"""
import random
import string

NCOLUMNS = 5
NROWS = 10**2


class Node(object):
    def __init__(self, value, row, left, right):
        self.value = value
        self.row = row
        self.left = left
        self.right = right


class BinarySearchTree(object):

    def __init__(self):
        pass

    def add(self, value):
        pass


class Database(object):

    """ A database modeled as a linked list of rows """

    def __init__(self):
        self.row_value = [None] * NCOLUMNS
        self.next = None

    def add_entry(self, row, column, entry):
        current = self
        i = 0
        while i < row:
            if current.next is None:
                current.next = Database()
            current = current.next
            i += 1
        current.row_value[column] = entry

    def print_db(self):
        current = self
        i = 0
        while current is not None:
            print(f'(row {i}) | {"|".join(current.row_value)}')
            current = current.next
            i += 1


def fill_sample_database():
    strgen = lambda: ''.join(random.choice(string.ascii_lowercase) for _ in range(15))
    nrows, ncols = NROWS, NCOLUMNS
    database = Database()
    for i in range(nrows):
        for j in range(ncols):
            database.add_entry(i, j, strgen())
    database.print_db()


if __name__ == "__main__":
    fill_sample_database()