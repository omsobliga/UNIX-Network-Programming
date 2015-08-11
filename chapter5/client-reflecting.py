#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Refelecting client
"""

import socket

HOST = ''
PORT = 50008


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    str_cli(s)
    s.close()


def str_cli(_socket):
    while True:
        data = raw_input('> ')
        if not data:
            break
        _socket.sendall(data)
        data = _socket.recv(1024)
        print 'Received', repr(data)


if __name__ == '__main__':
    main()
