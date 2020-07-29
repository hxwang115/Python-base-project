"""
selcet  tcp
"""
from socket import *
from select import select
# 全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)
# 创建监听套接字
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)# 立即释放端口
s.bind(ADDR)
s.listen(5)
# 设置关注列表
rlist = [s]# 用于等待处理连接
wlist = []
xlist = []

# 监控IO
while True:
    rs,ws,xs = select(rlist,wlist,xlist)
    # 遍历返回值列表，处理就绪的IO
    for r in rs:
        if r is s:
            c,addr = s.accept()
            print('Connect from',addr)
            rlist.append(c)
        else:
            data = r.recv(1024)
            if not data:
                rlist.remove(r)
                r.clse()
                continue
            print(data)
            r.send(b'ok')
        



