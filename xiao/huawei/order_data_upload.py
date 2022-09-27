#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from datetime import datetime, tzinfo, timezone
import json

UPLOAD_URL = "http://119.8.10.165:6447/recommend/datacollection/import/" \
             "orderinfo"
# UPLOAD_URL = "http://119.8.10.165:6447/recommend/datacollection/import/iteminfo"
id_token = "testToken"
app_id = "perfee"


def request_post_api(url, args):
    headers = {
        'Content-Type': 'application/json',
        "Accept": "application/json",
        # "Charset": "UTF-8",
        'Authorization': id_token,
        'X-Kit-AppID': app_id
    }

    res = requests.post(url, headers=headers, data=json.dumps(args))
    print(res.headers)
    print(res)
    print(res.text)

    # if res.get("result_code") != "200":
    #     msg = "upload order data failed"
    #     print("upload order data failed, requestid=%s,result_code=%s" % (
    #         res.get("requestid"), res.get("result_code")))
    #     raise Exception(msg)

    return res


def upload_order_data(
        data_opt_type, account_id, region_code, so_id, so_code, created_at,
        sku_id, sku_title, sku_count, sale_price, store_id, order_status,
        pay_amount):
    data = {
        "appid": app_id,
        "timestamp": str(int(datetime.utcnow().replace(
            tzinfo=timezone.utc).timestamp()*1000)),
        "industry_type": "1",
        "data_opt_type": data_opt_type,
        "orderdata": [
            {
                "userid": "%s" % account_id,
                "order_name": so_code,
                "order_time": str(int(created_at.replace(
                    tzinfo=timezone.utc).timestamp()*1000)),
                "sku_id": "%s" % sku_id,
                "sku_name": sku_title,
                "sku_number": str(sku_count),
                "sku_price": str(sale_price),
                "shop_id": str(store_id),
                "order_status": order_status,
                "status_change_time": str(int(created_at.replace(
                    tzinfo=timezone.utc).timestamp()*1000)),
                "order_price": str(pay_amount),
                "order_id": "%s" % so_id,
                "region_code": region_code
            }
        ]
    }

    print(data)
    return request_post_api(UPLOAD_URL, data)


if __name__ == "__main__":
    res = upload_order_data(
        data_opt_type="2", account_id=100, region_code="BD", so_id=13,
        so_code="D002", created_at=datetime(2018, 12, 1), sku_id=7000,
        sku_title="test", sku_count=1, sale_price=100, store_id=1,
        order_status="1", pay_amount=100)

    print(res)
