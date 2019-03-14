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
    host = ''
    port = 12333
    
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
                print("data: ", repr(data))

if __name__ == "__main__":
    main() 