# Chapter 3: Programming with RDDs

## RDD Basics

- RDD is an immutable distributed collection of objects
- Each RDD is split into multi _partitions_, which may be computed on different nodes of the cluster
- RDDs can contain any type of Python, Java, Scala objects, including user-defined classes
- 2 ways to create RDDs in driver program:
  - Loading an external dataset
  - Distributing a collection of objects (parallelizing a collection in your driver program)
- RDDs offer two types of operations: _transformation_ and _actions_
  - Transformations construct a new RDD from a previous one (_filter_ method)
  - Actions, computed a result based on a RDD, then return it to the driver program or save to an external storage system (HDFS, etc) (_first_ method)
- Spark computes RDDs in _lazy fashion_ - the first time they are used in an action.
- RDDs are (by default) recomputed each time you run an action on them.
- To reuse RDD, you can ask Spark to _persist_ using `RDD.persist()`. We can ask Spark to persist our data in a number of different places. After computing it the first time, Spark will store the RDD contents in memory (partitioned across the machines in your cluster), and reuse them in future actions.
- It is possible to persist RDDs on disk instead of memory.

### Summarize: Workflow of every Spark program and shell session

1. Create some input RDDs from external data
2. Transform them to define new RDDs using transformations
3. Ask Spark to persist() any RDDs that will need to be reused
4. Launch actions to kick off parallel computation

### Notes

- `cache()` is the same as calling `persist()` with the default storage level

## Creating RDDs

- Simplest way: take an existing collection and pass it to SparkContent's `parallelize()` method. This approach is useful when learning Spark. However, it is not widely used since it requires that you have entire dataset in memory in one machine
- A common way: load data from external storage.

## RDD Operations

- 2 types: _transformations_ and _actions_
- _transformations_ return RDDs, _actions_ return some other data type

### Transformations

- transformations doest not mutate the existing RDD. It returns a pointer to an entirely new RDD
- Spark keeps tracks of the set of dependencies between different RDDs, call the _lineage graph_. It uses this information to compute each RDD on demand and to recover lost data if part of a persistent RDD is lost.

### Actions

- Actions are operations that return a final value to the driver program or write data to an external storage.
- Some method:
  - `take()`: retrieve a small number of elements in RDD.
  - `collect()`: return the entire RDD. Your entire dataset must fit in memory on a single machine to use `collect()
  - saveAsTextFile()
  - saveAsSequenceFile()
- Each time we call a new action, the entire RDD must be computed from scratch. To avoid this inefficiency, users can _persist_ intermediate results

### Lazy Evaluation

- Happens when call a transformation on an RDD, the data is not loaded until it is necessary.
- Force Spark to execute transformations by running an action.
- No benefit to writing a single complex map instead of chaining together many simple operations.

## Passing Functions to Spark

### Python

- `DON'T DO THIS`: pass a function that is the member of an object, or contains references to fields in an object, Spark sends the entire object to worker nodes, which can be much larger than the bit of information you need. Instead, just extract the fields you need into a local variable and pass that in

```Python
class WordFunctions(object):
  def getMatchesNoReference(self, rdd):
    # DO THIS
    query = self.query
    return rdd.filter(lambda x: query in x)

  def isMatch(self, s):
    return self.query in s

  def getMatchesFunctionReference(self, rdd):
    # DON'T DO THIS
    return rdd.filter(self.isMatch)

  def getMatchesMemberReference(self, rdd):
    # DON'T DO THIS
    return rdd.filter(lambda x: self.query in x)
```

### Scala

- Didn't have time for this

### Java

- Didn't have time for this

## Common _Transformations_ and _Actions_

### Basic RDDs

#### 1. Element-wise transformations

- `map()`: Return type does not have to be the same as its input type
- `flatMap()`: Produce multiple output elements for each input element. The function we provide to `flatMap()` is called individually for each element in our input RDD. Instead of returning a single element, we return an iterator with our return values. Simple usage: Splitting up an input string into words
- `filter()`

#### 2. Pseudo set operations

- Requires the RDDs being operated on are of the same type
- `distinct()`: Unique elements. This operation is expensive
- `union()`: Returns the data from both source. Simple
- `intersection()`: Returns elements in both RDDs. Requires a shuffle over the network to identify common elements (Worse than `distinct`)
- `subtract()`: Takes in another RDD and returns an RDD that has only value present in the first RDD and not the second RDD. Like `intersection()`, it performs a shuffle
- `cartesian()`: Returns all possible pairs of (a,b) where a from source RDD, b from the other RDD. Very expensive for large RDDs

#### 3. Action

- Return type be the same type as that of the elements in the RDD we are operating over
  - `reduce()`: Like JS reduce
  - `fold()`: Like reduce but takes a "zero value" for initial call on each partition
- `aggregate()`:
