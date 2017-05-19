import pymysql
import logging

conn = pymysql.connect(host='127.0.0.1', user='root',
                       password='vtzf2123+', db='mysql', charset='utf8')
cursor = conn.cursor()
cursor.execute('use test')
test = "insert into client values (%s,%s,%s)"
try:
    cursor.execute('select * from student where sname=%s', '王丽')
    result = cursor.fetchall()
    print(result)
except Exception as e:
    logging.exception(e)
finally:
    cursor.close()
    conn.close()
