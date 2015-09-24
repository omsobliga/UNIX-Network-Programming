# poll vs epoll

## epoll 的设计初衷：

因为 **每次 select/poll 调用都必须告诉 kernel 所有之前监听过的描述符和新建的描述符。**
所以当连接数很多，而活跃连接很少，就会需要产生较大开销。

**为了减少 kernel 和 application 不必要数据的传递。**
epoll 通过使用 edge-triggered 可实现只提供状态发生变化的描述符。
同时为了与 select/poll 的调用方式保持一致，epoll 也提供了 level-triggered 版本。

> The epoll event mechanism [18, 10, 12] is designed
> to scale to larger numbers of connections
> than select and poll. One of the
> problems with select and poll is that in
> a single call they must both inform the kernel
> of all of the events of interest and obtain new
> events. This can result in large overheads, particularly
> in environments with large numbers
> of connections and relatively few new events
> occurring.

> Further reductions in the number of generated
> events can be obtained by using edge-triggered
> epoll semantics. In this mode events are only
> provided when there is a change in the state of
> the socket descriptor of interest. For compatibility
> with the semantics offered by select
> and poll, epoll also provides level-triggered
> event mechanisms.

> Event mechanisms like select
> and poll have traditionally combined these
> tasks into a single system call. However, this
> amalgamation requires the server to re-declare
> its interest set every time it wishes to retrieve
> events, since the kernel does not remember the
> interest sets from previous calls. This results in
> unnecessary data copying between the application
> and the kernel.

> Come from: [4]

## poll 和 epoll 主要区别？

### 在实现方式上的区别：

#### poll:

* `int poll(struct pollfd *fds, nfds_t nfds, int timeout);`

每次调用时候需要把所有 fds 都传递给 kernel，然后 application 发生阻塞，
直到 kernel 有准备好的 fd 返回。

#### epoll:

* `int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);`
* `int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);`

epoll 的事件注册和监听是分开的，分别通过 `epoll_ctl` 和 `epoll_wait` 实现。
所以在 `epoll_wait` 进行监听时候不需要把所有要监听的描述符都传递过去。
如果有新的描述符需要监听或者监听的描述符状态发生改变，只需要通知这一个描述符的状态到 kernel 就行。

### 时间复杂度上的差异？

select/poll 在返回后，需要遍历所有监听的文件描述符来判断是否就绪。
所以select/poll 的时间复杂度与监听的文件描述符相关，而不是活跃描述符。
当监听的描述符很多而活跃的描述符很少时，select/poll 的效率就很低。

epoll 通过回调机制进行通知，**所以只需要轮询返回的准备好的描述符**。
所以 epoll 的时间复杂度取决于活跃描述符，而不是监听的描述符。

### 总结：

所以 epoll 主要解决的问题就是：**kernel 和 application 不必要数据的传递**。

* 从 application 到 kernel，epoll 在描述符状态发生改变后，只需要传递该描述符给 kernel 即可。
  poll 需要在每次调用时将所有套接字传递过去。
* 从 kernel 到 application，epoll 只返回已准备好的套接字，poll 似乎返回所有套接字和它们的状态。

## select/poll/epoll 在不同环境中的性能表现？

select/poll/epoll 在 idle connection（空闲连接）比较少的时候差异不大。
当 idle connections 较大时候，select/poll 的性能下降较明显，epoll 的性能不受影响。
详细分析参考：[4]

## TODO:

* 测试 select/poll/epoll 在 idle connections 较多时的表现。

## Reference:

- [1] [《UNIX 网络编程》](http://book.douban.com/subject/1500149/)
- [2] [epoll 或者 kqueue 的原理是什么？](http://www.zhihu.com/question/20122137/answer/14049112)  # 网络模型入门介绍
- [3] [epoll(7) - Linux man page](http://linux.die.net/man/7/epoll)
- [4] [Comparing and Evaluating epoll, select, and poll Event Mechanisms](https://www.kernel.org/doc/ols/2004/ols2004v1-pages-215-226.pdf)  # 推荐：五星
- [5] [Linux IO 模式及 select、poll、epoll详解](http://segmentfault.com/a/1190000003063859)  # 推荐：四星
