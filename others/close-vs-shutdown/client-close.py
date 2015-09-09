#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket

HOST = ''
PORT = 50008


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall('Hello, world')
    time.sleep(5)
    s.close()
    print 'closed'
    time.sleep(5)
    data = s.recv(1024)
    print 'Received', repr(data)


if __name__ == '__main__':
    main()
