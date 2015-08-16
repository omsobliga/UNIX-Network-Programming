I/O 复用
========

chapter5 的程序都存在一个问题，客户端因为阻塞与 stdin.readline() 期间，如果服务
器进程被杀死。

**TCP 服务器虽然正确给客户发送一个 FIN，但客户进程正阻塞与从标准输入读入的过程，
它无法看到 FIN，直到从套接字读时为止（可能过了很长时间）。
这样进程需要一种预先告知内核的能力，使得内核一旦内核一旦发现进程指定的一个或
多个 I/O 条件就绪，它就通知进程，这种能力称为 I/O 复用。**

下面主要实现 I/O 复用的两种场景：

- **当客户处理多个描述符（通常是交互式输入和网络套接字）。**
- **TCP 服务器即需要处理监听套接字，又需要处理已连接套接字。**

这两种情况，下面都有实现，分别对应： ``client-with-select.py`` 和 ``server-with-select.py`` 。

I/O 复用的主要实现是 select 和 poll。

select 客户端模型
-----------------

运行程序::

    > python server-with-socket.py | python client-with-select.py

然后关闭 server，client 会输出::

    > Server terminated prematurely

**所以即使 server.py 意外中断，client 也可通过 select 即使捕获服务端发来的 FIN 进行处理。**

client 读写文件版本： ``client-read-file.py``

select 服务端模型
-----------------

``server-with-socket.py`` 中主程序会阻塞在 accept() 函数，直到有
**已连接套接字** 可用。

``server-with-select.py`` 中程序会阻塞在 select() 函数，如果发现监听套接字
（listenfd）就绪则创建新连接，发现已连接套接字（conn）就绪则进行数据传输。

运行程序::

    > python server-with-select.py | python client-with-select.py | python client-with-select.py

TODO
----

- select 中 wlist 和 xlist 的使用。
- poll 服务端模型。

Ref:
----

- http://ilab.cs.byu.edu/python/select/echoserver.html
- http://pymotw.com/2/select/
- https://docs.python.org/2/library/select.html
- http://www.cnblogs.com/Anker/p/3265058.html
- http://blog.csdn.net/lizhiguo0532/article/details/6568964
