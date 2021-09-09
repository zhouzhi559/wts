import pymysql
#
# host = "10.0.0.235"
# user = 'root'
# password = 'root'
# port = 3306

host = "10.0.0.103"
user = 'imds'
password = 'imotionflow'
port = 3306


# ---------------数据库、表单创建------------------#
# 创建数据库
class DB:
    def create_database(self, dBName):
        conn = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               port=port)
        cursor = conn.cursor()
        try:
            cursor.execute('create database  %s' % dBName)
            print('新数据库【%s】创建-成功！' % dBName)
            cursor.close()
            conn.close()
        except Exception:
            print('新数据库【%s】创建-失败！' % dBName)

    # ------------------数据库操作---------------------#
    # 连接数据库
    def get_connection(self, dbName):
        conn = pymysql.connect(host=host, user=user, password=password, port=port, db=dbName, )
        return conn
    def get_connection_nodb(self):
        conn = pymysql.connect(host=host, user=user, password=password, port=port )
        return conn

    def get_connection_mysql(self):
        conn = pymysql.connect(host=host, user=user, password=password, port=port)

        return conn

    # 执行SQL
    def execute_sql(self, conn, sql):
        sql = sql.lstrip()  # 去sql语句左边空格
        typeName = sql[0]  # 取sql第1个字母判断执行指令：select\insert\update\delete
        cursor = conn.cursor()
        cursor.execute(sql)
        if typeName == 'i' or typeName == 'I':
            conn.commit()
            return typeName
        elif typeName == 'd' or typeName == 'D':
            conn.commit()
            return typeName
        elif typeName == 'u' or typeName == 'U':
            conn.commit()
            return typeName
        elif typeName == 's' or typeName == 'S':
            rows = cursor.fetchall()
            return rows

    def test_sql(self, conn, sql, params):
        sql = sql.lstrip()  # 去sql语句左边空格
        typeName = sql[0]  # 取sql第1个字母判断执行指令：select\insert\update\delete
        cursor = conn.cursor()
        cursor.execute(sql, params)
        if typeName == 'i' or typeName == 'I':
            conn.commit()
            return typeName
        elif typeName == 'd' or typeName == 'D':
            conn.commit()
            return typeName
        elif typeName == 'u' or typeName == 'U':
            conn.commit()
            return typeName
        elif typeName == 's' or typeName == 'S':
            rows = cursor.fetchall()
            return rows



    # 断开数据库
    def close_connection(self, conn):
        conn.close()
