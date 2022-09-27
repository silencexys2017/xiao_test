include "constants.thrift"

// 仓库类型
enum PropertyValueSource {
    // 平台预置，对所有卖家可见
    PRESET = 1,
    // 卖家（店铺自定义）
    SELLER = 2,
    // 外部系统导入（供应商以及其他第三方），不可见
    EXTERNAL = 3
}

struct PropertyValue {
    1: i64 id,
    2: string value,
    3: optional PropertyValueSource source, // #TODO refactor to required
    4: optional i64 references, // #TODO refactor to required
    5: optional i64 seller_id,
    6: optional i64 store_id,
    7: optional bool enabled, // #TODO refactor to required
    8: optional string created_at, // #TODO refactor to required
    9: optional string updated_at
}

struct Property {
    1: i64 id,
    2: string name,
    3: list<PropertyValue> values
}

struct PropertyId {
    1: i64 pid,
    2: i64 pvid
}

struct SpecProperty {
    1: i64 id,
    2: string name,
    3: bool withImage,
    4: list<PropertyValue> values
}
