"""
Server file for centralized log management
"""
__author__="Mayur"
import socket
import sys
import thread
import json

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
		try:
		    print >>sys.stderr, 'client connected:', client_address
		    while True:
		        data = connection.recv(1024)
		        print >>sys.stderr, '"%s"' % data
		        if data:
		           pass
		        else:
		            break
		finally:
		    connection.close()

	def accepting_client_thread(self):
		"""Accepting Client Thread"""
		while True:
		    print >>sys.stderr, 'waiting for a connection'
		    connection, client_address = self.sock.accept()
		    thread.start_new_thread(self.multipleclients,(connection,client_address))
		self.sock.close()

if __name__=="__main__":
   data=read_from_file("logarch-server.json")
   if "server_port" not in data.keys():
   	   data['server_port']=8192
   if "server_hostname" not in data.keys():
	   data["server_hostname"]=socket.gethostname()
   print data
   server_socket=ManageSocket(server_hostname=data['server_hostname'],server_port=data['server_port'])
   server_socket.accepting_client_thread()
