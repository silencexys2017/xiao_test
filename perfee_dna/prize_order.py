import thriftpy2
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
import time
from datetime import datetime, timedelta
from weichigong import zconfig
import thrift_connector.connection_pool as connection_pool

_DEFAULT_CONFIG_FILE = '../config.json'
DEF_CONSTANTS = thriftpy2.load("./trpc/constants.thrift")
DEF_ORDER_SERVICE = thriftpy2.load("./trpc/order.thrift")
DEF_ORDER_STRUCT = DEF_ORDER_SERVICE.order_constants
DEF_GOODS_SERVICE = thriftpy2.load("./trpc/goods.thrift")
DEF_GOODS_STRUCT = DEF_GOODS_SERVICE.goods_struct
DEF_MEMBER_SERVICE = thriftpy2.load("./trpc/member.thrift")
DEF_MEMBER_STRUCT = DEF_MEMBER_SERVICE.member_struct
DEF_PROMOTION_SERVICE = thriftpy2.load("./trpc/promotion.thrift")
DEF_PROMOTION_STRUCT = DEF_PROMOTION_SERVICE.promotion_struct
DEF_MESSAGE_SERVICE = thriftpy2.load("./trpc/message.thrift")


order_client = connection_pool.ClientPool(
    DEF_ORDER_SERVICE.OrderService, "172.16.1.207", 8000,
    connection_class=connection_pool.ThriftPyCyClient
)
goods_client = connection_pool.ClientPool(
    DEF_GOODS_SERVICE.GoodsService, "172.16.0.177", 8000,
    connection_class=connection_pool.ThriftPyCyClient
)
promotion_client = connection_pool.ClientPool(
    DEF_PROMOTION_SERVICE.PromotionService, "172.16.1.195", 8000,
    connection_class=connection_pool.ThriftPyCyClient
)
member_client = connection_pool.ClientPool(
    DEF_MEMBER_SERVICE.MemberService, "172.16.0.190", 8000,
    connection_class=connection_pool.ThriftPyCyClient
)
message_client = connection_pool.ClientPool(
    DEF_MESSAGE_SERVICE.MessageService, "172.16.0.208", 8000,
    connection_class=connection_pool.ThriftPyCyClient
)


def getAppConfig():
    zkHosts = os.environ.get('_ZK_HOSTS')
    appName = os.environ.get('_APP_NAME')
    appEnv = os.environ.get('_APP_ENV')

    return zconfig(zkHosts, appName, appEnv)


def load_config(filename, env):
    with open(filename, 'r') as f:
        config = json.loads(f.read())

    return config[env]


def get_db(config, env, database):
    uri = config['mongodb']['uri']
    client = pymongo.MongoClient(uri)
    db = '%s%s' % (env, database)
    return client[db]


def init_logging(filename):
    directory = os.path.dirname(filename)
    if directory != '' and not os.path.exists(directory):
        os.makedirs(directory)

    level = logging.INFO
    if os.environ.get('_DEBUG') == '1':
        level = logging.DEBUG
    fmt = '[%(asctime)s %(levelname)s | %(module)s %(funcName)s] %(message)s'
    logging.basicConfig(
        filename=filename, level=logging.DEBUG, format=fmt,
        datefmt="%Y-%M-%d %H:%M:%S")
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(logging.Formatter(fmt=fmt, datefmt="%H:%M:%S"))
    logging.getLogger().addHandler(console)


def fix_prize_order():
    language = "bn"
    ACTIVITY_TYPE_LUCKY_DRAW = 2
    PAY_METHOD_COD = 2
    PLATFORM_ANDROID = "Android-App"
    ORDER_STATUS_SO_CREATE = 1
    for it in promotion_db.LuckyDrawLog.find(
        {"createdAt": {"$gt": datetime(2021, 10, 1)},
         "awardStatus": DEF_PROMOTION_STRUCT.AwardStatus.Unsend,
         "sendType": DEF_PROMOTION_STRUCT.AwardSendType.Order}):
        account_id = it["accountId"]
        region_id = it["regionId"]
        draw_log_id = it["_id"]
        address = member_client.get_draw_address(
            account_id, region_id)
        city_id = address.cityId
        address_id = address.id
        sku_id = int(promotion_db.LuckyDrawAward.find_one(
            {"_id": it["awardId"]}).get("award"))
        inv = goods_client.getSkuInventory(
            sku_id, region_id, cityId=city_id)
        sku = goods_client.get_sku_normal_model(
            sku_id, region_id, language)

        order_items = [DEF_ORDER_SERVICE.OrderItem(
            skuId=sku.sku.id, storeId=sku.sku.storeId,
            salePrice=0,
            dealPrice=0,
            priceRevision=sku.sku.priceRevision,
            count=1,
            discount=0,
            listingId=sku.listing.id,
            warehouseId=inv.warehouse.id,
            warehouseRegionId=inv.warehouse.region_id or 1,
            activityId=draw_log_id,
            activityType=ACTIVITY_TYPE_LUCKY_DRAW,
            isUseCoin=False,
            withBattery=sku.sku.withBattery,
            isMagnetic=sku.sku.withMagneto,
            isPowder=sku.sku.isPowder,
            isCompressor=sku.sku.isCompressed,
            isUsePromotion=False,
            isPlatformPostage=True,
            liquid=sku.sku.liquid
        )]
        print("-------activityId------=%r" % draw_log_id)
        # print("order_items=%r" % order_items)
        # print("account_id=%r" % account_id)
        # print("region_id=%r" % region_id)
        # print("address=%r" % address)
        # print("inv=%r" % inv)
        # print("sku=%r" % sku)

        pre_order_id = order_client.create_pre_order(
            account_id, region_id, order_items)
        batch = order_client.place_order(
            account_id, region_id, address_id, PAY_METHOD_COD,
            [DEF_ORDER_SERVICE.PostageInfo(
                0, 0, 0, True, False, sku.sku.storeId, inv.warehouse.id)],
            order_items, 0, 0, pre_order_id, timeSelected=0,
            platform=PLATFORM_ANDROID)
        if batch.batchId:
            for notice in batch.saleOrderNotices:
                message_client.change_order_notification(
                    account_id, notice.saleOrderId,
                    ORDER_STATUS_SO_CREATE, notice.code)
        promotion_client.update_lucky_draw_send_content(
            draw_log_id, str(batch.saleOrderNotices[0].saleOrderId))
        time.sleep(1)
        print("-------activityId=%s--success----=" % draw_log_id)

    """
    {
        "_id" : 737863,
        "regionId" : 1,
        "accountId" : 315939,
        "chanceType" : 1,
        "batchId" : 260,
        "awardId" : 2076,
        "awardStatus" : 2,
        "sendType" : 1,
        "sendContent" : "369543",
        "coinsCost" : 0,
        "awardLevel" : 3,
        "createdAt" : ISODate("2021-10-23T06:52:52.110Z"),
        "updatedAt" : ISODate("2021-10-23T06:52:52.110Z")
}
{
        "_id" : 2076,
        "batchId" : 260,
        "level" : 3,
        "type" : 1,
        "award" : "80001694283",
        "displayName" : "Prize 4",
        "total" : 20,
        "awardIndex" : 3,
        "drewNumber" : 1,
        "createdAt" : ISODate("2021-10-23T00:18:57.829Z"),
        "updatedAt" : ISODate("2021-10-23T00:18:57.829Z")
}
    """


if __name__ == '__main__':
    usage = 'python3 Sxx.py prd|dev|test'

    init_logging("prize_order.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    promotion_db = get_db(config, env, "Promotion")
    # FILE_NAME = "xed-order.xlsx"
    fix_prize_order()
