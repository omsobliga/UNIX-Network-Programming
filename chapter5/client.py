#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time

HOST = ''
PORT = 50008


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall('Hello, world')
    data = s.recv(1024)
    print 'Received', repr(data)
    time.sleep(5)
    s.sendall('Hello, world')
    data = s.recv(1024)
    print 'Received', repr(data)
    s.close()


if __name__ == '__main__':
    main()
