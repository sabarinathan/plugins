# Cassandra Monitoring
## What is Cassandra?

Apache Cassandra is an open-source, distributed NoSQL database management system that is built to handle large volumes of data. It is highly scalable and fault-tolerant, offering users high performance and low latency.

### Monitor the health and performance of your Cassandra database with our plugin integration:

#### Prerequisites
-  Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you intend to run the plugin

-  Install the jmxquery module for python.
	```
	pip install jmxquery
	```
-  Set up  the jmx port for Cassandra:

    1.  Open the cassandra-env.sh file from the location "/etc/cassandra"
    
    2.  By default JMX security is disabled in cassandra, to enable it locate following lines of code in *cassandra-env.sh* file.
		    
        ```
         if [ "$LOCAL_JMX" = "yes" ]; then
  		   JVM_OPTS="$JVM_OPTS -Dcassandra.jmx.local.port=$JMX_PORT -XX:+DisableExplicitGC"
         ```

    3.  Add the following lines to the else block of the above lines in the cassandra-env.sh file
    
        ```
         JVM_OPTS="$JVM_OPTS -Dcassandra.jmx.remote.login.config=CassandraLogin"'
         JVM_OPTS="$JVM_OPTS -Djava.security.auth.login.config=$CASSANDRA_HOME/conf/cassandra-jaas.config"
         JVM_OPTS="$JVM_OPTS -Dcassandra.jmx.authorizer=org.apache.cassandra.auth.jmx.AuthorizationProxy"
         ```
         

    4. Also, comment out the following lines in the cassandra-env.sh file:
        ```
        JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.password.file=/etc/cassandra/jmxremote.password"
        JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.access.file=/etc/cassandra/jmxremote.access"
        ```

    5.  Change the authentication in the cassandra.yaml file to PasswordAuthenticator:

          ```
          authenticator: PasswordAuthenticator
          ```

    6. Change the authorization in the cassandra.yaml file to CassandraAuthorizer:

          ```
          authorizer: CassandraAuthorizer
          ```


    7.  Restart Cassandra once you are done.

#### Plugin Installation

-  Create a directory named "cassandra_monitoring".
    
-  Download all the files in the "cassandra_monitoring" folder and place it under the "cassandra_monitoring" directory.
    ```
    wget https://raw.githubusercontent.com/site24x7/plugins/master/cassandra_monitoring/cassandra_monitoring.py

    wget https://raw.githubusercontent.com/site24x7/plugins/master/cassandra_monitoring/cassandra_monitoring.cfg
    ```

-  Execute the following command in your server to install jmxquery:
    ```
    pip install jmxquery
    ```

-  Execute the below command with appropriate arguments to check fora valid json output:

    ```
     python3 cassandra_monitoring.py --hostname localhost --port 7199 --logs_enabled False
    ```
    
#### Configurations


-  Provide your Cassandra configurations in the cassandra_monitoring.cfg file.
  
    ```
    [cassandra_1]
    hostname=<HOSTNAME>
    port=<PORT NUMBER>
    logs_enabled=False
    log_type_name=None
    log_file_path=None
    ```
#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the cassandra_monitoring.py script.

- Place the "cassandra_monitoring" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/cassandra_monitoring

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

-  Further move the folder "cassandra_monitoring" into the  Site24x7 Windows Agent plugin directory:
    ```
        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\cassandra_monitoring
    ```
    
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

----

### Supported Metrics
The following metrics are captured in the Cassandra monitoring plugin:

- **Total Latency (Read)**

    Read response time, in microseconds.

- **Total Latency (Write)**

    Write response time, in microseconds.

- **Cross Node Latency**

    The time period starts when a node sends a message and ends when the current node receives it.

- **Total Hints**

    Number of hint messages written to this node since [re]start. This includes one hint per host.

- **Throughtput (Writes)**

    Write requests per second.

- **Throughtput (Read)**

    Read requests per second.

- **Key cache hit rate**

    Rate of read requests for keys present in the cache.

- **Disk Used**

    Disk space used on a node, in bytes.

- **Completed compaction tasks**

    Total compaction tasks completed.

- **Pending compaction tasks**

    Total compaction tasks in queue.

- **ParNew garbage collections (count)**

    Number of young-generation collections

- **ParNew garbage collections (time)**

    Elapsed time of young-generation collections, in milliseconds.


- **CMS garbage collections (count)**

     Number of old-generation collections

- **CMS garbage collections (time)**

    Elapsed time of old-generation collections, in milliseconds

- **Exceptions**

    Requests for which Cassandra encountered an error

- **Timeout exceptions (write)**

    Requests not acknowledged within configurable timeout window during write

- **Timeout exception (read)**

    Requests not acknowledged within configurable timeout window during read

- **Unavailable exceptions (write)**

    Requests for which the required number of nodes was unavailable during writing

- **Unavailable exceptions (read)**

    Requests for which the required number of nodes was unavailable during reading

- **Pending tasks**

    Tasks in a queue awaiting a thread for processing

- **Dropped Mutations**

    Number of dropped mutations on this table.

- **Pending Flushes**

    Estimated number of flush tasks pending for this table.

- **Blocked On Allocation**

    Number threads are blocked by memtable allocation

- **Currently Blocked Tasks**

    Number of tasks that are currently blocked due to queue saturation but on retry will become unblocked

