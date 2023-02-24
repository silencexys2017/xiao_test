# -*- coding: utf-8 -*-

import unittest
import thriftpy2
import thrift_connector.connection_pool as connection_pool
import thriftpy2.protocol.json as proto

DEF = thriftpy2.load("order_struct.thrift")

b = DEF.PartnerProduct(
    skuId="13443", mapStr={"dkf": DEF.AreaIdName(id=34324, name="xiao")})

c = DEF.GatewayStatus

print(dir(c))
print(c.__dict__)
def struct_to_json():
    json = proto.struct_to_json(c)
    print(json)
    assert {"id": 13, "phones": ["5234", "12346456"]} == json


def address_areas():
    data = {"areaNames" : {
                "1" : {
                        "1348" : "Baringo"
                },
                "2" : {
                        "1003439" : "Baringo Central"
                },
                # "3" : {
                #         "1000032464" : "TestC"
                # }
        }}
    res = DEF.Address()
    res.areaLevel = len(data.get("areaNames", {}))
    areas = {}
    area_list = []
    for index in sorted(data.get("areaNames", {})):
        item = DEF.AreaIdName(
            id=int(list(data["areaNames"][index].keys())[0]),
            name=list(data["areaNames"][index].values())[0])
        areas[index] = item
        area_list.append(item)
        print(index, res.areaLevel)
        if index in ["2", 2] and res.areaLevel == 2:
            print("3432423")
            areas[3] = item
    res.areaNames = areas
    res.areaNameList = area_list
    print(res)


# struct_to_json()
address_areas()




