import pymongo
import json
import signal
from datetime import datetime
from random import randint

local_goods_image_base_url = "https://gimg-dev.perfee.com/goods/"
vendor_goods_image_base_url = "https://vimg-dev.perfee.com/image/"
m_site_goods_base_url = "https://m-dev.perfee.com/listing/"
# mongo_uri = ("mongodb://pf_prd_readonly:8K3bdg6MnK3r6a9EsaUF@mongo-perfee-paas/admin?"
#              "replicaSet=rs0&readPreference=secondaryPreferred")
mongo_uri = "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@10.20.107.255/admin?replicaSet=rs0"
goods_db_name = 'devGoods'
common_db_name = 'devCommon'
seller_db_name = 'devSeller'

DEFAULT_COUNTRY_CODE = "ww"
SPEC_SIZE_ID = 5
SPEC_COLOR_ID = 14


def _exit(signum, frame):
    skus_cursor.close()
    f.close()
    f2.close()
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


signal.signal(signal.SIGINT, _exit)
signal.signal(signal.SIGTERM, _exit)

now = datetime.now()
file_name = 'perfee_iteminfo_log_%s24_%s' % (now.strftime("%Y%m%d%H"), randint(1, 9999))
f = open('%s.json' % file_name, 'w')
f2 = open('%s.log' % file_name, 'w')


mongo_client = pymongo.MongoClient(mongo_uri)
goods_db = mongo_client[goods_db_name]
common_db = mongo_client[common_db_name]
seller_db = mongo_client[seller_db_name]
skus_cursor = goods_db.SpecOfSku.find({"type": 1}, no_cursor_timeout=True).sort([("_id", 1)])
try:
    cur_listing_id = None
    cur_region_id = None
    cur_brand_id = None
    cur_store_id = None
    cur_seller_id = None
    cur_third_category_id = None
    cur_second_category_id = None
    cur_first_category_id = None
    cur_warehouse_id = None
    cur_review_total_id = None

    listing = None
    region = None
    brand = None
    store = None
    seller = None
    third_category = None
    second_category = None
    first_category = None
    warehouse = None
    review_total = None
    listing_spec_values = None

    problem_listing_id = None

    for sku in skus_cursor:
        for region_id, status in sku["status"].items():
            print(sku["_id"], region_id)
            if sku["listingId"] != cur_listing_id:
                listing = goods_db.SpecOfListing.find_one({"_id": sku["listingId"]})
                cur_listing_id = sku["listingId"]
                _listing_spec_values = {}
                for _listing_spec in listing["specs"]:
                    _listing_spec_values[int(_listing_spec["id"])] = {}
                    for _listing_spec_value in _listing_spec["values"]:
                        _listing_spec_values[int(_listing_spec["id"])][int(_listing_spec_value["id"])] = _listing_spec_value["value"]
                listing_spec_values = _listing_spec_values
            if int(region_id) != cur_region_id:
                region = common_db.region.find_one({"id": int(region_id)})
                cur_region_id = int(region_id)
            if listing["brandId"] != cur_brand_id:
                brand = goods_db.Brand.find_one({"_id": listing["brandId"], "isDeleted": False})
                cur_brand_id = listing["brandId"]
            if listing["storeId"] != cur_store_id:
                store = seller_db.Store.find_one({"_id": listing["storeId"]})
                cur_store_id = listing["storeId"]
            if store["sellerId"] != cur_seller_id:
                seller = seller_db.Seller.find_one({"_id": store["sellerId"]})
                cur_seller_id = store["sellerId"]
            if listing["categoryId"] != cur_third_category_id:
                third_category = goods_db.Category.find_one({"_id": listing["categoryId"]})
                cur_third_category_id = listing["categoryId"]
            if (not third_category) or (third_category["depth"] != 3):
                if sku["listingId"] != problem_listing_id:
                    f2.write("%s\n" % sku["listingId"])
                    problem_listing_id = sku["listingId"]
                continue
            if third_category["parent"] != cur_second_category_id:
                second_category = goods_db.Category.find_one({"_id": third_category["parent"]})
                cur_second_category_id = third_category["parent"]
            if second_category["parent"] != cur_first_category_id:
                first_category = goods_db.Category.find_one({"_id": second_category["parent"]})
                cur_first_category_id = second_category["parent"]
            inv = goods_db.SkuInventory.find_one({"skuId": sku["_id"]})
            # 派生库存需要处理
            derive_sku = goods_db.SpecOfSku.find_one({"type": 2, "sourceSkuId": sku["_id"], "deriveRegion": int(region_id)})
            derive_inv_stock = 0
            if derive_sku:
                derive_inv = goods_db.SkuInventory.find_one({"skuId": derive_sku["_id"]})
                derive_inv_stock = derive_inv["stock"]
            if inv["warehouseId"] != cur_warehouse_id:
                warehouse = goods_db.Warehouse.find_one({"_id": inv["warehouseId"]})
                cur_warehouse_id = inv["warehouseId"]
            price = goods_db.SkuPrice.find_one({"skuId": sku["_id"], "region": int(region_id), "isDeleted": False})
            review_total = goods_db.listing_review_total.find_one({"listingId": sku["listingId"], "regionId": int(region_id)})

            specs = [spec for spec in sku["key"].split(";")]
            size, color = "", ""
            for spec in specs:
                spec_id, spec_value_id = spec.split(":")
                spec_id, spec_value_id = int(spec_id), int(spec_value_id)
                if spec_id == SPEC_SIZE_ID:
                    try:
                        size = listing_spec_values[spec_id][spec_value_id]
                    except KeyError:
                        _size = goods_db.PropertyValue.find_one({"_id": spec_value_id})
                        if _size:
                            size = _size["value"]["en"]
                elif spec_id == SPEC_COLOR_ID:
                    try:
                        color = listing_spec_values[spec_id][spec_value_id]
                    except KeyError:
                        _color = goods_db.PropertyValue.find_one({"_id": spec_value_id})
                        if _color:
                            color = _color["value"]["en"]
            try:
                price["listPrice"] = price["listPrice"] if price["listPrice"] != 0 else price["salePrice"]
            except TypeError:
                continue
            image = ""
            if sku["images"]:
                image = sku["images"][0]
            else:
                image = listing["images"][0] if listing["images"] else ""
            hw_obj = {
                "goods_id": "%s_%s_%s" % (sku["listingId"], sku["_id"], region_id),
                "goods_name": listing["title"],
                "country_code": DEFAULT_COUNTRY_CODE,
                "country_site": region["code"],
                "goods_desc": listing["desc"],
                "sku_id": str(sku["_id"]),
                "sku_name": sku["title"],
                "spu_id": str(listing["_id"]),
                "spu_name": listing["title"],
                "brand_id": str(int(listing["brandId"])) if listing["brandId"] != -1 else "",
                "brand_name": str(brand["name"] if brand else ""),
                "merch_id": str(int(seller["_id"])),
                "merch_name": seller["name"],
                "min_class": third_category["name"],
                "first_class": first_category["name"],
                "second_class": second_category["name"],
                "third_class": third_category["name"],
                "min_class_id": str(int(third_category["_id"])),
                "first_class_id": str(int(first_category["_id"])),
                "second_class_id": str(int(second_category["_id"])),
                "third_class_id": str(int(third_category["_id"])),
                "online_flg": "1" if status == 1 else "0",
                "goods_stock": str(int(inv["stock"]) + derive_inv_stock),
                "goods_price": str(int(price["salePrice"])),
                "goods_dcn": "%.2f" % (price["salePrice"] / price["listPrice"],),
                "score": "%.2f" % (review_total["skuService"]["score"] / review_total["skuService"]["count"],) if review_total else "",
                "comment_cnt": int(review_total["skuService"]["count"]) if review_total else 0,
                "color": color,
                "size": size,
                "is_24h_ship": 1 if int(warehouse["regionId"]) == int(region_id) else 0,
                "extend_attrs": json.dumps({"shipped_from": warehouse["location"]}),
                "shop_id": str(int(listing["storeId"])),
                "source_status": str(1),
                "activity_type": 0,
                "price_type": 0,
                "price_discount": "",
                "image_link": format_image_url(image),
                "goods_link": formar_lisitng_url(listing["_id"])
            }
            data = json.dumps(hw_obj)
            f.write(data + "\n")
    skus_cursor.close()
    f.close()
    f2.close()
    print("cursor close")
except Exception as err:
    skus_cursor.close()
    f.close()
    f2.close()
    print("cursor close")
    raise err
