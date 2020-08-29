# dbpy

Reference implementation of a simple database and indices model with the database as a linked list and indices as (unbalanced) binary search trees (both in memory).


```
writing sample database of 1000 rows and 5 columns...
finished writing database.
building indices for columns [0, 2]...
finished building indices.
running lookup performance test on random column...
0.10063699999999998s elapsed for scan lookup of rows for all values in column 0.
0.00814999999999999s elapsed for indices lookup of rows for all values in column 0
index lookup was 12.348098159509213 times faster than a scan lookup
```
