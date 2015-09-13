# close vs shutdown

## 问题

* close 和 shutdown 的区别是什么？分别适用于那些场景？
* close 是否会影响对端的使用情况，即：client 中调用 socket.close() 之后，server 的 send/recv 操作是否正常？

## 测试方案

* 检查程序运行状况
* 查看程序运行时 tcp 连接的状态

### 运行程序 1

    $ python multi-process-server.py | python client-close.py

server 输出:

    Connected by  ('127.0.0.1', 38136)
    success recv
    data: Hello, world
    success send
    success recv
    data:

client 输出:

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

* client 在调用 socket.close() 之后，无法再对 socket 进行操作（其实是描述符计数值为零）。
* server 在 client 发生 socket.close() 之后正常执行了 send/recv 操作，所以 *close 不会影响对端套接字的使用情况* 。

运行过程中 tcp 的连接状态:

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


### 运行程序 2

::

  $ python multi-process-server.py | python client-shutdown.py

server 输出结果与 `程序 1` 结果一致。

client 输出:

    shut_wr
    shut_rd
    Received 'Hello, world'

tcp 连接状态也与 `程序 1` 完全一致。

### 观察发现

- client 在调用 socket.close() 之后，无法再对 socket 进行操作（ **多进程不一定，因为描述符计数值可能不为零** ）。
- client 在调用 socket.shutdown(socket.SHUT_WD) 之后，可以继续进行 recv 操作。
- server 在 client 发生 socket.close() 之后正常执行了 send/recv 操作，所以 **close 不会影响对端套接字的使用情况** 。

## 主要区别

> Big difference between shutdown and close on a socket is the behavior when the socket is shared by other processes.
> A shutdown() affects all copies of the socket while close() affects only the file descriptor in one process.


## 使用建议

> 1. Always shutdown before close when possible.
> 2. If you finished receiving (0 size data received) before shutdown,
> close the connection after the last send finishes.
> 3. If you want to close the connection normally, shutdown the connection,
> and wait until you receive a 0 size data, and then close the socket.
> 4. In any case, if timed out or any other error occured simply close the socket.


## 其他

有一处需要注意的是，输出中有两个同样的 TCP 四元组，即： `(localhost.50008, localhost.55553)` 。
有时候状态还不一样，比如： `FIN_WAIT2` `CLOSE_WAIT` 。
我的理解是它们都是同一个 tcp 连接，只不过一个是 client 角度，一个是 server 角度。

## Reference:

* [Big difference between shutdown and close on a socket](http://stackoverflow.com/questions/4160347/close-vs-shutdown-socket#comment4491371_4160356)
* [close vs shutdown socket?](http://stackoverflow.com/a/26877667/3175815)
