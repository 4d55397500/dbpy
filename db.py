# db.py
"""
 reference database with binary search tree indices
 implementation
"""
import random
import string
import logging

NCOLUMNS = 5
NROWS = 10**2

# for debugging
logging.info = print
logging.debug = print


class BinarySearchTree(object):
    def __init__(self):
        self.value = None
        self.row = None
        self.left = None
        self.right = None

    def add(self, value, row):
        if self.value is None:
            self.value = value
            self.row = row
            self.left = BinarySearchTree()
            self.right = BinarySearchTree()
        elif value < self.value:
            self.left.add(value, row)
        else:
            self.right.add(value, row)

    def print_tree(self, parent, is_left):
        # breadth-first print
        if self.value is not None:
            if is_left:
                logging.debug(f'{self.value}, left child of {parent}. rowptr to {self.row}')
                assert parent is None or self.value < parent
            else:
                logging.debug(f'{self.value}, right child of {parent}. rowptr to {self.row}')
                assert parent is None or self.value > parent
            self.left.print_tree(self.value, True)
            self.right.print_tree(self.value, False)


class Indices(object):
    def __init__(self, database, cols):
        self.database = database
        self.cols = cols
    def build_indices(self):
        # build indices over specified columns
        logging.info('building indices ...')
        current = self.database
        indices = [BinarySearchTree() for _ in self.cols]
        while current is not None:
            for j, col in enumerate(self.cols):
                bst = indices[j]
                entry = current.row_value[col]
                bst.add(entry, current)
            current = current.next
        logging.info('finished building indices.')
        # for index in indices:
        # index.print_tree(None, None)


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
            logging.debug(f'(row {i}) | {"|".join(current.row_value)}')
            current = current.next
            i += 1


def fill_sample_database():
    logging.info(f'writing sample database of {NROWS} rows and {NCOLUMNS} columns...')
    strgen = lambda: ''.join(random.choice(string.ascii_lowercase) for _ in range(15))
    nrows, ncols = NROWS, NCOLUMNS
    database = Database()
    for i in range(nrows):
        for j in range(ncols):
            database.add_entry(i, j, strgen())
    logging.info('finished writing database.')
    #database.print_db()
    return database


def main():
    database = fill_sample_database()
    indices = Indices(database, cols=[0, 2])
    indices.build_indices()


if __name__ == "__main__":
    main()
