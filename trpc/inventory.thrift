include "exceptions.thrift"

struct SkuStockItem {
    1: i64 sku_id,
    2: i64 warehouse_id,
    3: i64 qty
    4: i64 soId
}

struct SkuInventoryItem {
    1: i64 warehouse_id,
    2: i64 vendor_id,
    3: string sku_code,
    4: i64 stock,
    5: i64 reservation
}

struct SkuInventories {
    1: i64 sku_id,
    2: i64 listing_id,
    3: list<SkuInventoryItem> inventories,
}

enum SkuInventoryLogType {
    INITIALIZATION = 1       // 初始化库存
    ORDER_OUT = 2            // 订单出存
    REJECTION_IN = 3         // 订单拒收入库
    STOCK_IN = 4             // 备货入库
    CANCELLATION_IN = 5      // 订单取消入库
}

struct SkuInventoryLog {
    1: required i64 id
    2: required i64 skuId
    3: required SkuInventoryLogType type
    4: required i64 stockChange
    5: required i64 currentStock
    6: required string createdAt
    7: optional bool isLatest
    8: optional i64 sourceOrderId
}
