from multiprocessing import Pool, Manager
import time
import os
import sys
from scrapy.cmdline import execute



def put_task(q, script_name):
    q.put(["scrapy", "runspider", "scrapy_request/spiders/{}".format(script_name)])


def get_task(q):
    time.sleep(10)
    comlines = execute(q.get())


def main():
    q = Manager().Queue()
    num = int(sys.argv[1])
    script_name = sys.argv[2]
    my_pool = Pool(num)

    my_pool.apply_async(put_task, (q, script_name))
    for i in range(num-1):
        # 异步循环获取任务
        my_pool.apply_async(get_task, (q,))

    my_pool.close()
    my_pool.join()
    print("任务执行完成")


if __name__ == '__main__':
    main()
