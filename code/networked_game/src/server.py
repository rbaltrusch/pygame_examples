# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:46:57 2021

@author: Korean_Crimson
"""
import socket
from _thread import start_new_thread

import config

# pylint: disable=invalid-name
# pylint: disable=global-statement
speed = "0,0"


def threaded_client(conn):
    """Tries to receive data from the client connection until the connection is
    terminated. Currently sends back the data received to all clients, unless
    the data received is equal to 'get', in which case it sends the last reply.
    """
    global speed

    conn.send(str.encode("Connected"))
    while True:
        try:
            data = conn.recv(config.CHUNKSIZE)
            if not data:
                print("Disconnected")
                break

            request_ = data.decode("utf-8")

            if request_.startswith("set:"):
                _, speed = request_.split(":")

            reply = speed
            print(f"Received {request_}. Sending: {reply}.")
            conn.sendall(str.encode(reply))
        except Exception as exc:
            raise exc

    print("Lost connection")
    conn.close()


def mainloop(socket_):
    """Accepts connections"""
    conn, addr = socket_.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))


def main():
    """Main function"""
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_.bind((config.SERVER_IP, config.PORT))
    socket_.listen(config.MAX_CLIENTS)
    print("Waiting for a connection, Server Started")
    while True:
        mainloop(socket_)


if __name__ == "__main__":
    main()
