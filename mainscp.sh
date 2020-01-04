#!/bin/bash
host_list="/soft_shell/server_list.conf"
cat $host_list | while read line
do
  host_ip=`echo $line|awk '{print $1}'`
  username=`echo $line|awk '{print $2}'`
  password=`echo $line|awk '{print $3}'`
  src_file=`echo $line|awk '{print $4}'`
  dest_file=`echo $line|awk '{print $5}'`
  ##key=`echo $line|awk '{print $6}'`
  ##./allscp.sh $key $src_file $username $host_ip $dest_file $password
  ./allscp.sh $src_file $username $host_ip $dest_file $password
done