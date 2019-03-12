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
#recieve socket for robot A.
def robo_client(rSocket):
    while True:
        data = rSocket.recieve(512)
        #implement a break or exit
        list_of_data = data.decode(encoding='UTF-8',errors='ignore').split(" ")

#Configure recieve socket and thread.
def main(port, ipv4_address):
    socket_lock = _thread.allocate_lock()
    try:
        robo_socket = socket(AF_INET, SOCK_STREAM)
        robo_socket.bind((ipv4_address, int(port)))
    except:
        print("could not bind to address or port. Exiting.")
        sys.exit(1)
    robo_socket.listen(10)
    print("Server Started")
    print("listening for requests")

    while True:
	    connectionSocket, address = robo_socket.accept()
	    print("Accepted connection from: " + str(connectionSocket.getpeername()))
	    _thread.start_new_thread(robo_client, (connectionSocket,))
    robo_socket.close()

if __name__ == "__main__":
    #argument_1 = port, argument_2 = domain_name.
    main(sys.argv[1], sys.argv[2]) #robot_a