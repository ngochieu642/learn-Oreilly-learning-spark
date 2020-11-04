# Chapter 4: Working with Key/Value Pairs

- Spark provides special operations on RDDs containing key/value pairs. These RDDs are called pair RDDs.
- Pair RDD are useful building block in many program

## Creating Pair RDDs

- From regular RDD: Use `map()`
- In Python, we need to return ad RDD composed of tuples

## Transformation on Pair RDDs

- Transformation on one pair RDD
  - `reduceByKey()`
  - `groupByKey()`
  - `combineByKey()`
  - `mapValues()`
  - `flatMapValues()`
  - `keys()`
  - `values()`
  - `sortByKey()`
- Transformation on two pair RDDs
  - `subtractByKey()`
  - `join()`
  - `rightOuterJoin()`
  - `leftOuterJoin()`
  - `cogroup()`

### Aggregations

- Every RDD has a fixed number of _partitions_ that determine the degree of parallelism to use when executing operations on the RDD
- When performing aggregations or grouping operations, we can ask Spark to use a specific number of partitions.
- If we want to change the partitioning of an RDD outside the context of grouping and aggregation operations, we can use `repartition()` function, which shuffles the data across the network to create a new set of partitions.
- Repartitioning is a fairly expensive operation.

### Grouping data

- `groupBy()`, `groupByKey()`
- Group data sharing the same key from multiple RDDs using `cogroup()`

### Joins

- `join()` operator is an inner join - Only keys that are represent in both pair RDDs are output

### Sorting data

- `sortByKey()` takes a parameter called `ascending` indicating whether we want it in ascending order.
- Sometimes we want a different sort order

## Data partitioning (Advanced)

- Partitioning will not be helpful in all applications, it is useful only when a dataset is reused _multiple times_ in key-oriented operations such as joins
- In Python , you can not pass a Hash Partitioner Object, instead, you just pass the number of partitions desired

### Operations that Benefit from Partitioning

- All operations that involve shuffling data by key across the network
- Some method:
  - `cogroup()`
  - `groupWith()`
  - `join()`
  - `leftOuterJoin()`
  - `rightOuterJoin()`
  - `groupByKey()`
  - `reduceByKey()`
  - `combineByKey()`
  - `lookup()`

### Operations that affect Partitioning

- here are all the operations that result in a partitioner being set on the output RDD
  - `cogroup()`
  - `groupWith()`
  - `join`
  - `leftOuterJoin()`
  - `rightOuterJoin()`
  - `groupByKey()`
  - `reduceByKey()`
  - `combineByKey()`
  - `partitionBy()`
  - `sort()`
  - `mapValues()`

## Custom Partitioners

- Help reduce communication by taking advantage of domain-specific knowledge
- To implement a custom partitioner in Python, pass a hash function as an additional argument to `RDD.partitionBy()`
- The hash function you pass will be compared by identity to that of other RDDs. If you want to partition multiple RDDs with the same partitioner, pass the same function object instead of creating a new lambda for each one.
