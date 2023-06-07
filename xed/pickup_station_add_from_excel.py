import logging
import sys
import os
import pymongo
from openpyxl import load_workbook

K_DB_URL = {
    "dev": "mongodb://root:KB5NF1T0aP@mongodb-headless.os:27017/admin?replicaSet=rs0",
	"test": "mongodb://root:IdrCgVpHzv@mongo-mongodb-headless.os:27017/admin?replicaSet=rs0&retrywrites=false",
    "prd": ""
}


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


def get_db(uri, env, database):
    client = pymongo.MongoClient(uri[env])
    db = '%s%s' % (env, database)
    return client[db]


def strip_string_name(name):
    if not name:
        return
    if not isinstance(name, str):
        name = str(name)
    name = name.strip()
    return name


def add_pickup_station(file_route):
    wb_obj = load_workbook(file_route, data_only=True)
    ks_sheet = wb_obj.get_sheet_by_name("Sheet1")
    start_id = None
    for it in bee_common_db.PickupStation.find().sort([("_id", -1)]).limit(1):
        start_id = it["_id"] + 1
    for row in list(ks_sheet.iter_rows(min_row=2, max_row=1551)):
        station_id = int(strip_string_name(row[0].value))
        station = bee_common_db.PickupStation.find_one(
            {"sourceStationId": station_id})
        if station:
            continue
        data = {
            "_id": start_id,
            "sourceStationId": station_id,
            "status": 1,
            "name": "Makadaraka HoneyComb KiliShop",
            "address": "MAKADARA TOWN, Hamza, Gean Apartment GO3, Along Luka Cres Road",
            "isSupportBigPackage": "1",
            "areaId": 315,
            "areaCode": "100140",
            "businessType": 3,
            "pickingCode": "1-105",
            "businessTime": "Mon-Sat 9:000am-6:00pm",
            "latitude": 36.873906,
            "longitude": -1.29692,
            "regionCode": "KE",
            "county": "Nairobi",
            "town": "Makadara",
            "phone": null,
            "leafAreaIds": [
                1000032006
            ]
        }
        start_id += 1
        county, sub_county, area = strip_string_name(
            row[0].value), strip_string_name(row[1].value), strip_string_name(
            row[2].value)
        shop_id = strip_string_name(row[4].value)


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging("release_ready.log")

    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env, source = sys.argv[1], sys.argv[2]
    bee_common_db = get_db(K_DB_URL, env, "BeeCommon")