#!bin/bash

time2=$(date "+%Y%m%d%H%M")
filestart='/data/logs/catallina.out.'
filename=$filestart$time2

if [ -f $filename ];then
	scp $filename root@198.11.180.134:/data/work
else
	ehco dir $filename not exits
fi