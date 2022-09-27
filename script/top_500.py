# -*- coding:utf-8 -*-
import pymongo
import json
from datetime import datetime


# uri = "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@10.20.107.255/admin?"\
#       "replicaSet=rs0"
uri = "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@10.20.107.255/admin?"\
      "replicaSet=rs0"
mongo_client = pymongo.MongoClient(uri)


# seller_db = mongo_client["devSeller"]
# goods_db = mongo_client["devGoods"]
# order_db = mongo_client["devOrder"]
# statistics_db = mongo_client["devStatistics"]
seller_db = mongo_client["prdSeller"]
goods_db = mongo_client["prdGoods"]
order_db = mongo_client["prdOrder"]
statistics_db = mongo_client["prdStatistics"]


def get_top_500_sold_listing():
    field = "$orderCount"
    start_time = datetime(2020, 5, 1)
    match = {"$match": {"createdAt": {"$gte": start_time}}}
    group = {"$group": {"_id": "$listingId", "count": {"$sum": field}}}
    match_1 = {"$match": {"count": {"$gt": 0}}}
    sort = {"$sort": {"count": -1}}
    limit = {"$limit": 500}

    return [{"listingId": it["_id"], "count": it["count"]}
            for it in statistics_db.ProductCount.aggregate(
            [match, group, match_1, sort, limit])]


def get_top_500_views_listing():
    field = "$views"
    start_time = datetime(2020, 5, 1)
    match = {"$match": {"createdAt": {"$gte": start_time}}}
    group = {"$group": {"_id": "$listingId", "count": {"$sum": field}}}
    match_1 = {"$match": {"count": {"$gt": 0}}}
    sort = {"$sort": {"count": -1}}
    limit = {"$limit": 500}

    return [{"listingId": it["_id"], "count": it["count"]}
            for it in statistics_db.ProductCount.aggregate(
            [match, group, match_1, sort, limit])]


if __name__ == "__main__":
    res_1 = get_top_500_sold_listing()
    print(json.dumps(res_1))
    print("------------------------------------------------------------------")
    res_2 = get_top_500_views_listing()
    print(json.dumps(res_2))
