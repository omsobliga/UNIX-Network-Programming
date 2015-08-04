Make Test
=========

单进程服务器模型
----------------

运行程序::

  $ python multi-process-server.py | python client.py
  $ netstat -a | grep 5007

输出状态::

  Proto Recv-Q Send-Q  Local Address          Foreign Address        (state)
  tcp4       0      0  localhost.50007        localhost.55553        ESTABLISHED
  tcp4       0      0  localhost.55553        localhost.50007        ESTABLISHED
  tcp4       0      0  *.50007                *.*                    LISTEN
  ...

- LISTEN 表示 server 主进程处于监听状态。
- 第一个 ESTABLISHED 表示 server 子进程正在进行请求处理。
- 第二个 ESTABLISHED 表示 client 已经与 server 建立连接，并进行数据通信。


并发服务器模型
--------------

未处理 SIGCHLD 信号
```````````````````

运行程序::

 $ python multi-process-server.py | python client.py
 $ ps -t ttys001 -o pid,ppid,tty,stat,args,wchan

输出状态::

  PID  PPID TTY      STAT ARGS                           WCHAN
  22098 18210 ttys001  S+   python multi-process-server.py -
  22113 22098 ttys001  Z+   (python)                       -
  22119 22098 ttys001  Z+   (python)                       -
  22227 22098 ttys001  Z+   (python)                       -

第一个表示主进程的状态，后面三个 STAT 为 ``Z+`` 表示僵死的子进程。服务器子进程终止时，给父进程发送一个 SIGCHLD 信号，如果父进程未加处理，子进程就会进入僵死状态。

处理 SIGCHLD 信号
`````````````````

运行程序::

 $ python multi-process-server-with-signal.py | python client.py
 $ ps -t ttys001 -o pid,ppid,tty,stat,args,wchan

输出状态::

  PID  PPID TTY      STAT ARGS                           WCHAN
  22098 18210 ttys001  S+   python multi-process-server.py -

不再有 ``Z+`` 僵死的子进程，在编写网络编程时需要注意：

1. 当 fork 子进程时，必须捕获 SIGCHLD 信号；
2. 当捕获信号时，必须处理被中断的系统调用；（slow system call）
3. SIGCHLD 的信息处理函数必须正确编写，应使用 waitpid 函数以免留下僵死进程。


QA
``

1. strace 观察 server.py 的内部执行状态？
2. 为什么子进程 exit 之后不直接回收资源，而需要发送 SIGCHLD 通知父进程进行回收？
3. signal handler 和 slow system call 是如何相互影响的？


Reference:
``````````
