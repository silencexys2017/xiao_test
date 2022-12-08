import time
from datetime import datetime, timedelta, timezone
import pytz
from obs import ObsClient
import traceback


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


def put_file(resource_name, file_name, content=None, is_temp=False):
    suffix = file_name.split('.')[-1]
    headers.contentType = CONTENT_TYPE[suffix]

    if is_temp is True:
        obj_key = '{}tmp/{}/{}'.format(
            current_app.config.get("resource/prefix"), resource_name, file_name)
    else:
        obj_key = '{}{}/{}'.format(
            current_app.config.get("resource/prefix"), resource_name, file_name)

    resp = obs_client.putContent(
        current_app.config["24.jpg"],
        obj_key, content=content, headers=headers)
    obs_client.close()
    if resp.status >= 300:
        abort(constants.HTTP_CODE_400,
              code=DEF_EXCEPTIONS.ERROR_UPLOAD_RESOURCE_INVALID,
              msg=resp.reason)
    else:
        # return resp.body.objectUrl
        return resp


def obs_test():
    obs_client = ObsClient(
        access_key_id=ACCESS_KEY_ID,
        secret_access_key=SECRET_ACCESS_KEY,
        server=SERVER_URL)
    try:
        resp = obs_client.getObjectMetadata(
            "perfee-user-upload-test", 'sagawa-label/200002470360-3.pdf')
        print(resp)

        if resp.status < 300:
            print('requestId:', resp.requestId)
            print('etag:', resp.body.etag)
            print('lastModified:', resp.body.lastModified)
            print('contentType:', resp.body.contentType)
            print('contentLength:', resp.body.contentLength)
        else:
            print('status:', resp.status)
    except:
        print(traceback.format_exc())


def upload_file_to_obs(bucket_name, object_name, file_path=None):
    obs_client = ObsClient(
        access_key_id=ACCESS_KEY_ID,
        secret_access_key=SECRET_ACCESS_KEY,
        server=SERVER_URL)
    try:
        resp = obs_client.putFile(bucket_name, object_name, file_path=file_path)
        print(resp)
        if resp.status < 300:
            print('requestId:', resp.requestId)
            print('etag:', resp.body.etag)
            print('lastModified:', resp.body.lastModified)
            print('contentType:', resp.body.contentType)
            print('contentLength:', resp.body.contentLength)
        else:
            print('status:', resp.status)
    except:
        print(traceback.format_exc())
    obs_client.close()


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
    # obs_test()
    object_name = '{}tmp/{}/{}'.format("dev/", "wms-public-temp-dev", "24.jpg")
    upload_file_to_obs(bucket_name="k-fms-temp-cn",
                       object_name='{}/{}/{}'.format("dev", "xiao-test", "24"),
                       file_path="24.jpg")
    print(res)

    # print(res)
    # time_zone_convert()
