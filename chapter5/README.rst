程序介绍
========

并发服务器模型
--------------

运行程序::

  $ python multi-process-server.py | python client.py
  $ netstat -a | grep 50008

输出状态::

  Proto Recv-Q Send-Q  Local Address          Foreign Address        (state)
  tcp4       0      0  localhost.50008        localhost.55553        ESTABLISHED
  tcp4       0      0  localhost.55553        localhost.50008        ESTABLISHED
  tcp4       0      0  *.50008                *.*                    LISTEN
  ...

- LISTEN 表示 server 主进程处于监听状态。
- 第一个 ESTABLISHED 表示 server 子进程正在进行请求处理。
- 第二个 ESTABLISHED 表示 client 已经与 server 建立连接，并进行数据通信。


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

第一个表示主进程的状态，后面三个 STAT 为 ``Z+`` 表示僵死的子进程。服务器子进程终止时，
给父进程发送一个 SIGCHLD 信号，如果父进程未加处理，子进程就会进入僵死状态。

处理 SIGCHLD 信号
`````````````````

运行程序::

 $ python multi-process-server-with-signal.py | python client.py
 $ ps -t ttys001 -o pid,ppid,tty,stat,args,wchan

输出状态::

  PID  PPID TTY      STAT ARGS                           WCHAN
  22098 18210 ttys001  S+   python multi-process-server.py -

可以看到不再有 ``Z+`` 僵死的子进程。

在编写网络编程时需要注意：

1. 当 fork 子进程时，必须捕获 SIGCHLD 信号；
2. 当捕获信号时，必须处理被中断的系统调用；（slow system call）
3. SIGCHLD 的信息处理函数必须正确编写，应使用 waitpid 函数以免留下僵死进程。

通过 ``strace`` 观察 ``multi-process-server-with-signal.py`` 的执行情况为::

  26582 accept(3, {sa_family=AF_INET, sin_port=htons(49357), sin_addr=inet_addr("127.0.0.1")}, [16]) = 4
  26582 fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 3), ...}) = 0
  26582 mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f26c86d3000
  26582 write(1, "Connected by ('127.0.0.1', 49357"..., 34) = 34
  26582 clone(child_stack=0, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x7f26c86c59d0) = 26982
  26582 close(4)                          = 0
  26582 accept(3,  <unfinished ...>
  26982 close(3)                          = 0
  26982 recvfrom(4, "Hello, world", 1024, 0, NULL, NULL) = 12
  26982 sendto(4, "Hello, world", 12, 0, NULL, 0) = 12
  26982 recvfrom(4, "Hello, world", 1024, 0, NULL, NULL) = 12
  26982 sendto(4, "Hello, world", 12, 0, NULL, 0) = 12
  26982 recvfrom(4, "", 1024, 0, NULL, NULL) = 0
  26982 close(4)                          = 0
  26982 rt_sigaction(SIGINT, {SIG_DFL, [], SA_RESTORER, 0x7f26c7ec7030}, {0x7f26c8206b70, [], SA_RESTORER, 0x7f26c7ec7030}, 8) = 0
  26982 rt_sigaction(SIGCHLD, {SIG_DFL, [], SA_RESTORER, 0x7f26c7ec7030}, {0x7f26c8206b70, [], SA_RESTORER, 0x7f26c7ec7030}, 8) = 0
  26982 exit_group(0)                     = ?
  26582 <... accept resumed> 0x7fffffc3fa90, [16]) = ? ERESTARTSYS (To be restarted)
  26582 --- SIGCHLD (Child exited) @ 0 (0) ---
  26582 rt_sigreturn(0xffffffff)          = -1 EINTR (Interrupted system call)
  26582 wait4(-1, [{WIFEXITED(s) && WEXITSTATUS(s) == 0}], WNOHANG, NULL) = 26982
  26582 write(1, "Child 26982 terminated\n", 23) = 23
  26582 wait4(-1, 0x7fffffc3f5f0, WNOHANG, NULL) = -1 ECHILD (No child processes)
  26582 write(1, "socket.error: [Errno 4] Interrup"..., 48) = 48
  26582 accept(3, {sa_family=AF_INET, sin_port=htons(49360), sin_addr=inet_addr("127.0.0.1")}, [16]) = 4

其中主要观察几个状态：

1. accept 建立连接，clone 创建子进程。
2. 子进程发出 SIGCHLD 信号，父进程进行捕获和处理。
3. 父进程原来阻塞在 accept 操作，当收到 SIGCHLD 信号后，触发信号处理操作，当信号处理完成之后，
   触发 socket.error 异常，随后重启 accept 继续进入阻塞状态。
   （TODO：具体为什么会在 accept 中触发 socket.error 异常还不清楚）


QA
``

1. 为什么子进程 exit 之后不直接回收资源，而需要发送 SIGCHLD 通知父进程进行回收？
2. signal handler 和 slow system call 是如何相互影响的？也就是为什么有了 signal 之后需要对 socket.error 进行捕获？


Reference:
``````````
