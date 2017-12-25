# -*- coding:utf-8 -*-
"""
server
"""
import socket
import select


def broadcast_data(sender_sock, message):
    """
    Function to broadcast chat messages to all connected clients
    :param sender_sock:
    :param message:
    :return: None
    """
    # Do not send the message to server's socket and the client who has send us the message
    for sock in conn_list:
        if sock != server_socket and sock != sender_sock:
            try:
                sock.send(message)
            except:
                # broken socket connection may be, chat client pressed ctrl+c for example
                sock.close()
                conn_list.remove(sock)
                continue


if __name__ == "__main__":
    conn_list = []  # List to keep track of socket descriptors
    RECV_BUFFER_SIZE = 4096  # Advisable to keep it as an exponent of 2
    PORT_NUM = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", PORT_NUM))
    server_socket.listen(10)
    conn_list.append(server_socket)  # Add server socket to the list of readable connections

    print "Chat server started on port " + str(PORT_NUM)

    while True:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(conn_list, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection received through server_socket
                new_sock, new_addr = server_socket.accept()
                conn_list.append(new_sock)
                print "Client (%s:%s) connected" % new_addr
                broadcast_data(new_sock, "(%s:%s) entered room\n" % new_addr)

            # Some incoming message from a client
            else:
                # Data received from client, process it
                try:
                    data = sock.recv(RECV_BUFFER_SIZE)
                    if data:
                        if data.strip() in ('exit' or 'quit'):
                            raise Exception
                        else:
                            broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
                except Exception as e:
                    broadcast_data(sock, "Client %s is offline\n" % sock)
                    print "Client %s is offline" % sock
                    sock.close()
                    conn_list.remove(sock)
                    continue

    server_socket.close()
