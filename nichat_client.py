#!/usr/bin/env python

import select
import socket
import sys
from hear_say import ni_hear, ni_say

#
# nichat_client.py
#
#   usage: ./nichat_client.py [hostname] [port]
#
#   Module containing the NichatClient class.
#    It takes two optional arguements, either
#    just a hostname, or a hostname followed 
#    by a port number.
#
# AUTHOR: Brandon Smith - smitbl07@students.ipfw.edu
#   IPFW CS350 Spring 2014
#   Professor Liu
#   Project 2
#   Due: March 4, 2014
#
# The name 'Nichat' is inspired by the "Knights who say Ni"
#  from "Monty Python and the Holy Grail."  I find it
#  fitting since the origin of the name 'Python' comes
#  from Monty Python.
#

class NichatClient():
    """Client for Nichat"""
    #
    # Initiate NichatClient class
    #
    def __init__(self, server='localhost', port=8888):

        sys.stdout.write("\nEnter name: ")
        self.name = sys.stdin.readline().strip()
        self.server = server
        self.port = int(port)

    #
    # Connect to a Nichat server
    #
    def ni_connect(self):
	
        # Attempts to open a socket and connect to a Nichat server
        try:
            self.ni_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ni_socket.connect((self.server, self.port))
        except OSError as err:
            if self.ni_socket:
                self.ni_socket.close()
            print ("\nERROR: ", err.errno)
            sys.exit(err.errno)
        
        ni_say(self.ni_socket, self.name) # Send name to server

    #
    # Send user input and recieve server output
    #
    def ni_session(self):

        self.ni_connect()
        connected =1

        while (connected):
            sys.stdout.write('> ')
            sys.stdout.flush()

            good_inputs, good_outputs, good_excepts = select.select([0, self.ni_socket], [], [])

            # Loop between user input and socket output
            for in_src in good_inputs:
                
                if in_src == 0:
                    message = sys.stdin.readline().strip()
                    if message:
                        ni_say(self.ni_socket, message)
                
                elif in_src == self.ni_socket:
                    message = ni_hear(self.ni_socket)
                    if message:
                        sys.stdout.write(message + '\n')
                        sys.stdout.flush()
                    else:
                        print ('Cutting connection...')
                        connected =0
                        break

        self.ni_socket.close()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        ni_client = NichatClient(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        ni_client = NichatClient(sys.argv[1])
    else:
        ni_client = NichatClient()
    ni_client.ni_session()
