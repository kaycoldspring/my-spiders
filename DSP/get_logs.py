import os,time


logname='catalina.out.'+time.strftime('%Y%m%d%H%M')[:-1]+'0'
os.system("sshpass -p '3dIrM#sA@MA$x4aKGB' scp root@47.89.253.225:/data/logs/%s /data/device"%logname)