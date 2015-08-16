#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
select server.

TODO: use wlist
"""

import select
import socket

HOST = ''
PORT = 50008
LISTENNQ = 5


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(LISTENNQ)
    handle_connection(s)
    s.close()


def handle_connection(_socket):  # Handle the connection
    rlist = [_socket]
    while True:
        ready_rlist, wlist, xlist = select.select(rlist, [], [], 1)
        for r in ready_rlist:
            if r is _socket:  # New client connection
                conn, addr = r.accept()
                print 'Connected by {}'.format(addr)
                rlist.append(conn)
            else:
                str_echo(rlist, r)


def str_echo(rlist, conn):  # Process the request
    data = conn.recv(1024)
    if not data:
        rlist.remove(conn)
        conn.close()
    else:
        conn.sendall(data)


if __name__ == '__main__':
    main()
