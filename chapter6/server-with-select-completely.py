#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Select server.

Complete 版本。
"""

import Queue
import select
import socket

HOST = ''
PORT = 50008
LISTENNQ = 5


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(LISTENNQ)
    handle_connection(s)
    s.close()


def handle_connection(_socket):  # Handle the connection
    rlist = [_socket]  # read list
    wlist = []  # write list
    message_queues = {}
    while True:
        ready_rlist, ready_wlist, exception_list = select.select(rlist, wlist, rlist, 1)

        # Handle ready rlist
        for r in ready_rlist:
            if r is _socket:
                conn, addr = r.accept()  # Create new client connection
                print 'Connected by {}'.format(addr)
                rlist.append(conn)
                # Save the data we want to send in same conn
                message_queues[conn] = Queue.Queue()
            else:
                data = r.recv(1024)
                if not data:
                    rlist.remove(r)  # 数据已接受完
                else:
                    message_queues[r].put(data)
                    # Start listening writable in conn
                    if r not in wlist:
                        wlist.append(r)

        # Handle ready wlist
        for w in ready_wlist:
            try:
                data = message_queues[w].get_nowait()
            except Queue.Empty:
                # Stop listening writable in conn
                wlist.remove(w)
                if w not in rlist:  # 可确保所有 data 都已经发送完
                    w.close()
                    del message_queues[w]
            else:
                w.sendall(data)

        # Handle exception list
        for e in exception_list:
            rlist.remove(e)
            if e in wlist:
                wlist.remove(e)
            e.close()

            del message_queues[e]


if __name__ == '__main__':
    main()
