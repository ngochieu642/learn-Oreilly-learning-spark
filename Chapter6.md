# Chapter 6: Advanced Spark Programming

- Shared variables: _accumulators_ (aggregate information) + _broadcast variables_ (efficiently distribute large values)
- Batch operations: Tasks with high setup costs, like querying a database

## 1. Accumulators

- Accumulators is of type shared variable.
- It provides a simple syntax for aggregating values from worker nodes back to the driver program
- Common uses: Count events that occur during job execution for debugging purpose.
- Accumulators work as follows:
  - We create them in the driver by calling `SparkContext.accumulator(initialValue)` method, which produces an accumulator holding an initial value
  - Worker code in Spark closures can add to the accumulator with its += method
  - The driver program can call the `value` property on the accumulator to access its value
- Tasks on worker nodes can not access the accumulator's value()

## Broadcast variables

- Is of type shared variable
- Allows the program to send a large, read-only value to all the worker nodes for use in one or more Spark's pera
- The process of using broadcast
  1. Create a `Broadcast[T]` by calling `SparkContext.broadcast` on an object of type T.
  2. Access its value with the `value` property
  3. The variable will be sent to each node only once, and should be treated as read-only
- The easiest way to satisfy the read-only requirements is to broadcast a primitive value or a reference to an immutable object

### Optimizing Broadcast

- When broadcasting large values, it is important to choose a data serialization format that is fast and compact
- In particular, Java Serialization can be very inefficient for anything except arrays of primitive types
- An alternative is _Kyro_

## Working on a Per-Partition Basis

- Allow us to avoid redoing setup work for each data item.
- Operations like opening a database connection or creating a random number generator are examples of setup steps that we wish to avoid doing for each element
- Spark has _per-partition_ version of `map` and `foreach` to help reduce the cost of these operations by letting your run code only once for each partition of an RDD