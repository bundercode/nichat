#!/usr/bin/env python

import socket

#
# hear_say.py
# 
#   small module to handle sending and recieving
#    data over Nichat sockets
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

MSG_SIZE = 1024 # Message buffer size

#
# Recieve and decode a message
#
def ni_hear(socket):

    message = socket.recv(MSG_SIZE).decode('UTF-8')
    return message

#
# Encode and send a message
#
def ni_say(socket, message):

    socket.send(bytes(str(message).encode('UTF-8')))
