# -*- coding:utf-8 -*-
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from multiprocessing import Process
from logging import Logger
import os


COROUTINE_NUMBER = 1000  # 协程池数量
pool = Pool(COROUTINE_NUMBER)  # 使用协程池

class Task():

    def __init__(self, dirpath):
        self.logger = Logger(self.__class__.__name__)
        self.dirpath = dirpath

    def read_file(self, fname):
        """
        使用协程池读取文件
        :param fname: 文件
        :return:
        """
        with open(fname, encoding='utf-8') as f:
            self.logger.info('start read')
            pool.map(self.work, f)

    def work(self, line):
        '''
        处理文件每一行内容的逻辑
        :param line: 文件每一行
        :return:
        '''
        '''dosomething'''

    def main(self):
        """
        使用多进程执行程序
        :return:r
        """
        p_list = []
        files = os.listdir(self.dirpath)
        '''进程会因为文件的数量而创建,当文件足够多时,是不适用的,之所以不用进程池,
        是因为multiprocessing.Pool和gevent有冲突,所以可以采用while 1 的方式,每次都读取文件夹下
        的第一个文件,处理完成后根据需要是否删除或移动'''
        if len(files) > 0:
            for f in files:
                need_file = self.dirpath + f
                self.logger.info('current file:%s'%need_file)
                p = Process(target=self.read_file, args=(need_file,))
                p.start()
                p_list.append(p)
                for p in p_list:
                    p.join()
                # shutil.move(self.dirpath + files[0], r'/data/detected/' + files[0])  移动到别处,但是需要提前创建目标文件夹
                os.remove(self.dirpath + files[0])  # 删除文件
        else:
            print('No executable file in the destination folder')
         

if __name__ == "__main__":
    Task('').main()



