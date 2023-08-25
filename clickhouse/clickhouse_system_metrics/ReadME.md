Clickhouse monitoring
---  
ClickHouse is a fast open-source OLAP database management system. For more details, refer their website: https://clickhouse.tech

### Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.
- Clickhouse Python Driver
https://clickhouse-driver.readthedocs.io/en/latest/installation.html

- To install the driver, execute the command :
	```
	pip install clickhouse-driver
	```

### Plugin Installation  

- Create a directory named "clickhouse_system_metrics"

- Download the below files and place it under the "clickhouse_system_metrics" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/clickhouse/clickhouse_system_metrics/clickhouse_system_metrics.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/clickhouse/clickhouse_system_metrics/clickhouse_system_metrics.cfg


- Edit the clickhouse_system_metrics.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python clickhouse_system_metrics.py --hostname = <hostname-or-ip> --port = <port>  --database = <db> --user = <username> --password = <password> --timeout = <timeout>
#### Configurations

- Edit the clickhouse_system_metrics.cfg with appropriate configurations
	```
	[localhost]
	hostname = localhost
	port = 9000
	database = default
	user = default
	password = 
	timeout = 10
	```
#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the clickhouse_system_metrics.py script.

- Place the "clickhouse_system_metrics" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/clickhouse_system_metrics

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "clickhouse_system_metrics" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\clickhouse_system_metrics


### Metrics Captured
    BackgroundBufferFlushSchedulePoolTask
    BackgroundDistributedSchedulePoolTask
    BackgroundMovePoolTask
    BackgroundPoolTask
    BackgroundSchedulePoolTask
    CacheDictionaryUpdateQueueBatches
    CacheDictionaryUpdateQueueKeys
    ContextLockWait
    DelayedInserts
    DictCacheRequests
    DiskSpaceReservedForMerge
    DistributedFilesToInsert
    DistributedSend
    EphemeralNode
    GlobalThread
    GlobalThreadActive
    HTTPConnection
    InterserverConnection
    LocalThread
    LocalThreadActive
    MemoryTracking
    MemoryTrackingForMerges
    MemoryTrackingInBackgroundBufferFlushSchedulePool
    MemoryTrackingInBackgroundDistributedSchedulePool
    MemoryTrackingInBackgroundMoveProcessingPool
    MemoryTrackingInBackgroundProcessingPool
    MemoryTrackingInBackgroundSchedulePool
    Merge
    MySQLConnection
    OpenFileForRead
    OpenFileForWrite
    PartMutation
    PostgreSQLConnection
    Query
    QueryPreempted
    QueryThread
    RWLockActiveReaders
    RWLockActiveWriters
    RWLockWaitingReaders
    RWLockWaitingWriters
    Read
    ReadonlyReplica
    ReplicatedChecks
    ReplicatedFetch
    ReplicatedSend
    Revision
    SendExternalTables
    SendScalars
    StorageBufferBytes
    StorageBufferRows
    TCPConnection
    VersionInteger
    Write
    ZooKeeperRequest
    ZooKeeperSession
    ZooKeeperWatch
