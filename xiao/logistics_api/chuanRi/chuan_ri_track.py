#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import pytz
from datetime import datetime

app_key = "43a04832c271b400ea946fd421c3be8743a04832c271b400ea946fd421c3be87"
# app_key = "b89323dd6062a0de21d94a9ccf6f8ae7b89323dd6062a0de21d94a9ccf6f8ae7"
# app_token = "067198af63d9530af3ee4c6dd3f0c5bc"
app_token = "ce8c12bfe118dd038df3f72b69ac0d4b"
header = {"Content-Type": "application/x-www-form-urlencoded"}
# track_api = "http://crgj.rtb56.com/webservice/PublicService.asmx/ServiceInterfaceUTF8"
track_api = "http://toms.ruantongbao.com/webservice/PublicService.asmx/ServiceInterfaceUTF8"


def _local_time_to_utc(time_str, courier):
    # pytz.country_timezones('bd')
    t_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    time_zone = 'Asia/Dhaka'
    if courier == "DEF_OCS.Courier.E_COURIER":
        if "T" in time_str:
            t_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        else:
            t_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    elif courier == "DEF_OCS.Courier.E_DESH":
        if "." in time_str:
            t_format = "%Y-%m-%dT%H:%M:%S.%f"
        else:
            t_format = "%Y-%m-%dT%H:%M:%S"
        time_zone = 'Asia/Kolkata'
    elif courier == "DEF_OCS.Courier.EXFCS":
        time_zone = "Asia/Rangoon"
    elif courier == "DEF_OCS.Courier.SAGAWA":
        time_zone = "Asia/Tokyo"
        t_format = "%Y%m%d%H%M"
    elif courier == 7:
        time_zone = "Asia/Tokyo"
        t_format = "%Y-%m-%d %H:%M:%S"

    local_tz = pytz.timezone(time_zone)
    local_dt = local_tz.localize(
        datetime.strptime(time_str, t_format), is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def get_track(tracking_number):
    params_json = json.dumps({"tracking_number": tracking_number})
    data = {
        "appToken": app_token,
        "appKey": app_key,
        "serviceMethod": "gettrack",
        "paramsJson": params_json
    }
    return requests.post(
        track_api, data=data, headers=header).json()
    # res = {
    #     "success": 1,
    #     "cnmessage": "获取跟踪记录成功",
    #     "enmessage": "Get Track successfully",
    #     "data": [
    #         {
    #             "server_hawbcode": "RZ000013260TW",
    #             "destination_country": "US",
    #             "track_status": "NT",
    #             "track_status_name": "转运中",
    #             "signatory_name": "",
    #             "details": [
    #                 {
    #                     "track_occur_date": "2018-09-04 11:52:27",
    #                     "track_location": "",
    #                     "track_description": "快件电子信息已经收到",
    #                 }
    #             ]
    #         }
    #     ]
    # }
    # if res.get("data"):
    #     return res["data"][0]
    # return {}


def get_api_track(tracking_number):
    params_json = json.dumps({"tracking_number": tracking_number})
    data = {
        "appToken": app_token,
        "appKey": app_key,
        "serviceMethod": "gettrack",
        "paramsJson": params_json
    }
    return requests.post(
        track_api, data=data, headers=header).json()


def _get_chuan_ri_tracks(tracks):
    track_li = []
    for it in tracks.get("details", []):
        done_time = _local_time_to_utc(
            it.get("track_occur_date"), 7)
        track_li.append((done_time, it.get("track_description")))
    print (track_li)
    return track_li


if __name__ == "__main__":
    # 352423961923
    res = get_api_track("D120210526000001")
    # res = get_track(352423961923)
    _get_chuan_ri_tracks(res.get("data")[0])
    print(res)