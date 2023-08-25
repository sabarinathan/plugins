#!/usr/bin/python
"""

Site24x7 Oracle DB Plugin

"""
import os
from ast import arg
import json
# if any changes are done to the metrics or units, increment the plugin version number here 
PLUGIN_VERSION = "1"

# Setting this to true will alert you when plugin is down
HEARTBEAT = "true"


# Mention the units of your metrics . If any new metrics are added, make an entry here for its unit if needed.
METRICS_UNITS = {'tablespace_usage_percent': '%','used_space':'MB','free_space':'MB','free_blocks':'blocks','reads':'reads','writes':'writes'}

def convertToMB(val):
    try:
        mb = round(float(val/(1024*1024)),2)
        return mb   
    except:
        mb = round(int(val/(1024*1024)),2)
        return mb

class Oracle(object):
    def __init__(self, args):


        self.connection = None
        self.host = args.host
        self.port = args.port
        self.sid = args.sid
        self.username = args.username
        self.password = args.password
        self.TABLESPACE_NAME=args.tablespace_name
        self.data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT, 'units':METRICS_UNITS}
     
    def metricCollector(self):
        c=None
        conn=None
        try:
            import cx_Oracle
        except Exception as e:
            self.data['status'] = 0
            self.data['msg'] = 'cx_Oracle module is not installed'
            return self.data

        try:
            try:
                conn = cx_Oracle.connect(self.username,self.password,self.host+':'+str(self.port)+'/'+self.sid)
                c = conn.cursor()
            except Exception as e:
                self.data['status']=0
                self.data['msg']='Exception while connecting to '+self.host

            c.execute("select * from (SELECT t.tablespace_name,t.logging,t.contents,t.status,NVL(df.allocated_bytes,0)-NVL((NVL(f.free_bytes,0)+df.max_free_bytes),0) usedBytes,NVL((NVL(f.free_bytes,0)+df.max_free_bytes),0) freeBytes,NVL(f.free_blocks,0) freeBlocks FROM sys.dba_tablespaces t, (select ff.tablespace_name,sum(ff.free_bytes) free_bytes,sum(ff.free_blocks) free_blocks from (SELECT fs.tablespace_name, SUM(fs.bytes) free_bytes, SUM(fs.blocks) free_blocks FROM sys.dba_free_space fs,sys.dba_data_files dfs where fs.file_id=dfs.file_id and fs.tablespace_name='"+self.TABLESPACE_NAME+"' GROUP BY fs.tablespace_name,dfs.autoextensible) ff group by tablespace_name) f, (select dff.tablespace_name,sum(dff.allocated_bytes) allocated_bytes,sum(dff.max_free_bytes) max_free_bytes from (select tablespace_name,autoextensible,sum(decode(sign(maxbytes-bytes),1,maxbytes,bytes)) allocated_bytes,sum(decode(sign(maxbytes-bytes),1,abs(maxbytes-bytes),0)) max_free_bytes from dba_data_files where tablespace_name='"+self.TABLESPACE_NAME+"' group by tablespace_name,autoextensible) dff group by tablespace_name) df WHERE t.tablespace_name = f.tablespace_name(+) and t.tablespace_name=df.tablespace_name(+) and t.tablespace_name='"+self.TABLESPACE_NAME+"'),(SELECT  SUM(rw.phyrds) phyrds, SUM(rw.phywrts) phywrts FROM sys.dba_data_files drw, V$filestat rw WHERE drw.file_id = rw.file# and drw.tablespace_name = '"+self.TABLESPACE_NAME+"' GROUP BY drw.tablespace_name)")
            
            for row in c:
                name, log, content, status, usedbytes, freebytes, free_blocks, reads, writes = row
                if name == self.TABLESPACE_NAME :
                    self.data['logging'] = log
                    self.data['content']=content
                    self.data['tablespace_status']=status
                    self.data['used_space']=convertToMB(usedbytes)
                    self.data['free_space']=convertToMB(freebytes)
                    self.data['reads']=reads
                    self.data['writes']=writes
                    self.data['free_blocks']=free_blocks
                    self.data['tablespace_usage_percent']=round((float(usedbytes)/float(usedbytes+freebytes))*100,2)
                    self.data['tablespace_name']=name
                else:
                    self.data['status'] = 0
                    self.data['msg'] = 'Please check the Tablespace Name in the configuration section'
                

        except Exception as e:
            self.data['status'] = 0
            self.data['msg'] = str(e)
        finally:
            if c!= None : c.close()
            if conn != None : conn.close()
            return self.data

if __name__ == "__main__":



    ORACLE_HOST = "localhost"
    ORACLE_PORT = "1521"
    ORACLE_SID = "XE"
    ORACLE_USERNAME = "test"
    ORACLE_PASSWORD = "test"
    TABLESPACE_NAME = "SYSTEM"  


    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--host",help="oracle host name",default=ORACLE_HOST)
    parser.add_argument("--port",help="oracle port number",default=ORACLE_PORT)
    parser.add_argument("--sid",help="oracle sid name",default=ORACLE_SID)
    parser.add_argument("--username",help="oracle username",default=ORACLE_USERNAME)
    parser.add_argument("--password",help="oracle password",default=ORACLE_PASSWORD)
    parser.add_argument("--tablespace_name",help="oracle tablespace name",default=TABLESPACE_NAME)


    args=parser.parse_args()


    oracle_plugin = Oracle(args)

    result = oracle_plugin.metricCollector()

print(json.dumps(result, indent=4, sort_keys=True))

            
