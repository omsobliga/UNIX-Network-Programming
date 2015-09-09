#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Single process server.
"""

import time
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
            time.sleep(10)
            data = conn.recv(1024)
            print 'success recv'
            print 'data: {}'.format(data)
            if not data:
                break
            conn.sendall(data)
            print 'success send'
        conn.close()
    s.close()


if __name__ == '__main__':
    main()
