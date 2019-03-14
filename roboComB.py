from socket import *
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
def main(port, ipv4_address):
    try:
        robo_socket = socket(AF_INET, SOCK_STREAM)
        robo_socket.connect((ipv4_address, int(port)))
    except:
        print("could not connect to host. Exiting.")
        sys.exit(1)
    robo_socket.sendall("le'derp".encode())
    #robo_socket.sendall("end".encode())
    

if __name__ == "__main__":
    robot_a_IP = 'localhost'
    robot_a_port = 12333
    main(robot_a_port, robot_a_IP) #robot_B