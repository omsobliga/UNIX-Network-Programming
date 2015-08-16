#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Multiple process server.
Fork one process after accept a connection.
Deal with SIGCHLD signo when child process exit.
"""

import os
import signal
import socket
import sys

HOST = ''
PORT = 50008
LISTENNQ = 5


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(LISTENNQ)
    signal.signal(signal.SIGCHLD, sig_chld_handler)

    while True:
        try:
            conn, addr = s.accept()
        except socket.error as e:  # Deal with slow system call
            print 'socket.error: {}'.format(e)
            continue

        print 'Connected by {}'.format(addr)
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


def sig_chld_handler(signo, frame):  # Process zombie child process
    while True:
        try:
            pid, exit_status = os.waitpid(-1, os.WNOHANG)
            print 'Child {} terminated'.format(pid)
        except OSError:  # No child process
            break


if __name__ == '__main__':
    main()
