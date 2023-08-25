Plugin for monitoring expiry days for PGP public keys
=====================================================

To monitor the number of days to expire for the public keys in PGP. For more details regarding pgp key configurations, please refer https://packaging.ubuntu.com/html/getting-set-up.html

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "python-gnupg driver" python module.

- How to install python-gnupg :

		default:    /usr/bin/python -m pip install python-gnupg
		python2:    python -m pip install python-gnupg
		python3:    python3 -m pip install python-gnupg

For more details on the python-gnupg driver , refer https://pypi.org/project/python-gnupg/#description. If pip command not present kindly install using the below section

- How to install pip :
	
		curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		python get-pip.py

### Plugin installation
---
##### Linux 

- Create a directory "pgp_expiry" .

- Download all the files in "pgp_expiry" folder and place it under the "pgp_expiry" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/pgp_expiry/pgp_expiry.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/pgp_expiry/pgp_expiry.cfg
  
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the pgp_expiry.py script.
	
- Configure the keys to be monitored, as mentioned below in "pgp_expiry.cfg"

		[expiry]
		keys_to_check = "B2E1062C8683440B,23BD06A606281990,B2E1062C86834232,"
		key_server = "keyserver.ubuntu.com"
		gpg_location = "/home/local/.gnupg"
		plugin_version = 1
		heartbeat = True

- Execute the below command with appropriate arguments to check for the valid json output.  

		python pgp_expiry.py --keys_to_check "key1,key2,key3" --key_server "keyserver.ubuntu.com" --gpg_location "/home/local/hostname/.gnupg" --plugin-version 1 --heartbeat True
		
- Move the directory "pgp_expiry" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics Captured
---
    	keyname - No of days for expiry from today
