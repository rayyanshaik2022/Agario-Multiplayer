import pickle
import socket
import time


class Network:

    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.6"
        self.port = 5555
        self.find_ip(ip)
        self.addr = (self.server, self.port)
        self.pos = self.connect()
        self.ping = 0

    def find_ip(self, ip):
        '''
        Takes a string, and returns (if found)
        the ip and port
        '''

        if ":" not in ip:
            return
        else:
            server, port = ip.split(":")
            self.server = server
            self.port = int(port)

            print(self.server, self.port)

    def connect(self):
        '''
        Makes the initial connection to the
        host/server
        '''

        try:
            self.client.connect(self.addr)
            time.sleep(0.00001)
            return pickle.loads(self.client.recv(2048*12))
        except:
            pass
    
    def send(self, data):
        '''
        Sends and immediately receives data with the host/server.
        Data is sent as bytes through object serialization
        '''

        try:
            pa = time.time()
            self.client.send(pickle.dumps(data))
            r_data = pickle.loads(self.client.recv(2048*12))
            pb = time.time()

            ping = round((pb-pa)*10000)
            if ping > 1:
                self.ping = ping
                
            return r_data
        except socket.error as e:
            print(e)
