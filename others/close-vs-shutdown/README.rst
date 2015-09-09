close vs shutdown
=================

问题
----

- close 和 shutdown 的区别是什么？分别适用于那些场景？
- close 是否会影响对端的使用情况，即：client 中调用 socket.close() 之后，server 的 send/recv 操作是否正常？

测试方案
--------

- 检查程序运行状况
- 查看程序运行时 tcp 连接的状态

运行程序 1
``````````

::

  $ python multi-process-server.py | python client-close.py

server 输出::

    Connected by  ('127.0.0.1', 38136)
    success recv
    data: Hello, world
    success send
    success recv
    data:

client 输出::

    closed
    Traceback (most recent call last):
      File "client-close.py", line 24, in <module>
        main()
      File "client-close.py", line 19, in main
        data = s.recv(1024)
      File "/usr/local/lib/python2.7/socket.py", line 170, in _dummy
        raise error(EBADF, 'Bad file descriptor')
    socket.error: [Errno 9] Bad file descriptor

因此：

- client 在调用 socket.close() 之后，无法再对 socket 进行操作（其实是描述符计数值为零）。
- server 在 client 发生 socket.close() 之后正常执行了 send/recv 操作，所以 **close 不会影响对端套接字的使用情况** 。

运行过程中 tcp 的连接状态::

    > lihang@lihang.aws.dev:~$ netstat -a | grep 50008
    tcp        0      0 *:50008                 *:*                     LISTEN
    tcp       12      0 localhost:50008         localhost:37834         ESTABLISHED
    tcp        0      0 localhost:37834         localhost:50008         ESTABLISHED

    > lihang@lihang.aws.dev:~$ netstat -a | grep 50008
    tcp        0      0 *:50008                 *:*                     LISTEN
    tcp        0      0 localhost:37834         localhost:50008         FIN_WAIT2
    tcp       13      0 localhost:50008         localhost:37834         CLOSE_WAIT

    > lihang@lihang.aws.dev:~$ netstat -a | grep 50008
    tcp        0      0 *:50008                 *:*                     LISTEN
    tcp       13      0 localhost:50008         localhost:37834         CLOSE_WAIT

    > lihang@lihang.aws.dev:~$ netstat -a | grep 50008
    tcp        0      0 *:50008                 *:*                     LISTEN


运行程序 2
```````````

::

  $ python multi-process-server.py | python client-shutdown.py

server 输出::

    Connected by  ('127.0.0.1', 38204)
    success recv
    data: Hello, world
    success send
    success recv
    data:

结果与 `程序 1` 结果一致。

client 输出::

    shut_wr
    shut_rd
    Received 'Hello, world'

这表明： **client 在调用 `s.shutdown(socket.SHUT_WR)` 之后成功执行后面的 recv 读操作。**

tcp 连接状态::

    > lihang@lihang.aws.dev:~$ netstat -a | grep 50008
    tcp        0      0 *:50008                 *:*                     LISTEN
    tcp       12      0 localhost:50008         localhost:38004         ESTABLISHED
    tcp        0      0 localhost:38004         localhost:50008         ESTABLISHED

    > lihang@lihang.aws.dev:~$ netstat -a | grep 50008
    tcp        0      0 *:50008                 *:*                     LISTEN
    tcp        0      0 localhost:37988         localhost:50008         FIN_WAIT2
    tcp        0      0 localhost:50008         localhost:37988         CLOSE_WAIT

    > lihang@lihang.aws.dev:~$ netstat -a | grep 50008
    tcp        0      0 *:50008                 *:*                     LISTEN
    tcp        0      0 localhost:50008         localhost:37988         CLOSE_WAIT

    > lihang@lihang.aws.dev:~$ netstat -a | grep 50008
    tcp        0      0 *:50008                 *:*                     LISTEN

tcp 连接状态与 `程序 1` 完全一致。

结论
----

- client 在调用 socket.close() 之后，无法再对 socket 进行操作（其实是因为描述符计数值为零）。
  server 在 client 发生 socket.close() 之后正常执行了 send/recv 操作，所以 **close 不会影响对端套接字的使用情况** 。
- 当只知道套接字读/写的某一个状态时，比如确定读操作完成，但写操作可能还没完成，这个时候就只能通过 shutdown 来关闭，
  因此 shutdown 在 I/O 复用场景中应用会比较多（I/O 复用中需要程序区分处理「可读/可写」事件）。

其他
----

有一处需要注意的是，输出中有两个同样的 TCP 四元组，即： `(localhost.50008, localhost.55553)` 。
有时候状态还不一样，比如： `FIN_WAIT2` `CLOSE_WAIT` 。
我的理解是它们都是同一个 tcp 连接，只不过一个是 client 角度，一个是 server 角度。
