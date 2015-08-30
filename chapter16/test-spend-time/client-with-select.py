#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Select client.
"""

import sys
import select
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
    stdineof = False
    while True:
        rlist, wlist, xlist = select.select([sys.stdin, _socket], [], [], 1)
        for r in rlist:
            if r is sys.stdin:  # input is readable
                data = sys.stdin.readline()
                if stdineof:  # has read eof
                    continue
                if not data:
                    stdineof = True
                    _socket.shutdown(socket.SHUT_WR)  # send FIN
                else:
                    _socket.sendall(data)
            elif r is _socket:  # socket is readable
                data = _socket.recv(1024)
                if not data:
                    sys.exit(0)
                sys.stdout.write(data)

        if stdineof:  # end
            return


if __name__ == '__main__':
    main()
