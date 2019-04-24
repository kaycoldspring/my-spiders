import MySQLdb


class MyMysqlClient(object):

    def __init__(self):

        self.conn = MySQLdb.connect(
            host='172.16.50.174',port=3306,
            user='spider',password='spider',
            charset='utf8',db='spider_data')

    def save_db(self):
        pass