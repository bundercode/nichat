#!/usr/bin/env python

import select
import socket
import sys
import threading
from hear_say import ni_hear, ni_say

#
# nichat_server.py
#
#   usage: ./nichat_server.py [port]
#
#   Module containing the NichatServer class.
#    It takes one optional arguement, a port 
#    number for the server to bind to.
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

class NichatServer():
    """Server for Nichat"""

    #
    # Initiate NichatServer class
    #
    def __init__(self, port=8888):

        self.port = int(port)
        self.ni_threads = []

    #
    # Create socket, bind to port, and listen for client connections
    #
    def open_socket(self):

        # Attempts to open socket, bind to port, and listen for clients
        try:
            self.ni_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ni_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.ni_socket.bind(('', self.port))
            self.ni_socket.listen(10)
        except OSError as err:
            if self.ni_socket:
                self.ni_socket.close()
            print ("\nERROR: ", err.errno)
            sys.exit(err.errno)

    #
    # Recieve new clients and create a new thread for each
    #
    def ni_serve(self):

        self.open_socket()
        server_running =1

        print ('\nServer running...\n')
        while (server_running):

            # Select between new clients and the stdin
            try:
                good_inputs, good_outputs, good_excepts = select.select([self.ni_socket, sys.stdin], [], [])
            except OSError as err:
                print ("\nERROR: ", err.errno)
                sys.exit(err.errno)
            except OSError as err:
                print ("\nERROR: ", err.errno)
                sys.exit(err.errno)

            # Loop between the server socket and the stdin
            for in_src in good_inputs:

                # Add a new client
                if in_src == self.ni_socket:

                    new_client = self.CliThread(self, self.ni_socket.accept())
                    new_client.start()
                    self.ni_threads.append(new_client)
                    print ('[ New client joined ]')

                # Shutdown server upon recieving keyboard input
                elif in_src == sys.stdin:

                    kill_sig = sys.stdin.readline()
                    server_running =0
                    break

        # Close server socket and client threads
        print ('\nServer stopping...\n')
        self.ni_socket.close()
        for c in self.ni_threads:
            c.join()

    #
    # Subclass of threading.Thread
    #
    class CliThread(threading.Thread):
        """Nichat client thread"""

        #
        # Initiate CliThread class
        #
        def __init__(self, server, accepted):

            threading.Thread.__init__(self)
            self.server = server
            self.client, self.address = accepted
            self.name = ni_hear(self.client)

            for c in self.server.ni_threads:
                ni_say(c.client, '[ <' + self.name + '> has joined ]')

        #
        # Recieve client input and send to all other clients
        #
        def run(self):

            thread_running =1

            while (thread_running):

                message = ni_hear(self.client)
                # Send message to all other clients
                if message:
                    if message == '/quit':
                        message = '[ <' + self.name + '> has left ]'
                        thread_running =0
                    else:
                        message = '<' + self.name + '> ' + message
                    
                    for c in self.server.ni_threads:
                        ni_say(c.client, message)

                else: # Socket closed
                    thread_running =0            

            self.server.ni_threads.remove(self)
            self.client.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ni_server = NichatServer(sys.argv[1])
    else:
        ni_server = NichatServer()
    ni_server.ni_serve()
