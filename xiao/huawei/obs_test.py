import time
from datetime import datetime, timedelta, timezone
import pytz
import requests
from obs import HeadPermission, ObsClient, PutObjectHeader
import traceback


ACCESS_KEY_ID = "BQAK1A35FNZRCLOIGPOV"
SECRET_ACCESS_KEY = "pLIjnidp8PmHFKePxDPrGRTS5JaNYxeNWRbuGy4J"
SERVER_URL = "https://obs.cn-south-4.myhuaweicloud.com"


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
        # resp = obs_client.putFile(bucket_name, object_name, file_path=file_path)
        resp = obs_client.putContent(
            bucket_name, object_name, content=file_path)
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
    # obs_test()
    object_name = '{}tmp/{}/{}'.format("dev/", "wms-public-temp-dev", "24.jpg")
    res = requests.get("https://kilimall-testing.s3.ap-northeast-1.amazonaws.com/lite-dev/public/store-info/logo-200000008.png")
    context = res.content
    print(str(context))
    print(isinstance(res.content, bytes))
    raise Exception
    print(len(res.content))
    obs_client = ObsClient(
        access_key_id=ACCESS_KEY_ID,
        secret_access_key=SECRET_ACCESS_KEY,
        server=SERVER_URL)

    headers = PutObjectHeader()
    # 设置对象访问权限为公共读
    headers.acl = HeadPermission.PUBLIC_READ
    headers.contentType = "image/png"
    resp = obs_client.putContent(
        "k-fms-temp-cn", "dev/tmp/xiao-test/logo-2.png", content=res.content,
        headers=headers)
    print(resp)
    # upload_file_to_obs(bucket_name="k-fms-temp-cn",
    #                    object_name='{}/{}/{}'.format("dev", "xiao-test", "24.jpg"),
    #                    file_path="24.jpg")
    print(res)

    # print(res)
    # time_zone_convert()
