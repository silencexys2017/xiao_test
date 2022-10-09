
def ratio_split_integer(split_num, each_ratio):
    # each_ratio: for example {1: float(1) / 5, 2: float(2) / 5}
    print(split_num, each_ratio)
    split_list = [int(round(float(item) * split_num)) for item in
                  each_ratio.values()]
    print(split_list)
    amount = sum(split_list)
    rest_num = abs(split_num - amount)
    index = 0
    number = 0
    if split_num < amount:
        for num in split_list:
            if num == 0:
                index += 1
                continue
            num = num - 1
            split_list[index] = num
            index += 1
            number += 1
            if number == rest_num:
                break
    elif split_num > amount:
        for num in split_list:
            num = num + 1
            split_list[index] = num
            index += 1
            if index == rest_num:
                break

    return dict(zip(each_ratio.keys(), split_list))


def avg_split_discounts(items, discounts):
    if not discounts:
        return
    dis_di = {}
    dis_amount = {}
    for it in discounts:
        dis_di[it["discountId"]] = it["discount"]
        dis_amount[it["discountId"]] = 0

    for it in items:
        if it.get("discountId"):
            dis_amount[it["discountId"]] += it["salePrice"] * it["count"]
    all_av_di = {}
    for key, value in dis_di.items():
        av_di = {}
        for it in items:
            if it.get("discountId") == key:
                av_di[(it["skuId"], it["activityType"], it["activityId"])] = \
                    float(it["salePrice"] * it["count"]) / dis_amount[key]
        res = ratio_split_integer(value, av_di)
        print(res)
        all_av_di.update(res)

    for it in items:
        if all_av_di.get((it["skuId"], it["activityType"], it["activityId"])):
            it["discount"] = all_av_di[
                (it["skuId"], it["activityType"], it["activityId"])]
        else:
            it["discount"] = 0

    print(items)


items = [
    {"skuId": 1, "activityType": 1, "activityId": 1, "salePrice": 343,
     "count": 3, "discountId": 1},
    {"skuId": 2, "activityType": 1, "activityId": 1, "salePrice": 543,
     "count": 3, "discountId": 1},
    {"skuId": 5, "activityType": 1, "activityId": 1, "salePrice": 1000,
     "count": 3, "discountId": 2},
    {"skuId": 5, "activityType": 2, "activityId": 1, "salePrice": 1000,
     "count": 3},
    {"skuId": 6, "activityType": 2, "activityId": 1, "salePrice": 433,
     "count": 3, "discountId": 2},
]

discounts = [
    {"discountId": 1, "discount": 20},
    {"discountId": 2, "discount": 20},
    {"discountId": 3, "discount": 20},
]


if __name__ == "__main__":
    avg_split_discounts(items, discounts)