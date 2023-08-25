# Oracle Core Monitoring


                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Install **python3.7** or higher version on the server.
- Roles need to be granted for the user to be used in plugin

	```
	grant select_catalog_role to {username}
	```
	```
	grant create session to {username}
	```

---
### Plugin Installation  

- Create a directory named "OracleCore".
- Install the **oracledb** python module.
	```
	pip3 install oracledb
	```

	
- Download the below files in the "OracleCore" folder and place it under the "OracleCore" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleCore/OracleCore.py && sed -i "1s|^.*|#! $(which python3)|" OracleCore.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleCore/OracleCore.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```
	 python3 OracleCore.py --hostname=<name of the host> --port=<port> --sid=<SID> --username=<USERNAME> --password=<PASSWORD> --oracle_home=<ORACLE_HOME>
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the OracleCore.cfg file.
	```
	    [ORCL]
	    hostname=localhost
	    port=1521
	    sid=<SID>
	    username=<USERNAME>
	    password=<PASSWORD>
	    logs_enabled="False"
	    log_type_name =None
	    log_file_path=None
	    oracle_home=None
	```	
#### Linux
- Place the "OracleCore" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/OracleCore
#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further, move the folder "OracleCore" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\OracleCore


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


	


## Supported Metrics
The following metrics are captured in the OracleCore Plugin:

### System Metrics 

- **Soft Parse Ratio**

    The Soft Parse Ratio Oracle metric is the ratio of soft parses

- **Total Parse Count Per Sec**

    The total number of parses per second

- **Total Parse Count Per Txn**

    The total number of parses per transaction

- **Hard Parse Count Per Sec**

    The total number hard parses per second

- **Hard Parse Count Per Txn**

    The number of hard parses per transaction

- **Parse Failure Count Per Sec**

    The number of failed parses per second

- **Parse Failure Count Per Txn**

    The number of failed parses per transaction

- **Temp Space Used**

    Temporary space used

- **Session Count**

    Total count of sessions

- **Session Limit %**

    Max number of concurrent connections allowed by db

- **Database Wait Time Ratio**

    Ratio of amount of CPU used to the amount of total db time

- **Memory Sorts Ratio**

    Percentage of sorts that are done to disk vs. in-memory

- **Disk Sort Per Sec**

    The number of sorts going to disk per second for this sample period

- **Rows Per Sort**

    Average number of rows per sort during this sample period

- **Total Sorts Per User Call**

    Total number of sorts per user call

- **User Rollbacks Per Sec**

    Number of times, per second during the sample period, that users manually issue the ROLLBACK statement

- **SQL Service Response Time**

    The average elapsed time per execution of a representative set of SQL statements

- **Long Table Scans Per Sec**

    Number of long and short table scans per second during the sample period

- **Average Active Sessions**

    Number of sessions, either working or waiting for a resource at a specific point in time

- **Logons Per Sec**

    The number of logons per second during the sample period

- **Global Cache Blocks Lost**

    Number of global cache blocks lost over the user-defined observation period

- **Global Cache Blocks Corrupted**

    Number of blocks that encountered a corruption or checksum failure during interconnect over the user-defined observation period


- **GC CR Block Received Per Second**

    Number of GC CR block received per second

- **Enqueue Timeouts Per Sec**

    Total number of table and row locks per second that time out before they could complete

- **Physical Writes Per Sec**

    The number of direct physical writes per second

- **Physical Reads Per Sec**

    The number of direct physical reads per second

- **Shared Pool Free %**

    Percentage of free space in shared pool

- **Library Cache Hit Ratio**

    The number of pin requests which result in pin hits

- **Cursor Cache Hit Ratio**

    Ratio of the number of times an open cursor was found divided by the number of times a cursor was sought

- **Buffer Cache Hit Ratio**

    The percentage of pages found in the buffer cache without having to read from disk

- **Dict Cache Hit Ratio**

    The measure  of ratio of dictionary hits to misses

- **Rman Failed Backup Count**

    Count of RMAN failed backups

- **Long Running Query**

    Count of long running queries


### PGA Metrics

- **Total PGA Allocated**

    Total amount of memory provided currently

- **Total Freeable PGA Memory**

    The amount of PGA memory that can be reallocated or given back to the operating system

- **Maximum PGA Allocated**

    Maximum amount of memory provided currently

- **Total PGA Inuse**

    Total amount of memory inuse
