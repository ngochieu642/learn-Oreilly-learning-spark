# Chapter 5: Loading & Saving data

- Set of data sources:
  1. File formats and filesystems:
  - For data stored in a local or distributed filesystem, such as NFS, HDFS, S3. Spark can access a variety of file formats including text, JSON, SequenceFiles, protocol buffers
  2. Structured data sources through Spark SQL
  - JSON & Apache Hive
  3. Databases and key/value stores
  - Connecting to Cassandra, HBase, Elasticsearch, JDBC databases

## 1. File Formats

- Common supported file formats:
  - Text file:
    - No Structured
    - Plain text files. Records are assumed to be one per line
  - JSON
    - Semi Structured
    - Most libraries require one record per line
  - CSV
    - Structured
  - SequenceFiles
    - Structured
    - A common Hadoop file format used for key/value data
  - Protocol buffers:
    - Structured
    - Fast, space-efficient multilanguage format
  - Object files
    - Structured
    - Useful for saving data from a Spark job to be consumed by shared code. Breaks if you change your classes, as it relies on java Serialization

### Text files

- Loading text files

```python
input = sc.textFile('./path/to/file.txt')
```

- Saving text files

```python
result.saveAsTextFile(outputFile)
```

### JSON

- Simplest way: Load as text then mapping over the values with a JSON parser
- Other way: Use preferred JSON serialization library to write out the value to string

**Loading JSON**

- Loading the data as text file and then parsing the JSON data is an approach that we can use in all supported languages. Assume that you have one JSON record per row
- If constructing JSON is expensive in language, use `mapPartitions()` to reuse the parser
- If you want to track the number of errors coming from malformed input, look at `accumulator()`

**Saving JSON**

- Simpler compared to loading it

### CSV

- Common Practice: make the first row's column values the names of each field

**Loading CSV**

- If CSV data does not contain newlines in any of the fields, you can load as text and parse it
- If there are embedded new lines, load each file in full and parse the entire segment. This can introduce bottlenecks in loading and parsing

**Saving CSV**

- To have a consistent output, we need to create a mapping

### SequenceFiles

- This is a popular Hadoop format composed of flat files with key/value pairs.
- SequenceFiles have sync markers that allow Spark to seek to a point in the file and then resynchronize with the record boundaries. This allows Spark to read SequenceFiles in parallel from multiple nodes.

**Loading SequenceFiles**

```python
sc.sequenceFile(inFile)
```

**Saving SequenceFiles**

### Object files

- Object files are a deceptively simple wrapper around SequenceFiles that allows us to save RDDs containing just values. With Object file, the values are written out using java serialization.

**Save object file**

- `saveAsObjectFile()`

**Loading object file**

- `objectFile()`

- Require almost no work to save almost arbitrary objects.
- Not available in Python -> Use `saveAsPickleFile()` and `pickleFile()` instead. These use Python pickle serialization library.

### Hadoop input and output format

## File Compression

## 2. Filesystems

### Local FS

### AWS S3

- Set up environment variables:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
- Pass a path `s3n://bucket/path-within-bucket`

### HDFS

- Hadoop distributed file system -> Spark works well
- Work on commodity hardware, resilient to node failure, high data throughput
- Spark and HDFS can be collocated on the same machines, Spark can take advantage of this data locality to avoid network overhead
- `hdfs://master:port/path`

## 3. Structured Data with Spark SQL

- Data has a schema (consistent fields across data records)
- We give Spark SQL a SQL Query to run on the data source, get back an RDD of Row objects, one per record

### Apache Hive

- Hive can store tables in variety of formats, from plain text to column-oriented formats, inside HDFS or other storage system.

### JSON

## 4.Database

### Java Database Connectivity

- Download JBDC connector (.jar file) at MySQL, dig into `debian-file/data.tar.xz/usr/share/java`

```python
from pyspark.sql import HiveContext
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

hiveCtx = HiveContext(sc)

dataframe_mysql = hiveCtx.read.format("jdbc") \
    .option("url", "jdbc:mysql://192.168.1.36:33060") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "sipiot.DeviceLog") \
    .option("user", "sip") \
    .option("password", "1234") \
    .load()

dataframe_mysql.show()
```

- Run the following program with jar file

```bash
bin/spark-submit --jars /code/src/mysql-connector-java-8.0.21.jar /code/src/jdbc-maria.py
```

### Cassandra

### HBase

### Elasticsearch
