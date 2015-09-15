#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Select server.

Complete 版本。

L54 和 L70 都进行了 close 操作。
如果只有 L54：当 server 发现 recv 为空，且 message_queue 数据还没发送完，将无法进行 close。
如果只有 L70：当 server 直接接收到一个 FIN 导致 recv 为空，将无法执行 L70 的 close。
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
        # 阻塞在这里，直到发现 ready 的 fd
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
                    # Stop listening readable in conn
                    rlist.remove(r)
                    if r not in wlist:  # 数据已接受完，且不再需要 send 操作
                        del message_queues[r]
                        r.close()
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
                if w not in rlist:  # 数据都已经发送完且不再 recv 新的数据
                    del message_queues[w]
                    w.close()
            else:
                w.sendall(data)

        # Handle exception list
        for e in exception_list:
            if e in rlist:
                rlist.remove(e)
            if e in wlist:
                wlist.remove(e)
            del message_queues[e]
            e.close()


if __name__ == '__main__':
    main()
