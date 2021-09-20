# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:46:57 2021

@author: Korean_Crimson
"""

import socket
import config

class Network:
    """Class used to connect to the server"""

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = config.SERVER_IP
        self.port = config.PORT
        self.addr = (self.server, self.port)
        self.id = self.connect() #pylint: disable=invalid-name

    def connect(self):
        """Sends its address to the server and receives the server response"""
        try:
            self.client.connect(self.addr)
            return self.client.recv(config.CHUNKSIZE).decode()
        except:
            print('failed')

    def send(self, data):
        """Sends the data (str) and returns the server response (str)"""
        try:
            self.client.send(str.encode(data))
            return self.client.recv(config.CHUNKSIZE).decode()
        except socket.error as exc:
            print(exc)
