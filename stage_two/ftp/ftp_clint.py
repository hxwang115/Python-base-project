"""
ftp 文件服务器，客户端
多进程/线程并发 socket
TCP套接字
"""
from socket import *
import sys
import time

ADDR = ("127.0.0.1", 8888)


class FTPClient:
    """
    客户端 查看，上传,下载，退出
    """

    def __init__(self, sockfd):
        """

        :param sockfd:套接字
        """
        self.sockfd = sockfd

    # 获取文件库列表
    def do_list(self):
        self.sockfd.send(b'L')  # 发送请求
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'ok':
            # 一次性接收文件名字符串
            data = self.sockfd.recv(4046)
            print(data.decode())
        else:
            print(data)

    # 退出
    def do_exit(self):
        self.sockfd.send(b'e')  # 发送请求
        self.sockfd.close()
        sys.exit('THANK YOU')

    # 下载文件
    def do_get_ftp(self, filename):
        self.sockfd.send(('D ' + filename).encode())  # 发送请求
        # 等待回应
        data = self.sockfd.recv(1024).decode()
        if data == 'ok':
            f = open(filename, 'wb')
            # 循环写入文件
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()

    # 上传文件
    def do_up_ftp(self, filename):
        try:
            f = open(filename, 'rb')
        except Exception as e:
            print('文件不存在')
            return
        # 发送请求
        self.sockfd.send(('UP ' + filename.split('/')[-1]).encode())
        # 等待反馈
        data = self.sockfd.recv(1024).decode()
        if data == 'ok':
            # 发送文件
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)


# 连接服务端
def main():
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print(e)
        return

    # 实例化对象
    ftp = FTPClient(sockfd)
    # 循环发送请求
    while True:
        print("请输入命令")
        print("list")
        print("get ftp")
        print("up ftp")
        print("exit")
        con = input("输入命令")
        if con.strip() == 'list':
            ftp.do_list()
        elif con.strip() == 'exit':
            ftp.do_exit()
        elif con.strip()[:3] == 'get':
            ftp.do_get_ftp(con.strip().split()[-1])
        elif con.strip()[:2] == 'up':
            ftp.do_up_ftp(con.strip().split()[-1])

        else:
            print('请输入正确命令')


if __name__ == '__main__':
    main()
