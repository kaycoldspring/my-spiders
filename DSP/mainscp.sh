#!/bin/bash
host_list=./server_list.conf
cat ${host_list} | while read line
do
  host_ip=`echo ${line}|awk '{print $1}'`
  username=`echo ${line}|awk '{print $2}'`
  password=`echo ${line}|awk '{print $3}'`
  src_file=`echo ${line}|awk '{print $4}'`
  dest_file=`echo ${line}|awk '{print $5}'`
  ./allscp.sh ${src_file} ${username} ${host_ip} ${dest_file} ${password}
done
