#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Select client.
"""

import sys
import select
import socket

HOST = ''
PORT = 50008


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    str_cli(s)
    s.close()


def str_cli(_socket):
    stdineof = False
    read_fd = open('read.txt', 'r')
    write_fd = open('write.txt', 'w')
    while True:
        readable, writable, exceptional = select.select([read_fd, _socket], [], [], 1)
        for r in readable:
            if r is read_fd:  # file is readable
                data = read_fd.readline()
                if stdineof:  # has read eof
                    continue
                if not data:  # first read eof
                    print 'End input.'
                    stdineof = True
                    _socket.shutdown(socket.SHUT_WR)  # send FIN
                else:
                    _socket.sendall(data)
            elif r is _socket:  # socket is readable
                data = _socket.recv(1024)
                if not data:
                    print 'Server terminated prematurely'
                    sys.exit(0)
                write_fd.write(repr(data))


if __name__ == '__main__':
    main()
