# -*- coding:utf-8 -*-
"""
client
"""

import socket
import select
import sys

RECV_BUFFER_SIZE = 4096


def prompt_prefix():
    """
    print a <You> prefix on screen
    :return: None
    """
    sys.stdout.write('<You> ')
    sys.stdout.flush()


def get_connection(host_IP, port_num):
    """
    client根据服务器IP:port创建客户端的一个连接socket
    :param host_IP:
    :param port_num:
    :return: socket fd for client's connection with server
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4
    sock.settimeout(2)
    # connect to remote host
    try:
        sock.connect((host_IP, port_num))
    except:
        print 'Unable to connect'
        sys.exit()
    print 'Connected to remote host. Start sending messages'
    return sock


def keep_chatting():
    """
    an infinite loop for user's chat
    :return: None
    """
    while True:
        rlist = [sys.stdin, client_sock]  # input comes from either keyboard or client socket fd

        # Get the list sockets which are readable
        read_list, write_list, error_list = select.select(rlist, [], [])

        for sock in read_list:
            # incoming message from remote server
            if sock == client_sock:
                data = sock.recv(RECV_BUFFER_SIZE)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data)
                    prompt_prefix()

            # user entered a message
            else:
                msg = sys.stdin.readline()
                client_sock.send(msg)
                prompt_prefix()


# main function
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Usage : python telnet.py hostname port'
        sys.exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
    client_sock = get_connection()
    prompt_prefix()
    keep_chatting()
