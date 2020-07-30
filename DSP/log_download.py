# -*- coding: utf-8 -*-
import os


def download_log_tar():

    result = os.system("wget --user=jerry --password=Jerry@2020_16 -P /data/logs https://dsp.cmcm.com/download-logs/2020_0115_0600_bid_data.tar.gz")
    if result == 0:
        os.system("tar -zxvf /data/logs/2020_0115_0600_bid_data.tar.gz -C /data/logs")
        log_csv = '/data/logs/data/druid_share/dsp_output/*'

