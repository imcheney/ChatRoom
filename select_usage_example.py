# -*- coding: utf-8 -*-
"""
select module's usage example
"""
import socket
import select

sock1 = socket.socket()
sock2 = socket.socket()

sock1.connect(('127.0.0.1', 5000))
sock2.connect(('127.0.0.1', 5000))

while True:  # we want to read many messages all the time, so just keep looping...
    rlist, wlist, elist = select.select([sock1, sock2], [], [], 5)  # Await a read event for up to 5 sec
    if [rlist, wlist, elist] == [[], [], []]:  # case for timeout
        print "Five seconds elapsed.\n"
    else:
        for sock in rlist:  # Loop through each socket in rlist, read and print the available data
            print sock.recv(100)
