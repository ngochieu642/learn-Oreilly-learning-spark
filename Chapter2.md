# Getting Started with Spark

## Spark Core Concepts

### Spark components

- Spark Core
  - Contains the basic functionality of Spark
  - Task scheduling, memory management, fault recovery, interacting with storage systems, ...
  - Home to API that defines _Resilient distributed data-sets_ (RDDs), which are Spark's main programming abstraction
  - RDDs represents a collection of items distributed across many compute nodes that can be manipulated in parallel
- Spark SQL
- Spark Streaming
- MLib
- GraphX
- Cluster Managers

### High level overview

- Every Spark application consists of a _driver program_, this launches various parallel operations on a cluster.
- _driver program_ contains application's main function and defines distributed datasets on the cluster, then applies operations to them.
- Driver programs access Spark through **SparkContext** object, which represents a connection to a computing cluster.
- In the shell, SparkContext is automatically created as the variable **sc**
- SparkContext can be used to build RDDs
- Driver programs manage a number of nodes called _executors_, which can be used to analyze data in parallel
- Spark automatically takes your function and ships it to executor nodes. We can write code in a single driver program and automatically have parts of it run on multiple nodes

## Standalone Applications

- You need to initialize your own SparkContext. After that, the API is the same
- In Python, write applications as Python scripts, and run them using the `bin/spark-submit` script included in Spark
