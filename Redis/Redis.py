#!/usr/bin/python
"""
  Site24x7 Redis Plugin
"""
import json,sys

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
host = "localhost"
port = "6379"
password = ""
dbs = "0"


### Uncomment/Comment the Attribute Names to be monitored
### Change plugin_version if you edit this section
METRICS = {
    #"_length": "length", 
    
    #"aof_current_rewrite_time_sec": "aof current rewrite time", 
    #"aof_enabled": "aof enabled", 
    #"aof_last_bgrewrite_status": "aof last bgrewrite status", 
    #"aof_last_rewrite_time_sec": "aof last rewrite time", 
    #"aof_last_write_status": "aof last write status", 
    #"aof_rewrite_in_progress": "aof rewrite in progress", 
    #"aof_rewrite_scheduled": "aof rewrite scheduled", 
    
    #"arch_bits": "arch bits", 
    "blocked_clients": "blocked clients", 
    #"client_biggest_input_buf": "client biggest input buf", 
    #"client_longest_output_list": "client longest output list", 
    "cluster_enabled": "cluster enabled", 
    "connected_clients": "connected clients", 
    "connected_slaves": "connected slaves", 
    "evicted_keys": "evicted keys", 
    "expired_keys": "expired keys", 
    #"hz": "hz", 
    "instantaneous_input_kbps": "incoming traffic", 
    "instantaneous_ops_per_sec": "ops/sec",
    "instantaneous_output_kbps": "output traffic", 
    "keyspace_hits": "keyspace hits", 
    "keyspace_misses": "keyspace misses", 
    #"latest_fork_usec": "latest fork usec", 
    #"loading": "loading", 
    #"lru_clock": "lru clock", 
    #"master_repl_offset": "master repl offset", 
    #"mem_allocator": "mem allocator", 
    #"mem_fragmentation_ratio": "mem fragmentation ratio", 
    #"migrate_cached_sockets": "migrate cached sockets", 
    #"multiplexing_api": "multiplexing api", 
    #"pubsub_channels": "pubsub channels", 
    #"pubsub_patterns": "pubsub patterns", 
    #"rdb_bgsave_in_progress": "rdb bgsave in progress", 
    #"rdb_changes_since_last_save": "rdb changes since last save", 
    #"rdb_current_bgsave_time_sec": "rdb current bgsave time sec", 
    #"rdb_last_bgsave_status": "rdb last bgsave status", 
    #"rdb_last_bgsave_time_sec": "rdb last bgsave time sec", 
    #"rdb_last_save_time": "rdb last save time", 
    #"redis_build_id": "redis build id", 
    #"redis_git_dirty": "redis git dirty", 
    #"redis_git_sha1": "redis git sha1", 
    #"rejected_connections": "rejected connections", 
    #"repl_backlog_active": "repl backlog active", 
    #"repl_backlog_first_byte_offset": "repl backlog first byte offset", 
    #"repl_backlog_histlen": "repl backlog histlen", 
    #"repl_backlog_size": "repl backlog size", 
    #"role": "role", 
    #"run_id": "run id", 
    #"sync_full": "sync full", 
    #"sync_partial_err": "sync partial err", 
    #"sync_partial_ok": "sync partial ok", 
    #"total_commands_processed": "total commands processed", 
    #"total_connections_received": "total connections received", 
    #"total_net_input_bytes": "total net input bytes", 
    #"total_net_output_bytes": "total net output bytes", 
    #"uptime_in_days": "uptime in days", 
    "uptime_in_seconds": "uptime", 
    "used_cpu_sys": "used cpu sys", 
    #"used_cpu_sys_children": "used cpu sys children", 
    "used_cpu_user": "used cpu user", 
    #"used_cpu_user_children": "used cpu user children", 
    "used_memory": "used memory", 
    #"used_memory_human": "used memory human", 
    #"used_memory_lua": "used memory lua", 
    #"used_memory_peak": "used memory peak", 
    #"used_memory_peak_human": "used memory peak human", 
    #"used_memory_rss": "used memory rss"
}


#Mention the units of your metrics in this dictionary. If any new metrics are added make an entry here for its unit.
METRICS_UNITS={'incoming traffic':'kbps','outgoing traffic':'kbps','used memory':'KB'}

class Redis(object):
    def __init__(self,args):
        self.args=args
        self.host=args.host
        self.port=args.port
        self.dbs=args.dbs
        if args.password:
            self.password=args.password
        else:
            self.password=""

    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        try:
            import redis
        except Exception:
            data['status']=0
            data['msg']='Redis Module Not Installed'
            return data
        stats = None
        for db in self.dbs.split(','):
            try:
                redis_connection = redis.StrictRedis(
                    host=self.host,
                    port=self.port,
                    db=int(self.dbs),
                    password=self.password
                )
                stats = redis_connection.info()
            except Exception as e:
                data['status']=0
                data['msg']=str(e)
        if not stats:
            return data
        total_keys=0
        for name, value in stats.items():
            try:
                if type(value)==dict and 'keys' in value:
                    total_keys+=value['keys']
                if name in METRICS.keys() :
                    if METRICS[name] == 'used memory':
                        value = value / 1024
                    data[METRICS[name]] = value
            except (ValueError, TypeError) as e:
                data[name] = value
        try:
            total_key_stats = data['keyspace hits'] + data['keyspace misses']
            if total_key_stats == 0:
                data['hit ratio']=0
            else:
                data['hit ratio'] = data['keyspace hits'] / total_key_stats
                data['total_keys']=total_keys
        except Exception as e:
                data['status']=0
                data['msg']=str(e)
        data['units']=METRICS_UNITS
        return data


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= "localhost")
    parser.add_argument('--port',help="Port",nargs='?', default= "6379")
    parser.add_argument('--dbs',help="dbs" , default= dbs)
    parser.add_argument('--password',help="Password" , default= password)
    args=parser.parse_args()

    redis_plugin = Redis(args)

    result=redis_plugin.metricCollector()
 
    print(json.dumps(result, indent=4, sort_keys=True))





