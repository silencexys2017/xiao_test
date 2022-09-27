import pymongo
import json
import os
import sys
import signal
import logging
from datetime import datetime, timezone
from random import randint

local_goods_image_base_url = "https://gimg-dev.perfee.com/goods/"
vendor_goods_image_base_url = "https://vimg-dev.perfee.com/image/"
m_site_goods_base_url = "https://m-dev.perfee.com/listing/"
_DEFAULT_FILE = 'perfee_orderinfo_log_%s24_%s'
_DEFAULT_CONFIG_FILE = '../config.json'

DEFAULT_COUNTRY_CODE = "ww"
SPEC_SIZE_ID = 5
SPEC_COLOR_ID = 14
map_pay_method = {
    1: 'Online',
    2: 'COD',
    3: 'Pre'
}
map_so_state = {
    1: 'Pending Payment',
    2: 'Pending Confirmation',
    3: 'Pending Dispatch',
    4: 'In Transit',
    5: 'All received',
    6: 'Restocking',
    -1: 'Cancel',
    -2: 'Rejected',
    -3: 'Partially Received'
}
"""
"0" => "未付款"; "1" => "已付款"; "2" => "备货"; "3" => "完全发货"; "4" => "已收到货"; "5" => "拒收",
"6" => "付款中"; "7" => "已授权"; "8" => "部分付款"; "10" => "退款"; "11" => "取消"; "13" =>"付款失败"
"15" => "部分配货"; "16" => "完全配货"; "20" => "部分发货";
"""


def _exit(signum, frame):
    log_file.close()
    json_file.close()
    print("cursor close")
    exit()


def format_image_url(file_name):
    if '{{{perfee.img}}}' in file_name:
        url = "%s%s" % (
            local_goods_image_base_url,
            file_name.replace('{{{perfee.img}}}', ''))
    elif '{{{vendor.obs}}}' in file_name:
        url = "%s%s" % (
            vendor_goods_image_base_url,
            file_name.replace('{{{vendor.obs}}}', ''))
    else:
        url = file_name
    return url


def formar_lisitng_url(listing_id):
    return "%s%s" % (m_site_goods_base_url, listing_id)


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


def load_config(filename, env):
    with open(filename, 'r') as f:
        config = json.loads(f.read())

    return config[env]


def get_db(config, env, database):
    uri = config['mongodb']['uri']
    client = pymongo.MongoClient(uri)
    db = '%s%s' % (env, database)
    return client[db]


def get_related_data():
    region_code_di = {it["id"]: it["code"] for it in common_db.region.find()}
    so_cursor = order_db.SaleOrder.find(
        {"id": {"$gt": 314782}}).sort([("id", 1)])
    total_count = so_cursor.count()
    pro_count = 0
    try:
        for so in so_cursor:
            pro_count += 1
            order_status = "0"
            change_time = so["createdAt"]
            if so["status"] == 1:
                order_status = "0"
            elif so["status"] == 2:
                if so["payMethod"] == 1:
                    order_status = "1"
                    change_time = so["paidAt"]
                else:
                    order_status = "2"
            elif so["status"] == 3:
                order_status = "2"
                change_time = so["confirmAt"]
            elif so["status"] == 4:
                order_status = "3"
                change_time = so["shippedAt"]
            elif so["status"] == 5:
                order_status = "4"
                change_time = so["closedAt"]
            elif so["status"] == 6:
                order_status = "2"
            elif so["status"] in [-1]:
                change_time = so["closedAt"]
                order_status = "11"
            elif so["status"] == -2:
                change_time = so["closedAt"]
                order_status = "5"

            sku_id = ""
            sku_title = ""
            sku_count = ""
            sku_price = ""
            for sod in order_db.SaleOrderDetail.find(
                    {"orderId": so["id"]}).sort([("id", 1)]):
                sku = goods_db.SpecOfSku.find_one({"_id": sod["skuId"]})
                if not sku:
                    log_file.write("%s\n" % sod["id"])
                    print("----sku=%s-----not found" % "skuId")
                    continue
                sku_id = sku_id + str(sod["skuId"]) + ","
                sku_title = sku_title + sku["title"] + ","
                sku_count = sku_count + str(sod["count"]) + ","
                sku_price = sku_price + str(sod["salePrice"]) + ","
            hw_obj = {
                "userid": "%s" % so["accountId"],
                "order_name": so["code"],
                "order_time": str(int(so["createdAt"].replace(
                    tzinfo=timezone.utc).timestamp()*1000)),
                "sku_id": sku_id[:-1],
                "sku_name": sku_title[:-1],
                "sku_number": sku_count[:-1],
                "sku_price": sku_price[:-1],
                "shop_id": str(so["storeId"]),
                "order_status": order_status,
                "status_change_time": str(int(change_time.replace(
                    tzinfo=timezone.utc).timestamp()*1000)),
                "order_price": str(so["payAmount"]),
                "order_id": "%s" % so["id"],
                "region_code": region_code_di[so["region"]]
            }

            data = json.dumps(hw_obj)
            json_file.write(data + "\n")
            pre_g = str(int(round((pro_count-1)/total_count, 2)*100))
            percent_g = str(int(round(pro_count/total_count, 2)*100))
            if percent_g != pre_g:
                sys.stdout.write("->" + "%" + percent_g)
                sys.stdout.flush()
        so_cursor.close()
        log_file.close()
        json_file.close()
        print("cursor close")
    except Exception as err:
        so_cursor.close()
        log_file.close()
        json_file.close()
        print("cursor close")
        raise err


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    file_name = _DEFAULT_FILE % (
        datetime.utcnow().strftime('%Y%m%d%H'), randint(0, 9))
    log_file = open("%s.log" % file_name, "w")
    json_file = open("%s.json" % file_name, "w")

    init_logging("%s.log" % file_name)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    seller_db = get_db(config, env, "Seller")
    order_db = get_db(config, env, "Order")
    goods_db = get_db(config, env, "Goods")
    common_db = get_db(config, env, "Common")
    signal.signal(signal.SIGINT, _exit)
    signal.signal(signal.SIGTERM, _exit)
    get_related_data()
