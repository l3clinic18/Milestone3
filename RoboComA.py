"""
simple unthreaded socket communication dedicated to recieve data from another robot.
"""
import socket
from urllib.parse import urlparse
import urllib.request
import json
import hashlib
import requests
import sys
import _thread

recieve_data = []
send_data = []

#Configure recieve socket and thread.
def main():
    """
    Unthreaded will start a server and wait (blocking) until another robot connects to it and recieves data
    from the remote robot.
    Args:
    Returns:
        dist_data (float): distance data from the base station to the target.
    """
    host = ''
    port = 12333
    dist_data = 0.0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as r_socket:
        r_socket.bind((host, port))
        r_socket.listen(2)
        print("Server Started")

        connectionSocket, address = r_socket.accept()
        with connectionSocket:
            while True:
                print("Accepted connection from: " + str(connectionSocket.getpeername()))
                data = connectionSocket.recv(1024)
                if not data: break
                print("data: ", repr(data.decode()))
                dist_data = float(data.decode())
    return dist_data

if __name__ == "__main__":
    main() 
