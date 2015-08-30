#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Refelecting client
"""

import sys
import socket
import time

HOST = ''
PORT = 50008


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    start_time = time.time()
    str_cli(s)
    end_time = time.time()
    print 'spend time={}'.format(end_time - start_time)
    s.close()


def str_cli(_socket):
    while True:
        data = sys.stdin.readline()
        if not data:
            break
        _socket.sendall(data)
        data = _socket.recv(1024)
        sys.stdout.write(data)


if __name__ == '__main__':
    main()
