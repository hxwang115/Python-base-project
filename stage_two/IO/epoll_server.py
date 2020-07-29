"""
IO 多路复用的epoll方法
"""
from socket import *
from select import *

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 8888))
s.listen(5)
# 创建对象
p = epoll()
# 建立查找字典，通过fileno找到IO对象
fdmap = {s.fileno(): s}
# 关注事件
p.register(s, EPOLLIN | EPOLLET)
# 循环监控IO发生
while True:
    events = p.poll()  # 返回的是 IO的fileno和事件组成的元组
    # 循环遍历列表，查看那个IO就绪
    for fd, event in events:
        if fd == s.fileno():
            c, addr = fdmap[fd].accept()
            print('connect from:', addr)
            p.register(c, EPOLLIN | EPOLLET)
            fdmap[c.fileno()] = c  # 维护字典
        elif event & EPOLLIN:  # 判断是否是epoolin就绪
            data = fdmap[fd].recv(1024)
            if not data:
                p.unregister(fd)
                fdmap[fd].close()
                del fdmap[fd]  # 从字典中删除
                continue
            print(data.decode())
            fdmap[fd].send(b'ok')
