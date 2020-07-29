"""
ftp 文件服务器，服务端
多进程/线程并发 socket
TCP套接字
"""
from socket import *
from threading import Thread
import sys, os
import time

# 全局变量
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)
FTP = "/home/hxwang/ftp/"


class FTPServer(Thread):
    """
    查看列表，下载，上传，退出处理
    """

    def __init__(self, connfd):
        """

        :param connfd: 连接套接字
        """
        self.connfd = connfd
        super().__init__()

    # 获取文件库中文件列表
    def do_list(self):
        files = os.listdir(FTP)
        print(files)
        if not files:
            self.connfd.send("文件库为空".encode())
            return
        else:
            self.connfd.send(b'ok')
            time.sleep(0.1)
            # 拼接文件名
        filelist = ''
        for file in files:
            # 判断文件是否为隐藏文件，是否为普通文件
            filelist += file + '\n'
        self.connfd.send(filelist.encode())

    # 将文件发往客户端
    def do_get(self, filename):
        try:
            f = open(FTP + filename, 'rb')
        except Exception:
            self.connfd.send('文件不存在'.encode())
            return
        else:
            self.connfd.send(b'ok')
            time.sleep(0.1)
            # 发送文件
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.connfd.send(b'##')
                    break
                self.connfd.send(data)

    # 接收客户端发来的文件
    def do_up(self, filname):
        if os.path.exists(FTP + filname):
            self.connfd.send(b'FILE ALREADY EXISTS')
            return
        self.connfd.send(b'ok')
        # 接收文件并写入
        f = open(filname, 'wb')
        while True:
            data = self.connfd.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()

    # 循环接收请求，分情况调用功能函数
    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if not data or data == 'e':
                return
            elif data.strip().split()[0] == 'D':
                self.do_get(data.strip().split()[-1])
            elif data.split()[0] == 'UP':
                self.do_up(data.strip().split()[-1])
            elif data == 'L':
                self.do_list()


# 搭建网络服务端模型
def main():
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 立即释放端口
    s.bind(ADDR)
    s.listen(5)
    print("listen the port 8888....")
    # 循环等待客户端连接
    while True:
        try:
            c, addr = s.accept()  # 等待客户端客户端连接请求
            print("Connect from", addr)
        except KeyboardInterrupt:
            sys.exit("退出服务器")
        except Exception as e:
            print(e)
            continue

        # 创建线程
        # 处理请求
        clint = FTPServer(c)
        clint.setDaemon(True)  # 主线程结束时讲其一并收回
        clint.start()  # 运行run


if __name__ == '__main__':
    main()
