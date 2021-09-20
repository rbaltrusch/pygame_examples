# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:46:57 2021

@author: Korean_Crimson
"""

import socket
from _thread import start_new_thread
import config

#pylint: disable=invalid-name

socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    socket_.bind((config.SERVER_IP, config.PORT))
except socket.error as e:
    str(e)

socket_.listen(config.MAX_CLIENTS)
reply = "0,0"
print("Waiting for a connection, Server Started")

def threaded_client(conn):
    """Tries to receive data from the client connection until the connection is
    terminated. Currently sends back the data received to all clients, unless
    the data received is equal to 'get', in which case it sends the last reply.
    """
    conn.send(str.encode("Connected"))
    while True:
        try:
            data = conn.recv(config.CHUNKSIZE)
            decoded = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break

            print("Received: ", decoded)
            global reply #pylint: disable=global-statement
            reply = decoded if decoded != 'get' else reply

            print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except Exception as e:
            raise e

    print("Lost connection")
    conn.close()

def main():
    """Main function"""
    conn, addr = socket_.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))

while True:
    main()
