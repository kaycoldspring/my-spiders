#!/bin/bash

for file in `ls /data/work1`
do
        if [ -f "/data/work2/1.log" ];then
        cat "/data/work1/"$file | grep 'Android' | grep '"IND"' >> /data/work/$file
        fi
done

rm -rf /data/work1/*
rm -rf /data/work2/*