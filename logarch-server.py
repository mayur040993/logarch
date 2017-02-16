"""
Server file for centralized log management
"""
__author__="Mayur"
import socket
import sys
import thread
import json
from elasticsearch import Elasticsearch
import datetime


def processingdata(data):
    return data.split(' ')

def read_from_file(conf_file):
    """Read data from conf file"""
    with open(conf_file) as data_file:
        data = json.load(data_file)
    return data

class ManageSocket():
    """Creating socket class to manage sockets"""

    def __init__(self,**kwargs):
        self.server_port=kwargs['server_port']
        self.server_hostname=kwargs['server_hostname']
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.server_hostname,self.server_port)
        print >>sys.stderr, 'starting up on %s port %s' % server_address
        sock.bind(server_address)
        sock.listen(5)
        self.sock=sock

    def multipleclients(self,connection,client_address):
        print connection
        try:
            print >>sys.stderr, 'client connected:', client_address
            while True:
                data = connection.recv(1024)
                data=json.loads(data)
                print type(data)
                data['@timestamp']=datetime.datetime.utcnow()
                print type(data)
                print data
                es.index(index=client_address[0],doc_type=client_address[0],body=data)
                print >>sys.stderr, '"%s"' % data
                if data:
                   pass
                else:
                    break
        finally:
            connection.close()

    def accepting_client_thread(self):
        """Accepting Client Thread"""
        print "Accepting Client Thread"
        while True:
            print >>sys.stderr, 'waiting for a connection'
            connection, client_address = self.sock.accept()
            print connection,client_address,"Mayur"

            print client_address
            es.indices.create(index=client_address[0], ignore=400)
            thread.start_new_thread(self.multipleclients,(connection,client_address))
        self.sock.close()

def check_elastic_conf(data):
     if "elasticsearch" not in data.keys():
         print "elastic search not integerated"
         return None,None,None,None;
     else:
         elastic_hostname=data['elasticsearch']['hostname']
         elastic_port=data['elasticsearch']['port']
         if "user" in data['elasticsearch'].keys() is not None:
             el_user=data['elasticsearch']['user']
         else:
             el_user=None
         if "password" in data['elasticsearch'].keys() is not None:
             el_pass=data['elasticsearch']['password']
         else:
             el_pass=None
     return elastic_hostname,elastic_port,el_user,el_pass

if __name__=="__main__":
   data=read_from_file("logarch-server.json")
   if "server_port" not in data.keys():
          data['server_port']=8192
   if "server_hostname" not in data.keys():
       data["server_hostname"]=socket.gethostname()
   elastic_hostname,elastic_port,el_user,el_pass=check_elastic_conf(data);
   if elastic_hostname:
       try:
           es = Elasticsearch([{'host':elastic_hostname,'port':elastic_port}], http_auth=(el_user,el_pass))
       except:
           print "check elastic search connection configurations"
   print data
   server_socket=ManageSocket(server_hostname=data['server_hostname'],server_port=data['server_port'])
   server_socket.accepting_client_thread()
