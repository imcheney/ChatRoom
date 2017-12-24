# -*- coding: utf-8 -*-
"""
select module's usage example

1. select通知你哪个fd有事件
select 在某个 socket 有数据到达时，或者当某个 socket 可以写数据时，又或者是当某个 socket 发生错误时通知.
select让你可以同时响应很多socket的多个事件.

2. Linux C VS Python
Linux 下 C 语言的 select 使用到位图来表示我们要关注哪些文件描述符的事件;
Python 中使用 list 来表示我们监控的文件描述符，当有事件到达时，返回的也是文件描述符的 list，表示这些文件有事件到达.

3. 例子
下面的简单程序是表示select等待从标准输入中获得输入, 注意, select如果不设置timeout的话, 是阻塞的!
因此, 在这里, 这个程序是等待在select这个语句的, 直到键盘输入了一些东西, 才会往下执行print语句.

rlist, wlist, elist = select.select( [sys.stdin], [], [] )
print sys.stdin.read()

上面的例子，由于参数只有一个事件 sys.stdin，表示只关心标准输入事件.
因此当select返回时, rlist只会是[sys.stdin], 返回结果表示可以从stdin中读入数据.
于是, 我们使用sys.stdin.read方法来读入数据.
"""

import socket
import select

sock1 = socket.socket()
sock2 = socket.socket()

sock1.connect(('127.0.0.1', 5000))
sock2.connect(('127.0.0.1', 5000))

while True:  # we want to read many messages all the time, so just keep looping...
    rlist, wlist, elist = select.select([sock1, sock2], [], [], 5)  # Await a read event for up to 5 sec
    if [rlist, wlist, elist] == [[], [], []]:  # case for timeout
        print "Five seconds elapsed.\n"
    else:
        for sock in rlist:  # Loop through each socket in rlist, read and print the available data
            print sock.recv(100)
