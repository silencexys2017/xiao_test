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


struct_to_json()

print(DEF.LOG_STATE_MAP_AF_STATE_BEFORE_AND_AFTER)