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
