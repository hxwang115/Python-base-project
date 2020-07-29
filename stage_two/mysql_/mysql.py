"""
将字典存入数据库中
"""
import pymysql
import re
# 打开文件
f = open('dict.txt')

# 连接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='unique',
                     database='dict',
                     charset='utf8')
# 获取游标
cur = db.cursor()
# 执行SQL语句


sql = 'insert into words(word,mean) value(%s,%s)'
for line in f:
    tup = re.findall(r'(\S+)\s+(.*)',line)
    print(tup)
    try:
        cur.execute(sql,tup)
        db.commit()
    except:
        db.rollback()
# 结束工作
f.close()
cur.close()
db.close()





