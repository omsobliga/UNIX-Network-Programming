#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Select client.
"""

import os
import sys
import signal
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
    if (os.fork() == 0):
        while True:
            data = _socket.recv(1024)
            if data:
                _socket.sendall(data)
            else:
                break
        os.kill(os.getpid(), signal.SIGTERM)

    while True:
        data = sys.stdin.readline(1024)
        if data:
            sys.stdout.write(data)
        else:
            break

    _socket.shutdown(socket.SHUT_WR)
    return


if __name__ == '__main__':
    main()
