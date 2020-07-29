"""
登录用户界面
"""
import pymysql
# 连接数据库
db = pymysql.connect(user='root',
                     host='localhost',
                     port=3306,
                     password='unique',
                     database='stu',
                     charset='utf8')
cur = db.cursor()
def register():
    name = input('user:')
    password = input('password:')
    sql = 'select * from user where name=%s'
    cur.execute(sql,[name])
    result = cur.fetchone() # 进行查找看结果
    # 如果不为空,说明用户名重复
    if result:
        return False
    if not result:
        try:
            sql_1 = 'insert into user(name,password) values(%s,%s)'
            cur.execute(sql_1,(name,password))
            db.commit()
            return True
        except:
            db.rollback()
            return False
def login_in():
    name = input('user:')
    password = input('password')
    sql = 'select password from user where name=%s'
    cur.execute(sql,[name])
    if password == cur.fetchone()[0]:
        return True


while True:
    print("""==============
             1.登录   2.注册
             ==============
    """)
    cmd = int(input('输入命令:'))
    if cmd == 1:
        if  login_in():# 登录
            print('登录成功')
            break
        else:
            print('登录失败')
    if cmd == 2:
        if register():# 注册
            print('注册成功')
        if not register():
            print('用户已存在')
