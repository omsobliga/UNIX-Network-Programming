非阻塞式 I/O
============

非阻塞读和写
------------

chapter6 中的 client-with-select.py 使用了阻塞式 I/O，如果在标准输入有一行文本
可读，就调用 read 读入它，再调用 write 把它发送给服务器。然而如果套接字发送缓冲
区已满，write 调用就会阻塞。 **在进程阻塞于 write 调用期间，可能有来自套接字
接收缓冲区的数据可供读取。**

有两种方案可以解决这个问题：

1. 使用非阻塞 read/write，引入缓冲区管理。
2. 分离套接字的读写操作到不同的进程。

第一种方案由于引入了缓冲区管理，会使程序变得很复杂。第二种方案由于分离套接字 
read/write 操作到不同进程，由于可在不同进程独立运行，使得 read/write 发生阻塞后
降低对整体造成的影响（等待）。

测试不同 str_cli 的运行时间：
`````````````````````````````
在 test-spend-time 文件执行::

    cat data.in | python client-reflecting.py > client-reflecting.out
    cat data.in | python client-with-select.py > client-with-select.out
    cat data.in | python ../client-fork-read.py > client-fork-read.out

其中 data.in 中存放 1w 行数据，可以看到运行时间分别为::

    spend time=0.541697978973
    spend time=0.218165159225
    spend time=0.011971950531

非阻塞 connect
--------------

当在一个非阻塞的 TCP 套接字上调用 connect 时，connect 将立即放回一个 EINPROGRESS
错误，不过已经发起的 TCP 三路握手继续进行。接着通过 select 检测这个连接是否成功建立。

由于完成一个 connect 需要花费 RTT 时间，当程序需要访问多次，比如：Web 访问需要
连续加载多个页面时，通过非阻塞 connect 可以使连接并行执行。

非阻塞 accept
-------------

accept 函数由 TCP 服务器调用，用于从已完成连接队列队头返回下一个已完成连接。如果
已完成连接队列为空，那么进程被投入睡眠。

在 chapter6 中，通过 select 通知程序监听的套接字上是否已有连接就绪，因此随后的
accept 调用就不再需要阻塞。
