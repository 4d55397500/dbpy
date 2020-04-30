# db.py
"""
 reference database with binary search tree indices
 implementation
"""
import random
import string
import logging
import time

NCOLUMNS = 5
NROWS = 10**3

# for debugging
logging.info = print
#logging.debug = print
#logging.error = print


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

    def find(self, value):
        if self.value is None:
            return None
        elif self.value == value:
            return self.row
        elif value < self.value:
            return self.left.find(value)
        else:
            return self.right.find(value)

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
        self.indices = []

    def build_indices(self):
        # build indices over specified columns
        logging.info(f'building indices for columns {self.cols}...')
        current = self.database
        indices = [BinarySearchTree() for _ in self.cols]
        while current is not None:
            for j, col in enumerate(self.cols):
                bst = indices[j]
                entry = current.row_value[col]
                bst.add(entry, current)
            current = current.next
        self.indices = indices
        logging.info('finished building indices.')
        # for index in indices:
        # index.print_tree(None, None)

    def lookup(self, col, value):
        logging.debug(f'looking up row containing {value} at column {col} in index')
        if col not in self.cols:
            logging.error(f"an index doesn't exist for column {col}")
            return
        index = self.indices[self.cols.index(col)]
        return index.find(value)


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

    def scan_column(self, column):
        # yield all entries in column
        current = self
        while current is not None:
            yield current.row_value[column]
            current = current.next

    def scan_lookup(self, column, value):
        # lookup by scanning column
        current = self
        while current is not None:
            candidate = current.row_value[column]
            if candidate == value:
                return current
            current = current.next

    def print_db(self):
        current = self
        i = 0
        while current is not None:
            logging.debug(f'(row {i}) | {"|".join(current.row_value)}')
            current = current.next
            i += 1

def fill_sample_database():
    logging.info(f'Writing sample database of {NROWS} rows and {NCOLUMNS} columns...')
    strgen = lambda: ''.join(random.choice(string.ascii_lowercase) for _ in range(15))
    nrows, ncols = NROWS, NCOLUMNS
    database = Database()
    progress = [p/10. + 0.1 for p in range(10)]
    pi = 0
    for i in range(nrows):
        if i / nrows > progress[pi]:
            print(f"Finished writing {progress[pi] * 100}% of database.")
            pi += 1
        for j in range(ncols):
            database.add_entry(i, j, strgen())
    logging.info('finished writing database.')
    #database.print_db()
    return database


def performance_test_index_lookups(database, indices):
        print('running lookup performance test on random column...')
        col = random.choice(indices.cols)
        column_values = database.scan_column(col)

        sl_start = time.process_time()
        for value in column_values:
            database.scan_lookup(col, value)
        sl_end = time.process_time()
        sl_elapsed = sl_end - sl_start
        print(f'{sl_elapsed}s elapsed for scan lookup of rows for all values in column {col}.')

        column_values = database.scan_column(col)
        il_start = time.process_time()
        for value in column_values:
            indices.lookup(col, value)
        il_end = time.process_time()
        il_elapsed = il_end - il_start
        print(f'{il_elapsed}s elapsed for indices lookup of rows for all values in column {col}')
        speedup = sl_elapsed / il_elapsed
        print(f'index lookup was {speedup} times faster than a scan lookup')


def main():
    database = fill_sample_database()
    indices = Indices(database, cols=[0, 2])
    indices.build_indices()
    performance_test_index_lookups(database, indices)


if __name__ == "__main__":
    main()
