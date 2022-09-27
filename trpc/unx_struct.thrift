# Error Code
const i16 ERROR_REPEAT_CREATION = 1000
const i16 ERROR_LOCAL_SUB_NOT_FOUND = 1001

struct LocalizedSubsidiary {
    1: required i32 id,
    2: required i32 regionId,
    3: required string name,
    4: required string callingCode,
    5: required string code,
    6: required string flag,
    7: required string currencySymbol,
    8: required string timeZone,
    9: optional bool mainSwitch,
    10: optional bool subSwitch,
    11: optional bool allowedAddStore,
    12: optional string domain,
    13: optional string exchangeRateRef,  // 汇率参考
    14: optional i32 firstFreight,  // 头程运费（含清关）
    15: optional string currency,
    16: optional string language
}

struct LocalizedSubsidiaries {
    1: required i32 total,
    2: required list<LocalizedSubsidiary> localizedSubsidiaries
}