import pymysql, os, logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger('INA')
logger.setLevel(logging.DEBUG)

# 建立一个FileHandler来把日志记录在文件里，级别为debug以上
# fh = logging.FileHandler("/data/logs/ina_click.log")
fh = RotatingFileHandler("/data/logs/send.log", maxBytes=1024*1024*100, backupCount=1)
fh.setLevel(logging.DEBUG)
# 建立一个StreamHandler来把日志打在CMD窗口上，级别为error以上
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# 将相应的handler添加在logger对象中
logger.addHandler(ch)
logger.addHandler(fh)



class MyMysql():

    def __init__(self):

        self.conn = pymysql.connect("rm-rj9359u6ma681ncgto.mysql.rds.aliyuncs.com", "ddjuser", "3dIrM#sA@MA$x4aKGB",
                             "ddj")
        self.cursor = self.conn.cursor()


    def get_server(self):
        sql = "select a.* from machine a, (select a.country, a.tag , min(a.id) as minid from machine a," \
              "(select country, tag, min(cnt) as minCnt from machine group by country, tag) b " \
              "where a.Country = b.country and a.tag = b.tag and a.cnt = b.minCnt group by a.Country, a.Tag) b " \
              "where a.id = b.minid"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data


    def update_cnt(self, num, server):

        updateSql  ="update machine set cnt = %s where Machine = %s"
        self.cursor.execute(updateSql,[num, server])
        self.conn.commit()


    def conn_close(self):
        self.cursor.close()
        self.conn.close()

db = MyMysql()
def task():
    taskList = db.get_server()  # 获取任务列表
    fileList = os.listdir('/data/device') # 遍历设备文件夹
    if len(fileList) > 0:
        for task in taskList:
            server = task[2]  # 获取ip, 接收文件次数
            num = task[4]
            file = fileList[-1]
            # 利用sshpass 执行scp命令  参数为 ip,源文件  这里写绝对路径
            logger.info('start send %s to %s'%(file, server))
            result = os.system("sshpass -p '3dIrM#sA@MA$x4aKGB' scp /data/device/%s root@%s:/data/work1"%(file, server))
            result1 = os.system("sshpass -p '3dIrM#sA@MA$x4aKGB' scp /data/device/1.log root@%s:/data/work2"%(server))
            if result == 0 and result1 == 0:         # 返回值为0,则执行成功
                logger.info('send task success')
                num += 1            # 将对应服务器的接收文件次数+1
                db.update_cnt(num, server)  # 更新数据库
            else:
                logger.error('send fail')
        db.conn_close()

    else:
        logger.info('No files in this folder')



if __name__ == '__main__':
    task()