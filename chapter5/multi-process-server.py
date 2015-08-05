#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Multiple process server.
Fork one process after accept a connection.

Output::

    Connected by  ('127.0.0.1', 53494)
    Connected by  ('127.0.0.1', 53495)
    Connected by  ('127.0.0.1', 53496)
"""

import os
import socket
import sys

HOST = ''
PORT = 50008
LISTENNQ = 5


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(LISTENNQ)
    while True:
        conn, addr = s.accept()
        print 'Connected by ', addr
        if (os.fork() == 0):
            s.close()  # Close listen fd, because child process need not listen event.
            str_echo(conn)
            conn.close()  # Close connected fd
            sys.exit(0)  # Clild process terminates
        conn.close()


def str_echo(conn):  # Process the request
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)


if __name__ == '__main__':
    main()
