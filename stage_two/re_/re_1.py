"""
正则表达式练习
通过输入端口来获得地址
"""
import re
f = open('exc.txt')


def get_address(port):
    while True:
        data = ''
        for line in f:
            if line is '\n':
                break
            data += line
        if not data:
            break
        obj = re.match(port,data)
        if obj:
            pattern = r'[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}'
            obj = re.search(pattern,data)
            return obj.group()
    return 'no have this port'


if __name__ == '__main__':
    port = input('端口')
    f = get_address(port)
    print(f)




