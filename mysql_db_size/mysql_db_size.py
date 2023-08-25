#!/usr/bin/python
"""

Site24x7 MySql Plugin

"""
import traceback
import re
import json
import os
import subprocess
import time
import sys

VERSION_QUERY = 'SELECT VERSION()'

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section: 
#Use either True | False - enabled True will read mysql configurations from my.cnf file , Please provide the my.cnf path below
USE_MYSQL_CONF_FILE=False

#Used only when USE_MYSQL_CONF_FILE is set to True , We have provided the default path change it as it is in your server
MY_CNF_FILE_LOCATION='/etc/mysql/my.cnf'

MYSQL_HOST = "localhost"

MYSQL_PORT="3306"

MYSQL_USERNAME="root"

MYSQL_PASSWORD=""

MYSQL_SOCKET = "/tmp/mysql.sock"

#Mention the units of your metrics in this python dictionary. If any new metrics are added make an entry here for its unit.
METRICS_UNITS={'connection_usage':'%'}

class MySQL(object):
    
    def __init__(self,config):
        self.configurations = config
        self.connection = None
        self.host = os.getenv('MYSQL_HOST', self.configurations.get('host', 'localhost'))
        self.port = os.getenv('MYSQL_PORT', int(self.configurations.get('port', '3306')))
        self.username = os.getenv('MYSQL_USERNAME', self.configurations.get('user', 'root'))
        self.password = os.getenv('MYSQL_PASSWORD', self.configurations.get('password', ''))
    
    @staticmethod
    def get_sock_path():
        _output, _status, _proc = None, False, None
        try:
            _proc = subprocess.Popen("netstat -ln | awk '/mysql(.*)?\.sock/ { print $9 }'" ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(0.5)
            if not _proc.poll() is None:
                _status = True
                _output, error = _proc.communicate()
                _output = _output.strip("\n")
        except Exeception as e:
            if type(_proc) is subprocess.Popen:
                _proc.kill()
                _proc.poll()
        finally:
            return _status, _output
    
    #execute a mysql query and returns a dictionary
    def executeQuery(self, con, query):
        try:
            cursor = con.cursor()
            cursor.execute(query)
            metric = {}
            for entry in cursor:
                try:
                    metric[entry[0]] = float(entry[1])
                except ValueError as e:
                    metric[entry[0]] = entry[1]

            return metric
        except pymysql.OperationalError as message:
            pass

    def getDbConnection(self):
        try:
            import pymysql
            if USE_MYSQL_CONF_FILE:
                db = pymysql.connect(read_default_file=MY_CNF_FILE_LOCATION)
            else:
                db = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=int(self.port))
            self.connection = db
        except Exception as e:
            try:
                import pymysql
                _status, _output = MySQL.get_sock_path()
                if _status:
                    db = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=int(self.port), unix_socket=_output)
                else:
                    db = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=int(self.port), unix_socket=MYSQL_SOCKET)
                self.connection = db
            except Exception as e:
                traceback.print_exc()
                return False
        return True

    def checkPreRequisites(self,data):
        bool_result = True
        try:
            import pymysql
        except Exception:
            data['status']=0
            data['msg']='pymysql module not installed'
            bool_result=False
            pymysql_returnVal=os.system('pip install pymysql >/dev/null 2>&1')
            if pymysql_returnVal==0:
                bool_result=True
                data.pop('status')
                data.pop('msg')
        return bool_result,data

    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT

        bool_result,data = self.checkPreRequisites(data)
        
        if bool_result==False:
            return data
        else:
            try:
                import pymysql
            except Exception:
                data['status']=0
                data['msg']='pymysql module not installed'
                return data

            if not self.getDbConnection():
                data['status']=0
                data['msg']='Connection Error'
                return data
    
            try:
                con = self.connection
                
                # get MySQL version
                try:
                    cursor = con.cursor()
                    cursor.execute(VERSION_QUERY)
                    result = cursor.fetchone()
                    data['version'] = result[0]
                except pymysql.OperationalError as message:
                    return data
    
                global_metrics = self.executeQuery(con, 'SELECT table_schema "DB Name",ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) "DB Size in MB" FROM information_schema.tables GROUP BY table_schema;')
                units={}
                for k , v in global_metrics.items():
                    data[k]=v
                    units[k]='MB'
                data['units']=units
                cursor.close()
                con.close()
            except Exception as e:
              pass
        return data

if __name__ == "__main__":

    configurations = {'host': MYSQL_HOST, 'port': MYSQL_PORT, 'user': MYSQL_USERNAME, 'password': MYSQL_PASSWORD}

    mysql_plugins = MySQL(configurations)
    
    result = mysql_plugins.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
