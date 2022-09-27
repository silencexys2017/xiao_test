#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymongo
from datetime import datetime, timedelta
from threading import Thread

uri = "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@10.20.107.255/admin?" \
      "replicaSet=rs0"
# uri = "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@10.20.107.255/admin?"\
#       "replicaSet=rs0"

client = pymongo.MongoClient(uri, 27017)

o_db = client.devOrder
g_db = client.devGoods
s_db = client.devStatistics
# g_db = client.prdGoods
# o_db = client.prdOrder
# s_db = client.prdStatistics
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
START_TIME = datetime.strptime("2018-11-20T00:00:00.000Z", TIME_FORMAT)

nt_time = datetime.utcnow()
day_time = datetime(nt_time.year, nt_time.month, nt_time.day, 0, 0, 0)


def statistics_products(start_time, INTERVAL):
    for item in range(INTERVAL):
        start = start_time + timedelta(days=item)
        end = start_time + timedelta(days=(item + 1))
        cond = {"createdAt": {"$gte": start, "$lt": end},
                "listingId": {"$exists": False}}
        sku_ids = set()
        so_ids = set()
        for it in o_db.SaleOrderDetail.find(cond):
            sku_ids.add(it["skuId"])
            so_ids.add(it["orderId"])

        sku_di = {}
        for it in g_db.SpecOfSku.find({"_id": {"$in": list(sku_ids)}}):
            sku_di[it["_id"]] = {"listingId": it["listingId"],
                                 "storeId": it["storeId"],
                                 "orderCount": 0, "views": 0, "rejected": 0,
                                 "actualSold": 0}
        so_di = {it["id"]: it for it in o_db.SaleOrder.find(
            {"id": {"$in": list(so_ids)}})}
        for it in o_db.SaleOrderDetail.find(cond):
            so_it = so_di[it["orderId"]]
            o_db.SaleOrderDetail.update_one(
                {"_id": it["_id"]},
                {"$set": {"listingId": sku_di[it["skuId"]]["listingId"]}})
            s_db.OrderSku.find_one_and_update(
                {"saleOrderDetailId": it["id"]},
                {"$set": {
                    "storeId": so_it["storeId"],
                    "regionId": 1,
                    "accountId": so_it["accountId"],
                    "listingId": sku_di[it["skuId"]]["listingId"],
                    "skuId": it["skuId"],
                    "activityType": it.get("activityType", 0),
                    "activityId": it.get("activityId", 0),
                    "saleOrderId": it["orderId"],
                    "count": it["count"],
                    "salePrice": it["salePrice"],
                    "dealPrice": it["dealPrice"],
                    "discount": it.get("discount", 0),
                    "coin": it.get("coin", 0),
                    "coinRedeem": it.get("redeem", 0),
                    "voucherRedeem": it.get("voucherRedeem", 0),
                    "warehouseId": it["warehouseId"],
                    "vat": it.get("vat", 0),
                    "status": it["status"],
                    "createdAt": it["createdAt"]}
                }, upsert=True)
            goal = sku_di[it["skuId"]]
            goal["orderCount"] += it["count"]
            if so_it["status"] == 5:
                goal["actualSold"] += it["count"]
            elif so_it["status"] == -2:
                goal["rejected"] += it["count"]

            if so_it.get("confirmAt"):
                o_db.ShipOrderDetail.update_one({"saleOrderDetailId": it["id"]},
                                                {"$set": {"listingId": sku_di[
                                                    it["skuId"]]["listingId"]}})

        for key, value in sku_di.items():
            up = {"$set": {"regionId": 1, "listingId": value["listingId"],
                           "storeId": value["storeId"]},
                  "$inc": {"orderCount": value["orderCount"],
                           "views": value["views"],
                           "rejected": value["rejected"],
                           "actualSold": value["actualSold"]}}
            s_db.ProductCount.find_one_and_update(
                {"skuId": key, "createdAt": start}, up, upsert=True)


def statistics_data():
    thread_num = 29
    t_obj = []
    for item in range(thread_num):
        if item == 0:
            INTERVAL = 82
            days = 0
        elif item == 1:
            INTERVAL = 38
            days = 82
        elif item == 2:
            INTERVAL = 27
            days = 120
        elif item == 3:
            INTERVAL = 13
            days = 147
        elif item == 4:
            INTERVAL = 16
            days = 160
        elif item == 5:
            INTERVAL = 11
            days = 176
        elif item == 6:
            INTERVAL = 16
            days = 187
        elif item in [7, 8, 9]:
            INTERVAL = 10
            days = 203 + (item - 7) * 10
        elif item == 10:
            INTERVAL = 9
            days = 233
        elif item == 11:
            INTERVAL = 10
            days = 242
        elif item == 12:
            INTERVAL = 7
            days = 252
        elif item == 13:
            INTERVAL = 15
            days = 259
        elif item == 14:
            INTERVAL = 6
            days = 274
        elif item == 15:
            INTERVAL = 9
            days = 280
        elif item == 16:
            INTERVAL = 12
            days = 289
        elif item == 17:
            INTERVAL = 16
            days = 301
        elif item == 18:
            INTERVAL = 16
            days = 317
        elif item == 19:
            INTERVAL = 13
            days = 333
        elif item == 20:
            INTERVAL = 6
            days = 346
        elif item == 21:
            INTERVAL = 4
            days = 352
        elif item == 22:
            INTERVAL = 5
            days = 356
        elif item in [23, 24]:
            INTERVAL = 12
            days = 361 + (item - 23) * 12
        elif item in [25, 26, 27]:
            INTERVAL = 17
            days = 385 + (item - 25) * 17
        elif item == 28:
            INTERVAL = 25
            days = 436

        start = START_TIME + timedelta(days=days)
        t1 = Thread(target=statistics_products, args=(start, INTERVAL,))
        t_obj.append(t1)
        t1.start()

    for t1 in t_obj:
        t1.join()
    print("statistics_data complete")


if __name__ == "__main__":
    statistics_data()
