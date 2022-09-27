# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime, timedelta
from operator import itemgetter, attrgetter


_DEFAULT_CONFIG_FILE = '../config.json'
REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}
MONTH = ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"]
map_pay_method = {
    1: 'Online',
    2: 'COD',
    3: 'Pre'
}
map_client = {
    1: 'App',
    2: 'iOS',
    3: 'PC',
    4: 'WAP'
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

map_so_type = {
    1: 'Normal',
    2: 'Flash',
    3: 'Lucky Draw',
    4: 'Redeem',
    5: 'Mixed',
    6: 'Group Buying'
}

map_delivery_method = {
    1: '平台承运',
    2: '店铺自发货',
    3: "平台送，店铺设运费"
}

map_package_state = {
    1: 'Pending Dispatch',
    2: 'In Transit',
    3: 'In Delivery',
    4: 'Completed',
    5: 'In Delivery',
    -1: 'Rejected',
    -2: 'Cancel'
}


UTC_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
LOCAL_FORMAT = '%Y-%m-%d %H:%M:%S'
TIME_FORMAT = '%Y%m%d'


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


def utc2local(utc_datetime):
    if not utc_datetime:
        return utc_datetime
    # utc_dt = datetime.strptime(utcstr, UTC_FORMAT)
    # local: 东6区
    lo_dt = utc_datetime + timedelta(hours=6)
    return lo_dt.strftime(TIME_FORMAT)


def _get_currency(region):
    return {1: "BDT", 3: "MMK"}.get(region)


def _get_logistics(log_id):
    return {1: "eCourier", 2: "eDesh", 3: "exfcs"}.get(log_id)


def export_settle_accounts_orders(start_time, end_time):
    so_li = []
    so_ids = []
    address_ids = set()
    for it in order_db.SaleOrder.find(
            {"createdAt": {"$gte": start_time, "$lt": end_time},
             "status": 5}).sort([("_id", -1)]):
        so_ids.append(it["id"])
        address_ids.add(it["addressId"])
        so_li.append({"id": it["id"], "time": it["createdAt"]})

    add_di = {it["id"]: it for
              it in member_db.address.find({"id": {"$in": list(address_ids)}})}
    sod_dict = {}
    sku_ids = set()
    for it in order_db.SaleOrderDetail.find({"orderId": {"$in": so_ids}}):
        if sod_dict.get(it["orderId"]):
            sod_dict[it["orderId"]].append(it)
        else:
            sod_dict[it["orderId"]] = [it]
        sku_ids.add(it["skuId"])

    sku_dict = {it["_id"]: it["title"] for it in goods_db.SpecOfSku.find(
        {"_id": {"$in": list(sku_ids)}})}

    spg_dict = {it["saleOrderId"]: it for it in order_db.ShipPackage.find(
        {"saleOrderId": {"$in": so_ids}})}

    workbook = xlsxwriter.Workbook(FILE_NAME)
    worksheet = workbook.add_worksheet("saleOrders")
    headings = [
        "商户订单号", "收款人证件类型", "收款人证件号码", "收款人名称", "收款人账号",
        "交易时间", "交易币种", "交易金额", "商品名称", "商品数量", "商品单价",
        "快递公司编码", "运单号", "收货人姓名", "收货人联系方式", "收货人地址", "发货日期"
    ]
    style_headings = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column('A:Q', 15, other_bold)
    worksheet.write_row('A1', headings, style_headings)
    row = 1
    for it in so_li:
        row += 1
        so_id = it["id"]
        spg = spg_dict[so_id]
        sod_li = sod_dict[so_id]
        worksheet.write('A%d' % row, so_id)
        worksheet.write('B%d' % row, '02')
        worksheet.write('C%d' % row, 'MA63BG0G5')
        worksheet.write('D%d' % row, '成都巢南信息技术有限公司')
        worksheet.write('E%d' % row, '51050142629300001594')
        worksheet.write('F%d' % row, utc2local(it["time"]))
        worksheet.write('G%d' % row, _get_currency(spg["region"]))
        # worksheet.write('G%d' % row, "CNH")
        worksheet.write('H%d' % row, spg["amount"])

        title = ""
        count = ""
        price = ""
        for index, item in enumerate(sod_li):
            count = count + str(item["count"]) + ";"
            # if index > 0:
            #     continue
            title = title + sku_dict[item["skuId"]] + ";"
            price = price + str(item["dealPrice"]) + ";"

        worksheet.write('I%d' % row, title[:-1])
        worksheet.write('J%d' % row, count[:-1])
        worksheet.write('K%d' % row, price[:-1])

        worksheet.write('L%d' % row, _get_logistics(spg["terminalDeliveryId"]))
        worksheet.write('M%d' % row, spg["terminalDeliveryCode"])
        address = add_di[spg["addressId"]]
        worksheet.write('N%d' % row, address["name"])
        worksheet.write('O%d' % row, address["phone"])
        worksheet.write(
            'P%d' % row, (address["state"] + " " + address["city"] + " " +
                          address["area"] + " " + address["address1"]).replace(
                '\n', '').replace('\r', ''))
        if not spg.get("shippedAt"):
            shipped_at = spg.get("dispatchedAt")
        else:
            shipped_at = spg.get("shippedAt")
        worksheet.write('Q%d' % row, utc2local(shipped_at))
    workbook.close()


def utc2_local_time(utc_datetime):
    if not utc_datetime:
        return utc_datetime
    # utc_dt = datetime.strptime(utcstr, UTC_FORMAT)
    # local: 东6区
    lo_dt = utc_datetime + timedelta(hours=6)
    return lo_dt.strftime("%Y%m%d %H:%M:%S")


def get_order_time():
    order_ids = [373846,373855,373857,373863,373904,374048,374141,374142,374169,374201,374365,374404,374496,374601,374898,374902,374909,374913,374914,374929,374941,374970,374983,374988,374997,374998,375006,375018,375023,375025,375031,375032,375033,375036,375045,375046,375047,375048,375061,375062,375071,375078,375090,375116,375124,375153,375198,375199,375210,375219,375221,375231,375238,375253,375258,375261,375262,375317,375368,375370,375377,375398,375401,375409,375415,375441,375442,375478,375491,375505,375537,375551,375570,375600,375601,375607,375616,375625,375637,375646,375652,375653,375677,375699,375701,375704,375707,375711,375741,375745,375746,375747,375752,375760,375771,375772,375773,375775,375784,375788,375793,375794,375801,375807,375819,375820,375829,375842,375847,375848,375850,375859,375868,375886,375892,375893,375894,375898,375907,375909,375921,375922,375923,375924,375925,375933,375938,375945,375947,375950,375951,375961,375962,375970,375987,375993,376000,376001,376013,376029,376030,376032,376039,376042,376043,376044,376045,376049,376050,376058,376059,376062,376069,376070,376078,376091,376095,376102,376104,376116,376120,376130,376137,376141,376146,376150,376162,376163,376173,376184,376185,376188,376194,376200,376204,376208,376212,376214,376235,376240,376242,376243,376254,376255,376271,376276,376277,376297,376299,376308,376316,376336,376353,376355,376356,376358,376372,376377,376379,376394,376395,376402,376403,376404,376407,376408,376412,376422,376444,376455,376456,376460,376461,376472,376477,376481,376490,376495,376497,376498,376499,376500,376506,376507,376519,376524,376528,376535,376539,376543,376544,376545,376555,376560,376562,376567,376568,376574,376579,376582,376590,376599,376605,376623,376625,376632,376641,376645,376646,376647,376649,376655,376660,376663,376666,376669,376670,376674,376678,376680,376681,376682,376683,376689,376698,376705,376719,376724,376727,376742,376747,376748,376749,376752,376754,376756,376764,376766,376767,376772,376777,376780,376781,376782,376789,376790,376799,376800,376804,376806,376819,376822,376831,376832,376838,376839,376841,376857,376862,376866,376867,376874,376875,376886,376887,376889,376899,376902,376904,376916,376922,376932,376934,376936,376937,376942,376943,376944,376952,376961,376964,376976,376978,376986,376992,376995,376996,376998,377000,377006,377011,377016,377018,377019,377033,377039,377040,377042,377046,377049,377051,377059,377063,377067,377068,377074,377078,377079,377093,377094,377097,377101,377102,377103,377104,377105,377110,377126,377127,377128,377129,377130,377142,377146,377147,377151,377164,377165,377171,377179,377185,377189,377190,377191,377197,377198,377201,377206,377207,377208,377211,377212,377213,377217,377220,377222,377223,377228,377230,377232,377234,377240,377241,377242,377246,377248,377250,377254,377262,377269,377276,377279,377280,377282,377284,377286,377289,377290,377305,377310,377318,377324,377335,377336,377340,377341,377342,377344,377350,377353,377367,377369,377370,377375,377377,377380,377382,377383,377399,377401,377405,377412,377413,377414,377415,377416,377419,377435,377441,377445,377448,377449,377450,377452,377455,377456,377457,377458,377471,377472,377474,377475,377476,377477,377485,377486,377489,377492,377495,377496,377497,377506,377513,377518,377519,377522,377525,377529,377535,377537,377538,377541,377542,377552,377556,377559,377565,377570,377572,377575,377576,377586,377591,377592,377601,377602,377615,377618,377620,377621,377634,377648,377653,377655,377657,377658,377662,377668,377690,377695,377700,377701,377702,377707,377711,377712,377714,377717,377720,377723,377736,377740,377755,377756,377785,377791,377793,377799,377801,377815,377820,377822,377823,377835,377840,377920,377922,377923,377925,377950,377963,377969,377996,377997,377999,378000,378002,378005,378022,378038,378059,378065,378073,378078,378087,378102,378108,378111,378116,378117,378118,378119,378123,378130,378131,378132,378135,378141,378149,378150,378151,378152,378159,378160,378172,378173,378174,378175,378178,378189,378191,378193,378200,378209,378210,378220,378222,378234,378246,378270,378277,378280,378295,378301,378302,378303,378306,378309,378316,378330,378331,378332,378338,378352,378353,378354,378360,378371,378372,378374,378375,378376]
    for it in order_db.SaleOrder.find(
            {"id": {"$in": order_ids}}).sort([("id", 1)]):
        print(utc2_local_time(it["createdAt"]),
              utc2_local_time(it["shippedAt"]))


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    _DEFAULT_LOG_FILE = 'orders_202106.log'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    goods_db = get_db(config, env, "Goods")
    seller_db = get_db(config, env, "Seller")
    member_db = get_db(config, env, "Member")
    FILE_NAME = "orders-202202.xlsx"
    export_settle_accounts_orders(
        datetime(2022, 2, 1), datetime(2022, 3, 1))
    # get_order_time()

