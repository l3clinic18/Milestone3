from socket import *
from urllib.parse import urlparse
import urllib.request
import json
import hashlib
import requests
import sys
import _thread
import decawave

recieve_data = []
send_data = []

#Configure recieve socket and thread.
def send_(port, ipv4_address, deca_data):
    try:
        robo_socket = socket(AF_INET, SOCK_STREAM)
        robo_socket.connect((ipv4_address, int(port)))
    except:
        print("could not connect to host. Exiting.")
        sys.exit(1)
    print(str(deca_data).encode())
    robo_socket.sendall(str(deca_data).encode())
    #robo_socket.sendall("end".encode())