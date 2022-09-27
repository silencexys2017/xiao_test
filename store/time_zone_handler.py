#!/usr/bin/env python
# -*- coding:utf-8 -*-

import thriftpy
from datetime import datetime, timedelta
import time
import pymongo
import pytz


def get_local_time_by_utc(t_datetime, region_id=None, time_zone=None):
    if region_id:
        if region_id == 1:
            time_zone = 'Asia/Dhaka'
        elif region_id == 2:
            time_zone = 'Asia/Shanghai'
        elif region_id == 3:
            time_zone = 'Asia/Rangoon'
        elif region_id == 4:
            time_zone = 'Asia/KarachiThu'
        elif region_id == 5:
            time_zone = 'Asia/Tokyo'
        local_tz = pytz.timezone(time_zone)
        return pytz.utc.localize(t_datetime, is_dst=None).astimezone(local_tz)

    if time_zone:
        local_tz = pytz.timezone(time_zone)
        local_dt = pytz.utc.localize(t_datetime, is_dst=None)
        return local_dt.astimezone(local_tz)


def mon_go_db_test(utc_time):
    url = "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@mongo-perfee-paas/admin?" \
          "replicaSet=rs0"
    client = pymongo.MongoClient(url, 27017)
    unx_db = client.devUnx
    unx_db.xiao.insert_one({"now": utc_time})


if __name__ == "__main__":
    time_pass = datetime.now()
    start = time_pass - timedelta(
        hours=time_pass.hour, minutes=time_pass.minute,
        seconds=time_pass.second, microseconds=time_pass.microsecond)
    print(time_pass)
    res = get_local_time_by_utc(start, region_id=1)
    print(res)
    start = datetime(res.year, res.month, res.day, res.hour, res.minute,
                     res.second, res.microsecond)
    print(start)
    # mon_go_db_test(start)
    time_zone = datetime.now(pytz.timezone('Asia/Dhaka'))

