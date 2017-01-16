import socket
import sys
import sh
import json
import threading
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='example.log',level=logging.DEBUG)


server_port=8192
hostname=socket.gethostname()

class get_connection(threading.Thread):

    def __init__ (self,logfile,server_hostname,server_port,hostname):
        threading.Thread.__init__(self)
        self.logfile = logfile
        self.server_hostname=server_hostname
        self.server_port=server_port
        self.hostname=hostname

 
    def parsedata(self,logfile,line):
        logs={
		"hostname":self.hostname,
                "logs":line,
                "name":logfile["name"]
	     }
        return logs

    def run(self):
        logging.debug(self.logfile)
	    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	server_address = (self.server_hostname,self.server_port)
	    logging.debug(sys.stderr, 'connecting to %s server_port %s' % server_address)
	    sock.connect(server_address)
	try:
        for line in sh.tail("-f",self.logfile["filepath"], _iter=True):
    	    logs=self.parsedata(self.logfile,line)
            #print logs
            logging.debug(logs)
            logs=json.dumps(logs)
		sock.sendall(logs)
	finally:
    	   sock.close()

   

def read_from_file():
    with open('logarch.json') as data_file:    
    	data = json.load(data_file)
    return data


def creating_threads():
   data=read_from_file()
   global server_port
   global hostname
   if "server_port" in data.keys():
      server_port=data["server_port"]
   else:
      data["server_port"]=server_port
   try:
   	if "server_hostname" in data.keys():
           server_hostname=data["server_hostname"]
   except:
        logging.debug("Server Hostname not found in logp.json file add server_hostname")
        sys.exit(1)
   if "hostname" in data.keys():
      hostname=data["hostname"]
   else:
      data["hostname"]=hostname

   
   threads = []
   for logfile in data["logfiles"]:
       logging.debug(logfile)
       thread=get_connection(logfile,server_hostname,server_port,hostname)
       thread.start()
       threads.append(thread)
   for thread in threads:
       thread.join()

if __name__=="__main__":
   creating_threads()
