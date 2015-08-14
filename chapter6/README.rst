I/O 复用
========

chapter5 的程序都存在一个问题，如果 server 终止，客户端因为阻塞与 stdin.readline()，所以无法马上得到通知。

**当客户端需要处理多个描述符时，就需要用到 I/O 复用。** 内核一旦发现进程指定的一个或多个 I/O 条件就绪，它就通知进程，这种能力称为 I/O 复用。

I/O 复用的主要实现是 select 和 poll。

select 客户端模型
-----------------

运行程序::

    > python server-with-socket.py | python client.py

然后关闭 server，client 会输出::

    > Server terminated prematurely


TODO
----

- shutdown 怎么测试生效？
