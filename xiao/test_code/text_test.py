import json
import hashlib
from dapr.clients import DaprClient
from typing import Dict, Optional, Union, Sequence, List


def sign_md5():
    thriftpy2.load("./thrift_app/order_struct.thrift")

    a = {"networkBaseInfoVo":{"address":"Joy803001-shopinfo","areaCode":"100101","areaId":289,"areaName":"Central Business District","businessName":None,"businessTime":"00:00","businessType":3,"cityId":1,"cityName":"Nairobi","codStatus":0,"countryCode":"KE","createdAt":1627973428,"id":718864905,"isSupportBigPackage":None,"isSupportCOD":False,"latitude":None,"longitude":None,"parentId":1,"pauseEndTime":1609516800,"pauseStartTime":1609430400,"pickingCode":"1-1009","remark":None,"stationCode":"803-1","stationDesc":None,"stationDescRid":None,"stationLevel":"2","stationName":"Joy803001","stationNameRid":None,"stationScore":None,"stationSize":None,"stationSubType":None,"stationType":2,"status":1,"supplierId":None,"updatedAt":1669185072},"networkCoverageVoList":None,"networkStaffInfoVoList":[{"address":"Joy803001-shopinfo","age":None,"createdAt":1627973428,"email":"Joy803001@11.com","firstName":"Joy803001","gender":None,"id":42608,"identifyNo":"Joy803001 Joy803001","identifyType":None,"lastName":"Joy803001","mobileNo":"793007894","parentId":None,"positionId":None,"stationId":718864905,"status":0,"telephoneNo":None}]}

    params = json.dumps(a, separators=(',', ':'), ensure_ascii=False)

    sign_1 = hashlib.md5((params + "12345678").encode(
        encoding='utf-8')).hexdigest()
    print(sign_1)


def argus_kw(kwargs):
    print(**kwargs)


def dapr_client_set():
    dapr_client = DaprClient()
    dapr_client.save_state("dev", "test", "yongsheng")


def dapr_client_get():
    dapr_client = DaprClient()
    dapr_client.get_state(state_store_name, state_key)


def xiao_test(value: Union[bytes, str]):
    print(value)



dapr_client_set()
# xiao_test({"xiao": 1})