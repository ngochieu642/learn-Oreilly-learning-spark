# Chapter 7: Running on a Cluster

- Explains runtime architecture of a distributed Spark application
- Discusses options for running Spark in distributed clusters (Hadoop YARN, Apache Meso, Spark's standalone cluster manager) in both on-premise and cloud deployments

## 1. Spark runtime architecture

- In distributed mode, Spark uses a master/slave architecture with one central coordinator and many distributed worker
- The central coordinator is called the driver.
- The driver communicates with a potentially large number of distributed workers called executors
- A driver and it executors are together termed a Spark application
- A Spark application is launched on a set of machines using an external service called a _cluster manager_

### The driver

- This is the process where the `main()` method runs.
- Create SparkContext, RDDs, performs transformations and actions
- Perform 2 duties:

  - converting a user program into units of physical execution called _tasks_

    - Tasks are the smallest unit of work in Spark
    - tasks are bundled up and prepared to be sent to the cluster
    - Spark creates a _logical directed acyclic graph_ (DAG), then it convert this logical graph into execution graph, then fro execution graph into a set of stages. Each stages consist of multiple tasks.

  - Scheduling tasks on executors:
    - when executors are started, they register themselves with the driver
    - Each executor represents a process capable of running tasks and storing RDD data
    - The driver will look at the current set of executors and try to schedule each task in an appropriate location, based on data placement.
    - The driver exposes information about the running Spark application through a web interface, which by default is available at port 4040.

### Executors

- launched once at the beginning of a Spark application and typically run for the entire lifetime
- Have 2 roles:
  - Run the tasks that make up the application and return results to the driver.
  - provide in-memory storage for RDDs that are cached by user programs

### Cluster Manager

- A pluggable component in Spark
- _driver_ and _executor_ when refer to the processes that execute each Spark application
- _master_ and _worker_ used to describe the centralized and distributed portions of the cluster

### Launching a Program

1. User submit an application using `spark-submit`
2. `spark-submit` launches the driver program and invokes the `main()` method specified by the user
3. The driver program contacts the cluster manager to ask for resources to launch clusters
4. The cluster manager launchs executors on behalf of the driver program
5. The driver process run through the user's application. Base on the RDD actions and transformations in the program, the driver sends work to executors in the form of tasks
6. tasks are run on executor processes to compute and save result
7. If the driver's `main()` method exits or it calls `SparkContext.stop()`, it will terminate the executors and release resources from the cluster manager

## 2. Deploying Applications with spark-submit

- When submit this without any extra flag, it runs the supplied Spark program locally
- Provide extra flags with the address of a Standalone cluster and a specific size of each executor process we'd like to launch

```bash
bin/spark-submit --master spark://host:7077 --executor-memory 10g my_script.py
```

- Possible values for the --master flag in spark-submit

  - `spark://host:port`: Connection a Spark standalone cluster at the specified port. Default port 7077
  - `mesos://host:port`: Connect to a mesos cluster. Default port 5050
    `yarn`: Connect to a YARN cluster. When running on YARN, you will need to set the HADOOP_CONFIG_DIR environment variable to point the location of your Hadoop configuration directory, which contains information about the cluster
  - `local`: Run in local mode with a single core
  - `local[N]`: Run in local mode with N cores
  - `local[*]`: Run in local mode and use as many cores as the machine has

- `spark-submit` provides a variety of options that let you control specific details about a particular run of your application. There are two categories:
  1. Scheduling information:
  - Such as the amount of resources you'd like to request for your job
  2. Information about the runtime dependencies of your application, such as libraries or files you want to deploy to all worker machinesI

```bash
bin/spark-submit [options] <app jar | python file> [app options]
```

- Common flags for spark-submit
  - `--master`: Indicates the cluster manager to connect to.
  - `--deploy-mode`: Whether to launch the program locally("client") or one of the worker inside the cluster. In client mode, `spark-submit` wil run your driver on the same machine
    where `spark-submit` is itself being invoked. In cluster mode, the driver will be shipped to execute on a worker node in the cluster. Default mode is client
  - `--class`: Main class (if use Java or Scala)
  - `--name`: human-readable name for your application. Will be displayed in Spark's web UI
  - `--jars`: A list of JAR files to upload and place on the classpath of your application. If your applications depends on a small number of third-party JARS, you can add them here
  - `--files`: A list of files to ve place in the working directory of your application.
    This can be used for data files that you want to distribute to each node
  - `--py-files`: A list of files to be added to the PYTHONPATH of your application
  - `--executor-memory`: The amount of memory to use for executors.Suffixes used to specify larger quantities "512m" or "15g"
  - `--driver-memory`: Amount of memory to use for the driver process

## 3. Packing Your Code and Dependencies

- If your program import any libraries that are not in the `org.apache.spark` package or part of the language library, you need to ensure that all your dependencies are present at the runtime of your Spark applications

**Python**

- PySpark uses the existing Python installation in worker machines, you can install dependency libraries using directly on the worker machine using standard Python package managers (pip), or via manual installation into the `site-packages` directory of your Python installation

**Java | Scala**

- Rely on a build tool to produce a single JAR containing the entire transitive dependency graph of an application.
- Most popular build tools for Java and Scala are Maven and sbt (scala build tool)

## 4. Scheduling Within and Between Spark Applications

- Scheduling policies help ensure that resources are not overwhelmed and allow for prioritization of workloads.
- Spark primarily relies on the cluster manager to share resources between applications.

## 5. Cluster Manager

### Standalone Cluster Manager

**Launching the Standalone cluster manager**

- Starting a master and workers by hand, or by using launch scripts in Sparks' _sbin_ directory

- Process

1. Copy a compiled version of Spark to the `same location` on all your machines, for example `home/yourname/spark`
2. Set up password-less SSH access from your master machine to the others. This requires having the same `user account` on all machines, creating a private SSH key for it on the master via ssh-keygen, and adding this key to `.ssh/authorized_keys` file for all the workers.

```bash
ssh-keygen -t dsa
cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys
chmod 644 ~/.ssh/authorized_keys
```

3. Edit `conf/slaves` file on your master and dill in the workers' hostnames
4. To start the cluster, run `sbin/start-all.sh` on you master

### Which Cluster Manager to use

- Standalone cluster is the easiest to set up and will provide all the same features as the other if you are running only Spark

- YARN is likely to be preinstalled in many Hadoop distributions
- Mesos allow interactive applications such as the Spark shell scale down their CPU allocation between commands -> Suitable for environments where multiple users are unning interactive shells
- It is best to run Spark on the same nodes as HDFS for fast access to storage
