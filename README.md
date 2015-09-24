# UNIX Network Programming

书中原程序是通过 C 实现，这里采用 Python 实现一遍，按 chapter 进行分类。同时加入一些自己的理解。

## 各章节内容

### chapter4

- 基本套接字函数

### chapter5

- TCP 客户/服务器程序示例

  - 基础并发服务器模型
  - 僵死进程和 SIGCHLD 信号的处理

### chapter6

- I/O 复用

  - select 版本的 client
  - select/poll/epoll 版本的 server
  - select/poll/epoll 的区别

### chapter16

- 非阻塞 I/O

  - 非阻塞 read/write
  - 非阻塞 connect
  - 非阻塞 accept

### others

- close vs shutdown
- poll vs epoll

## TODO

- 网络模型的发展
