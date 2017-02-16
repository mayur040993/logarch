import socket
import sys
import sh
import json
import threading
import time
from flask import Flask, request, render_template
from flask import jsonify
app = Flask(__name__)


server_port=8192
hostname=socket.gethostname()
threads = []

class get_connection(threading.Thread):

    thread_id=1

    def __init__ (self,logfile,server_hostname,server_port,hostname):
        threading.Thread.__init__(self)
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.logfile = logfile
        self.server_hostname=server_hostname
        self.server_port=server_port
        self.hostname=hostname
        self.id=self.__class__.thread_id
        self.__class__.thread_id+=1


    def parsedata(self,logfile,line):
        logs={
            "hostname":self.hostname,
            "logs":line,
            "name":logfile["name"],
             "thread_id":self.hostname+str(self.id)
        }
        return logs

    def run(self):
        #print self.logfile
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected=False
        check_wait=5;

        while check_wait!=0 and not connected:
            try:
                server_address = (self.server_hostname,self.server_port)
                #print >>sys.stderr, 'connecting to %s server_port %s' % server_address
                sock.connect(server_address)
                connected=True
                time.sleep(5)
            except:
                check_wait-=1
                print "Server with hostname:%s and port:%s not reachable" % (self.hostname,self.server_port)

        if connected:
            try:
                for line in sh.tail("-f",self.logfile["filepath"], _iter=True):
                    with self.pause_cond:
                        print self.pause_cond
                        print self.paused
                        print self,"in self"
                        time.sleep(2)
                        while self.paused:
                            print "paused"
                            time.sleep(1)
                    logs=self.parsedata(self.logfile,line)
                    logs=json.dumps(logs)
                    sock.sendall(logs)
            finally:
                sock.close()

    def pause(self):
        self.paused=True
        print self.paused,"mayur"
        self.pause_cond.acquire()

    def resume(self):
        self.paused=False
        self.pause_cond.notify()
        self.pause_cond.release()



def read_from_file(client_conf):
    with open(client_conf) as data_file:
        data = json.load(data_file)
    return data

thread_dict={}
def creating_threads():
    data=read_from_file('logarch-client.json')
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
        print "Server Hostname not found in logarch-client.json file add server_hostname"
        sys.exit(1)
    if "hostname" in data.keys():
        hostname=data["hostname"]
    else:
        data["hostname"]=hostname

    for logfile in data["logfiles"]:
        print logfile
        thread=get_connection(logfile,server_hostname,server_port,hostname)
        thread.start()
        print thread
        thread_dict[thread.hostname+str(thread.id)]=thread
        threads.append(thread)

    print thread_dict
    app.run(debug=True,use_reloader=False)

    return threads

@app.route('/pause')
def pause_api():
    if 'thread_id' in request.args:
        print thread_dict
        thread_dict[str(request.args['thread_id'])].paused=True
        print thread_dict[str(request.args['thread_id'])].paused
        return 'pause ' + request.args['thread_id']


@app.route('/resume')
def resume_api():
    if 'thread_id' in request.args:
        thread_dict[str(request.args['thread_id'])].a
        return 'resume ' + request.args['thread_id']



if __name__=="__main__":
    threads=creating_threads()
