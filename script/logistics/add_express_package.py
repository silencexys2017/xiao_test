# -*- coding:utf-8 -*-
import pymongo
from pymongo.collection import ReturnDocument
from datetime import datetime


# uri = "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@10.20.107.255/admin?"\
#       "replicaSet=rs0"
uri = "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@10.20.107.255/admin?"\
      "replicaSet=rs0"
mongo_client = pymongo.MongoClient(uri)

# logistics_db = mongo_client['devLogistics']
# order_db = mongo_client["devOrder"]
# seller_db = mongo_client["devSeller"]
# goods_db = mongo_client["devGoods"]
# ids_db = mongo_client["devIds"]
logistics_db = mongo_client['prdLogistics']
order_db = mongo_client["prdOrder"]
seller_db = mongo_client["prdSeller"]
goods_db = mongo_client["prdGoods"]
ids_db = mongo_client["prdIds"]


def add_express_package_in_pending_receipt_state(
        so_id, delivery_id=None, delivery_code=None, ship_operator_id=0):
    so_di = order_db.SaleOrder.find_one(
        {"id": so_id, "status": {"$in": [3, 4, 5, -2]}})
    if not so_di:
        raise Exception("该订单不符合要求.")
    wh_di = goods_db.Warehouse.find_one({"_id": so_di["warehouseId"]})
    if wh_di["regionId"] != 2:
        raise Exception("不是从国内发货的商品.")

    pg_di = order_db.ShipPackage.find_one({"saleOrderId": so_id})
    store_di = seller_db.Store.find_one({"_id": so_di["storeId"]})
    if (so_di.get("withBattery") != 0 or so_di.get("isMagnetic")
            or so_di.get("isPowder") or so_di.get("isCompressor")):
        tran_ware_id = store_di["speTransWareId"]
    else:
        tran_ware_id = store_di["comTransWareId"]
    if not delivery_id:
        delivery_id = pg_di.get("deliveryId")
    if not delivery_code:
        delivery_code = pg_di.get("deliveryCode")

    query = {'_id': "ExpressPackage"}
    update = {'$inc': {'seq': 1}}
    res = ids_db.ids.find_one_and_update(
        query, update, upsert=True, return_document=ReturnDocument.AFTER)
    data = {
        "id": res["seq"],
        "packageId": pg_di["id"],
        "regionId": so_di["region"],
        "status": 2,
        "addressId": pg_di["addressId"],
        "accountId": so_di["accountId"],
        "saleOrderId": so_id,
        "saleOrderCode": so_di["code"],
        "storeId": so_di["storeId"],
        "itemCount": pg_di["itemCount"],
        "soCreatedAt": so_di["createdAt"],
        "confirmedAt": so_di["confirmAt"],
        "createdAt": datetime.utcnow(),
        "deliveryCode": delivery_code,
        "deliveryId": delivery_id,
        "shipOperatorId": ship_operator_id,
        "shippedAt": so_di["shippedAt"],
        "tranWareId": tran_ware_id
    }

    logistics_db.ExpressPackage.insert_one(data)


if __name__ == "__main__":
    add_express_package_in_pending_receipt_state(304890)
    print("----------success------------")