include "constants.thrift"

// OFS仓库类型
enum OfsWarehouseType {
    // 平台物理仓
    PLATFORM_PHYSICAL = 1,
    // 平台虚拟仓
    PLATFORM_VIRTUAL = 2
    // 店铺虚拟仓
    STORE_VIRTUAL = 3
}

// 仓库类型
enum WarehouseType {
    // 物理仓
    PHYSICAL = 1,
    // 虚拟仓
    VIRTUAL = 2
}

// 仓库用途（角色）
enum WarehouseRole {
    // 存储型（保管）仓库
    STORAGE = 1

    // 逻辑虚设仓库
    DUMMY = 2,

    // 中转仓库
    TRANSSHIPMENT = 3

    // 退货仓
    RETURNED = 4
}

// 仓库状态（管理视角）
enum WarehouseState {
    // 停用状态
    CLOSED = 0

    // 正常营运状态
    OPEN = 1
}

// 仓库申请单状态
enum WarehouseApplicationState {
    // 待审核
    APPLYING = 0,

    // 申核通过
    APPROVED = 1,

    // 被拒绝（驳回）
    REJECTED = 2
}

// 仓库
struct Warehouse {
    1: i64 id,
    2: i64 region_id,
    3: string name,
    4: string location,
    5: bool international_shipping,
    6: WarehouseType type,
    7: WarehouseRole role,
    8: WarehouseState state,
    9: list<constants.SupportedPaymentMethods> payment_methods
}

// 创建仓库申请（卖家自有虚拟仓）
struct WarehouseApplication {
    1: i64 application_id,
    2: i64 region_id,
    3: i64 seller_id,
    4: i64 store_id,
    5: string warehouse_name,
    6: string location,
    7: bool seller_sharing,
    8: WarehouseApplicationState state,
    9: string created_at,
    10: optional string updated_at,
    11: optional i64  operator_id,
    12: optional string reject_reason,
    13: optional Warehouse warehouse
}

// 备货仓使用申请
struct StorageWarehouseApplication {
    1: i64 application_id,
    2: i64 region_id,
    3: i64 seller_id,
    4: i64 store_id,
    5: i64 warehouse_id,
    6: WarehouseApplicationState state,
    7: string created_at,
    8: optional string updated_at,
    9: optional i64  operator_id,
    10: optional string reject_reason,
    11: optional Warehouse warehouse
}
