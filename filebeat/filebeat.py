#!/usr/bin/python3

import json
import urllib
import urllib.request as connector

metric_units={
    "total.freespace":"bytes",
    "total.spaceused":"bytes",
    "total.space":"bytes",
    "tcp.established":"bytes",
    "tcp.listening":"bytes",
    "tcp.closing":"bytes",
    "network.in":"bytes",
    "network.out":"bytes",
    "network.in.errors":"bytes",
    "network.out.dropped":"bytes",
    "network.out.errors":"bytes",
    "syn.sent":"bytes",
    "syn.recv":"bytes"
}



class Filebeat(object):

    def __init__(self, args):
        self.host=args.host
        self.port=args.port
        self.plugin_version=args.plugin_version
        self.heartbeat=args.heartbeat  
        self.resultjson = {}
        
        self.metrics_collector()
        
        self.resultjson['plugin_version'] = self.plugin_version
        self.resultjson['heartbeat_required'] = self.heartbeat
     
    def metrics_collector(self):

        try:
            url="http://"+self.host+":"+self.port+"/metricbeat-*/_search?pretty"
            data1=((connector.urlopen(url)).read()).decode("UTF-8")
            data1=json.loads(data1)
            data=data1["hits"]["hits"][1]["_source"]
            self.resultjson["system.type"]=data["service"]["type"]
            self.resultjson["network1.name"]=data["system"]["network"]["name"]
            name=data["system"]["network"]["name"]
            self.resultjson[name+".out"]=data["system"]["network"]["out"]["bytes"]
            self.resultjson[name+".out.errors"]=data["system"]["network"]["out"]["errors"]
            self.resultjson[name+".out.dropped"]=data["system"]["network"]["out"]["dropped"]
            self.resultjson[name+".in"]=data["system"]["network"]["in"]["bytes"]
            self.resultjson[name+".in.errors"]=data["system"]["network"]["in"]["bytes"]
            self.resultjson[name+".out.dropped"]=data["system"]["network"]["in"]["dropped"]
            data=data1["hits"]["hits"][3]["_source"]
            self.resultjson["network2.name"]=data["system"]["network"]["name"]
            name=data["system"]["network"]["name"]
            self.resultjson[name+".out"]=data["system"]["network"]["out"]["bytes"]
            self.resultjson[name+".out.errors"]=data["system"]["network"]["out"]["errors"]
            self.resultjson[name+".out.dropped"]=data["system"]["network"]["out"]["dropped"]
            self.resultjson[name+".in"]=data["system"]["network"]["in"]["bytes"]
            self.resultjson[name+".in.errors"]=data["system"]["network"]["in"]["bytes"]
            self.resultjson[name+".out.dropped"]=data["system"]["network"]["in"]["dropped"]       
            data=data1["hits"]["hits"][5]["_source"]["system"]["fsstat"]
        
            self.resultjson["total.freespace"]=data["total_size"]["free"]
            self.resultjson["total.spaceused"]=data["total_size"]["used"]
            self.resultjson["total.space"]=data["total_size"]["total"]
            self.resultjson["total.files"]=data["total_files"]
            data=data1["hits"]["hits"][7]["_source"]["system"]["socket"]["summary"]["tcp"]["all"]
            self.resultjson["tcp.listening"]=data["listening"]
            self.resultjson["tcp.established"]=data["established"]
            self.resultjson["tcp.closing"]=data["closing"]
            self.resultjson["tcp.count"]=data["count"]
            self.resultjson["syn.recv"]=data["syn_recv"]
            self.resultjson["syn.sent"]=data["syn_sent"]
       
        except Exception as e:
            self.resultjson["msg"]=str(e)
            self.resultjson["status"]=0
        return self.resultjson

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= "localhost")
    parser.add_argument('--port',help="Port",nargs='?', default= "9200")
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    args=parser.parse_args()
	
    filebeat = Filebeat(args)
    resultjson = filebeat.metrics_collector()
    resultjson['units'] = metric_units
    print(json.dumps(resultjson, indent=4, sort_keys=True))
