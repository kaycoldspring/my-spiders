from scrapy.cmdline import execute
import os,sys
from time import sleep
from multiprocessing import Pool


sys.path.append(os.path.dirname(__file__))

def run_spider(number):
    print('spider %s is started ... ...' % number)
    # 执行启动爬虫的命令
    execute('scrapy runspider SXRSpider.py'.split(' '))  # 此处需要变更为你的爬虫名字

if __name__ == "__main__":
    p = Pool(20)    # 开启的进程数
    for i in range(20):
        # 创建进程
        p.apply_async(run_spider, args=(i,))
        sleep(2)
        p.close()
        p.join()