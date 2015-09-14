#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Single process server.

print::

    Connected by  ('127.0.0.1', 53494)
    Connected by  ('127.0.0.1', 53495)
    Connected by  ('127.0.0.1', 53496)
"""

import socket

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
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
        conn.close()
    s.close()


if __name__ == '__main__':
    main()
