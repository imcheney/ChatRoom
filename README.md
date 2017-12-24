A simple Python chatroom
========================

About
------------------------
A simple Python chatroom using socket and select

How select works in 7 lines of code
-----------------------------------
while 1:  # we want to read many messages all the time, so just keep looping...
    rlist, wlist, elist = select.select( [sock1, sock2], [], [], 5 )  # Await a read event for up to 5 sec
    if [rlist, wlist, elist] == [ [], [], [] ]:  # case for timeout
        print "Five seconds elapsed.\n"
    else:
        for sock in rlist:  # Loop through each socket in rlist, read and print the available data
            print sock.recv( 100 )

