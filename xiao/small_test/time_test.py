import time
from datetime import datetime, timedelta, timezone
import pytz


ACCESS_KEY_ID = "BQAK1A35FNZRCLOIGPOV"
SECRET_ACCESS_KEY = "pLIjnidp8PmHFKePxDPrGRTS5JaNYxeNWRbuGy4J"
SERVER_URL = "https://obs.cn-south-4.myhuaweicloud.com"


def utc2local(utc_st):
    """UTC时间转本地时间（+8:00）"""
    now_stamp = time.time()
    local_time = datetime.fromtimestamp(now_stamp)
    utc_time = datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    print(local_st)
    return local_st


def local2utc(local_st):
    """本地时间转UTC时间（-8:00）"""
    time_struct = time.mktime(local_st.timetuple())
    print(time_struct)
    utc_st = datetime.utcfromtimestamp(time_struct)
    return utc_st


def local_obj_time_to_utc(time_obj, time_zone='Asia/Dhaka'):
    # pytz.country_timezones('bd')
    # t_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    # l_format = "%Y-%m-%d %H:%M:%S"
    local_tz = pytz.timezone(time_zone)
    local_dt = local_tz.localize(time_obj, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt


def time_zone_convert():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
    print(type(utc_dt))
    cn_dt = utc_dt.astimezone(timezone(timedelta(hours=-8)))
    print(cn_dt)
    jan_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
    print(jan_dt)
    cn_2_jan_dt = cn_dt.astimezone(timezone(timedelta(hours=9)))
    print(cn_2_jan_dt)


def return_test():
    return 1, 2


def _local_time_to_utc(time_str):
    t_format = TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    local_tz = pytz.timezone("Etc/GMT-1")
    local_dt = local_tz.localize(
        datetime.strptime(time_str, t_format), is_dst=None)
    return local_dt.astimezone(pytz.utc)


if __name__ == "__main__":
    utc_time = datetime(2014, 9, 18, 10, 42, 16, 126000)
    # utc转本地
    # local_time = utc2local(utc_time)
    # print(local_time)
    # output：2014-09-18 18:42:16

    # 本地转utc
    # utc_tran = local2utc(utc_time)
    # res = _local_time_to_utc("2021-05-05 21:27:34")
    # print(utc_tran)
    # output：2014-09-18 10:42:16
    # res = local_obj_time_to_utc(datetime(2020, 2, 1))
    # res = return_test()

    # print(res)
    time_zone_convert()
