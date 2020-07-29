"""
网页 HTTP
"""
import gevent
from gevent import monkey

monkey.patch_all()
from socket import *


# 具体功能实现
class HTTPServer:
    def __init__(self, host='0.0.0.0', port=8888, dir=None):
        self.host = host
        self.port = port
        self.dir = dir
        self.address = (host, port)
        # 实例化对象时直接创建套接字
        self.create_socket()
        self.bind()

    def create_socket(self):
        """
        创建套接字
        :return:
        """
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self):
        """
        绑定地址
        :return:
        """
        self.sockfd.bind(self.address)

    def server_forever(self):
        self.sockfd.listen(3)
        print('Listen the port %d' % self.port)
        # 循环接收客户端消息
        while True:
            c, addr = self.sockfd.accept()
            print('Connect from', addr)
            gevent.spawn(self.handle, c)

    def handle(self, c):
        while True:
            data = c.recv(1024)
            if not data:
                break
            # 提取请求内容
            data_line = data.splitlines()[0]
            info = data_line.decode().split(' ')[1]
            print(c.getpeername(), info)
            if info == '/' or info[-5:] == '.html':
                self.get_html(c, info)

    def get_html(self, c, info):
        if info == '/':
            # 请求主页
            filename = self.dir + '/index.html'
        else:
            filename = self.dir + info
        try:
            fd = open(filename)
        except Exception:
            # 网页不存在,（响应体）
            response = 'HTTP/1.1 404 Not Found\r\n'
            response += 'Content-Type:text/html\r\n'
            response += '\r\n'
            response += '<h1>Sorry...</h1>'
        else:

            # 网页存在
            response = 'HTTP/1.1 200 ok\r\n'
            response += 'Content-Type:text/html\r\n'
            response += '\r\n'
            response += fd.read()
        finally:
            c.send(response.encode())


if __name__ == '__main__':
    """
    用户需要展示自己的网页
    """
    HOST = '0.0.0.0'
    PORT = 8888
    DIR = './static'
    httpd = HTTPServer(HOST, PORT, DIR)
    httpd.server_forever()  # 启动服务
