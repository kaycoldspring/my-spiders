# -*- coding: utf-8 -*-
# @Time    : 2020/1/11 13:54
# @Author  : Kay Luo
# @FileName: gen_config.py
# @Software: PyCharm

import os, datetime


# file = 'catalina.out.202001110000'
# print(os.path.splitext(file))

# t = time.strftime('%Y%m%d%H')
# print(t)

now = datetime.datetime.now()
print(now)
later = (now + datetime.timedelta(hours=-1)).strftime('%Y%m%d%H')
print(later)
files = os.popen('ls /data/logs/')
log_time = (datetime.datetime.now() + datetime.timedelta(hours=-1)).strftime('%Y%m%d%H')
for file in files:
    if log_time in os.path.splitext(file)[1]:
        src_file = '/data/logs/' + 'catalina.out.' + log_time + '*'  # 生成要发送的源文件

        with open('/soft_shell/demo.conf', 'r') as f:
            content = f.read()
            new_content = content.replace('${src_file}', src_file)

        with open('/soft_shell/server_list.conf', 'w') as f:
            f.write(new_content)


    else:
        continue




