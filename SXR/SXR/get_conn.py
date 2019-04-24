import MySQLdb

class MyMysqlClient(object):

    def __init__(self):
        '''
        获取MySQL连接
        '''
        self.conn = MySQLdb.connect(
            host='127.0.0.1',port=3306,
            user='root',password='123456',charset='utf8',db='test'
        )

    def save_word(self,word):
        '''
        存入数据库
        :return:
        '''
        sql='insert into kword(word) values (%s)'
        self.conn.cursor().execute(sql,[word])
        self.conn.commit()

    def get_word(self):
        '''
        获取关键字
        :return:
        '''
        sql='select word from kword'
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result