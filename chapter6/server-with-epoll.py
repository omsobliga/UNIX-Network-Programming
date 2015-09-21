#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Epoll server.

实现基本与 poll 一致。
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
    message_queues = {}  # 记录不同 socket 将要要发送的数据
    socket_eofs = {}  # 记录不同 socket 是否接受了 EOF

    # 初始化事件集
    READ_ONLY = select.EPOLLIN | select.EPOLLPRI | select.EPOLLHUP | select.EPOLLERR
    WRITE_ONLY = select.EPOLLOUT
    READ_WRITE = READ_ONLY | WRITE_ONLY

    # 初始化 poll 对象
    poller = select.epoll()
    poller.register(_socket, READ_ONLY)

    # fd 与 socket 的映射
    fd_to_socket = {_socket.fileno(): _socket}

    while True:
        # 阻塞在这里，直到发现 ready 的 fd
        polls = poller.poll()

        for fd, event in polls:
            s = fd_to_socket[fd]

            # Handle ready readfd
            if event & (select.EPOLLIN | select.EPOLLPRI):

                if s is _socket:
                    conn, addr = s.accept()  # Create new client connection.
                    print 'Connected by {}'.format(addr)

                    poller.register(conn, READ_ONLY)
                    fd_to_socket[conn.fileno()] = conn

                    # Save the data we want to send in same conn.
                    message_queues[conn] = Queue.Queue()
                else:
                    data = s.recv(1024)
                    if not data:
                        # 数据已接受完，且不再需要 send 操作
                        if s not in message_queues or not message_queues[s].qsize:
                            # Remove a file descriptor being tracked by a polling object.
                            poller.unregister(s)
                            del message_queues[s]
                            s.close()
                        else:
                            socket_eofs[s] = True
                    else:
                        message_queues[s].put(data)
                        # Modifies fd's eventmask to READ_WRITE.
                        poller.modify(s, READ_WRITE)

            # Handle ready writefd
            elif event & select.EPOLLOUT:
                try:
                    data = message_queues[s].get_nowait()
                except Queue.Empty:
                    # 数据都已经发送完且不再 recv 新的数据
                    if s in socket_eofs and socket_eofs[s]:
                        # Remove a file descriptor being tracked by a polling object.
                        poller.unregister(s)
                        del message_queues[s]
                        s.close()

                    # Modifies fd's eventmask to READ_ONLY.
                    poller.modify(s, READ_ONLY)
                else:
                    s.sendall(data)

            # Handle ready exceptfd
            elif event & select.EPOLLERR:
                poller.unregister(s)
                del message_queues[s]
                s.close()


if __name__ == '__main__':
    main()
