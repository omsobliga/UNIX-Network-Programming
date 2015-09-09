基本 TCP 套接字函数
===================

socket 函数
-----------

`socket.socket([family[, type[, proto]]])`

创建新的套接字。

* family 表示套接字采用什么协议，其中：socket.AF_INET 表示 IPv4。
* type 表示套接字类型，其中：SOCK_STREAM 表示字节流套接字。

connect 函数
------------

`socket.connect(address)`

TCP 客户用 connect 函数来建立与 TCP 服务器的连接。

调用 connect 函数将触发 TCP 的三次握手过程，仅在连接建立成功或出错时才返回。
默认为阻塞状态，需要等待 RTT 才能返回。

bind 函数
---------

`socket.bind(address)`

把一个本地协议地址赋予一个套接字。

listen 函数
-----------

`socket.listen(backlog)`

监听套接字上的连接，backlog 表示套接字排队的最大连接个数。

内核为任何一个给定的监听套接字维护两个队列：

1. 未完成连接队列，客户发出 SYN 并且到达服务器，服务器正在等待完成相应的 TCP 三次握手。
2. 已完成连接队列，完成三次握手。

accept 函数
-----------

`socket.accept()`

用于从已完成连接队列队头返回下一个已完成连接。

close 函数
----------

`socket.close()`

把该套接字标记成关闭，该套接字描述符不能再被调用进程使用，即：read/write。
**如果在并发服务器中使用只是导致相应描述符的引用计数值减 1， 如果引用计数值仍大于 0，
这个 close 调用不会引发 TCP 的四分组连接终止序列。意味着改套接字在其他进程中仍可被正常使用。**

shutdown 函数
-------------

`socket.shutdown(how)`

对套接字只关闭读或写，或者读写都关闭。分别对应参数： `SHUT_RD` `SHUT_WR` `SHUT_RDWR` 。

关于 close 和 shutdown 的比较，参考： `socket close vs shutdown <../others/close-vs-shutdown>`_
