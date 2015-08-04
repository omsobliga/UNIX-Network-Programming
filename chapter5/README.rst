Make Test
=========

python multi-process-server.py | python client.py
-------------------------------------------------

netstat -a | grep 5007
``````````````````````

::

  Proto Recv-Q Send-Q  Local Address          Foreign Address        (state)
  tcp4       0      0  localhost.50007        localhost.55553        ESTABLISHED
  tcp4       0      0  localhost.55553        localhost.50007        ESTABLISHED
  tcp4       0      0  *.50007                *.*                    LISTEN
  ...

LISTEN 表示 server 主进程处于监听状态。
第一个 ESTABLISHED 表示 server 子进程正在进行请求处理。
第二个 ESTABLISHED 表示 client 已经与 server 建立连接，并进行数据通信。


ps -t ttys001 -o pid,ppid,tty,stat,args,wchan
`````````````````````````````````````````````

::

  PID  PPID TTY      STAT ARGS                           WCHAN
  22098 18210 ttys001  S+   python multi-process-server.py -
  22113 22098 ttys001  Z+   (python)                       -
  22119 22098 ttys001  Z+   (python)                       -
  22227 22098 ttys001  Z+   (python)                       -

第一个表示主进程的状态，后面三个 STAT 为 `Z+` 表示僵死的子进程。
