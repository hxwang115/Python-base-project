"""
TCP 并发
思路：
1、将客户端处理设置为协程函数
2、让SOCKET模块下的阻塞可以触发协程跳转
"""
import gevent
from gevent import monkey

monkey.patch_all()  # 执行脚本，修改阻塞

from socket import *


def handle(c,addr):
    while True:
        data = c.recv(1024).decode()
        if not data:
            break
        print(addr[1],data)
        c.send(b'ok')


s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 8888))
s.listen(5)
# 循环接收客户端连接
while True:
    c, addr = s.accept()
    print("Connect from", addr)
    # handle(c)
    gevent.spawn(handle, *(c,addr))
