# I/O 复用

chapter5 的程序都存在一个问题，客户端因为阻塞与 stdin.readline() 期间，如果服务器进程被杀死。

**TCP 服务器虽然正确给客户发送一个 FIN，但客户进程正阻塞与从标准输入读入的过程，
它无法看到 FIN，直到从套接字读时为止（可能过了很长时间）。
这样进程需要一种预先告知内核的能力，使得内核一旦内核一旦发现进程指定的一个或多个 I/O 条件就绪，
它就通知进程，这种能力称为 I/O 复用。**

下面主要实现 I/O 复用的两种场景：

- **当客户处理多个描述符（通常是交互式输入和网络套接字）。**
- **TCP 服务器即需要处理监听套接字，又需要处理已连接套接字。**

这两种情况，下面都有实现，分别对应： `client-with-select.py` 和 `server-with-select.py` 。

I/O 复用的主要实现是：select、poll 和 epoll。

## select/poll/epoll 的实现模型

### select 客户端模型

运行程序:

    > python server-with-socket.py | python client-with-select.py

然后关闭 server，client 会输出:

    > Server terminated prematurely

**所以即使 server.py 意外中断，client 也可通过 select 即使捕获服务端发来的 FIN 进行处理。**

### select 服务端模型

* `server-with-socket.py` 中主程序会阻塞在 accept() 函数，直到有 **已连接套接字** 可用。

* `server-with-select-completely.py` 中程序会阻塞在 select() 函数，
  **如果发现监听套接字（listenfd）就绪则创建新连接，发现已连接套接字（conn）就绪则进行数据传输**。

### poll 服务端模型

* `server-with-poll.py` 实现逻辑与 select 有些相似，只是套接字的存储形式不一样。
  需要在 Linux 环境下运行，Mac OS 没有 poll 环境。

### epoll 服务端模型

* `server-with-epoll.py` 代码与 poll 基本一样。

## select/poll/epoll 的区别

### select vs poll 主要区别

- select 采用 bit mask（位掩码）记录 fd 的状态，因此有长度限制。（依赖系统）
- poll 采用 pollfd array 记录 fd 状态，所以不再有长度限制。
- select 在各个系统上都有实现，移植性更好；poll/epoll 只在个别系统上有实现。

> poll() scales better because the system call only requires listing the file descriptors of interest,
> while select() builds a bitmap, turns on bits for the fds of interest,
> and then afterward the whole bitmap has to be linearly scanned again.
> select() is O(highest file descriptor), while poll() is O(number of file descriptors).

> From: https://docs.python.org/2/library/select.html#polling-objects

### poll vs epoll

详细分析参见：[poll vs epoll](./poll-vs-epoll)

## Reference:

- [Echo Server with Select](http://ilab.cs.byu.edu/python/select/echoserver.html)
- [select – Wait for I/O Efficiently](http://pymotw.com/2/select/)  # socket.close() 逻辑有误。
- [Python select library](https://docs.python.org/2/library/select.html)
- [What are the differences between poll and select?](http://stackoverflow.com/questions/970979/what-are-the-differences-between-poll-and-select)
- [epoll 或者 kqueue 的原理是什么？](http://www.zhihu.com/question/20122137/answer/14049112)
- [epoll(7) - Linux man page](http://linux.die.net/man/7/epoll)
- [epoll 边缘触发和水平触发的区别](http://blog.himdd.com/archives/3289)
