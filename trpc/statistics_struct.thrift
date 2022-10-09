const string UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
const string TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
const i16 COUNT_TOP_DAY_LIMIT = 92
const i16 DNA_SERVICE_PORT = 8000

struct OneListing {
    1: i64 listingId,
    2: i32 count
}
enum SoldSortType {
    ACTUAL_SOLD = 1,
    ORDER_COUNT = 2,
    REJECTED = 3,
    BUYER_COUNT = 4,
    REVIEWS = 5
}
enum ProductUpdateType {
    ORDER_COUNT = 1,
    ACTUAL_SOLD = 2,
    REJECTED = 3,
    REVIEWS = 4,
    MULTIPLE = 0
}
enum PromotionType {
    FLASH = 1,
    PRIZE = 2,
    REDEEM = 3,
    NONE = 0
}
struct OrderSku {
    1: i64 saleOrderDetailId,
    2: i32 storeId,
    3: i64 accountId,
    4: i64 listingId,
    5: i64 skuId,
    6: PromotionType activityType=0,
    7: i64 activityId=0,
    8: i64 saleOrderId,
    9: i16 count,
    10: i64 salePrice,
    11: i64 dealPrice,
    12: i32 discount,
    13: i32 coin,
    14: i32 coinRedeem,
    15: i32 voucherRedeem,
    16: i32 warehouseId,
    17: i32 vat=0,
    18: i16 status,
    19: string createdAt,
    20: i16 regionId
}

enum PaymentMethods {
    ONLINE = 1,
    COD = 2,
    PRE = 3
}

enum PackageStatus {
    UNSHIPPED = 1,
    SHIPPED = 2,
    DISPATCHING = 3,
    SELLER_DELIVERED = 5,
    ACCEPT = 4,
    REJECT = -1,
    CANCEL = -2
}

enum Courier {
    E_COURIER = 1,
    E_DESH = 2,
    SELF = 3
}

enum DeliveryMethod {
    PLATFORM_CARRIER = 1,  // 平台派送，平台统收
    SHOP_SELF_DELIVERY = 2,  // 店铺自己派送，⾮平台统收
    SHOP_SELF_SET = 3, // 平台派送, 运费自己设置，⾮平台统收
    ALL = 0
}

struct ClearingOrder {
    1: string packageCode,
    2: i16 SHOContain,
    3: i64 saleOrderId,
    4: bool isSelfDelivery,
    5: PaymentMethods payMethod,
    6: string createdAt,
    7: i64 accountId,
    8: i32 itemTotal,
    9: i16 postage,
    10: i32 discount,
    11: i16 coinRedeem,
    12: i16 platVoucher,
    13: i16 storeVoucher,
    14: i32 payAmount,
    15: double payFee,
    16: i16 regionId,
    17: i32 warehouseId, // operateFee
    18: PackageStatus status,
    19: string terminalDeliveryCode,
    20: string completedAt,
    21: double commissionRate,
    22: i16 operateFee,
    23: i32 storeId,
    24: string monthClearingCode,
    25: Courier terminalDeliveryId,
    26: DeliveryMethod deliveryMethod
}

enum ClearingStatus {
    PENDING_CONFIRM = 1,
    CONFIRMED = 2,
    QUESTION = -1
}

const list<i16> CLEARING_IN_CONFIRMABLE = [
ClearingStatus.PENDING_CONFIRM, ClearingStatus.QUESTION]

const list<i16> CLEARING_CAN_AUTO_CONFIRM = [
ClearingStatus.PENDING_CONFIRM, ClearingStatus.CONFIRMED]

struct ClearingCorrection {
    1: i32 correctionAmount,
    2: optional string information,
    3: optional list<string> annex
}

struct MonthlyClearingSummary {
    1: string code,
    2: ClearingStatus status,
    3: i16 year,
    4: i16 month,
    5: i32 storeId,
    6: i32 regionId,
    7: bool isSelfDelivery,
    8: i64 itemTotal,
    9: i32 discount,
    10: i32 totalPostage,
    11: i32 platPostage,
    12: i32 storePostage,
    13: i64 payAmount,
    14: i32 coinRedeem,
    15: i64 settlementCoinRedeem,
    16: i32 platVoucher,
    17: i32 storeVoucher,
    18: i64 settlementStoreVoucher,
    19: i64 payFee,
    20: i64 commissionBase,
    21: i64 commission,
    22: i32 operateFee,
    23: ClearingCorrection correction,
    24: i64 settlementAmount,
    25: string createdAt,
    26: optional i32 afterSaleAmount,
    27: optional i32 reward,
    28: optional i32 penalty,
    29: optional i32 logisticsCost,
    30: optional string lastUpdatedAt,
    31: i64 selfDeliveryCODAmount,
    32: i64 selfDeliveryCODPostage
}

enum ClearingOperateCode {
    CREATE = 3,
    CORRECT = 1,
    CONFIRMED = 2,
    SYS_CONFIRMED = 4,
    QUESTION = -1
}

enum Operator {
    CUSTOMER = 1,
    SELLER = 2,
    ADMIN = 3,
    LOGISTIC = 4,
    SYSTEM = 5
}

const map<i16, string> OPERATOR_MAP = {1: "customer", 2: "store", 3: "perfee", 4: "logistics", 5: "system"}

struct ClearingLog {
    1: string createdAt,
    2: ClearingOperateCode operateCode,
    4: string operator,
    3: i32 operatorId
}

struct MonthlyClearingsRes {
    1: i32 count,
    2: list<MonthlyClearingSummary> monthlyClearings
}

enum RequestFrom {
    SELLER = 1,
    DNX = 2
}

struct ClearingOrdersRes {
    1: i32 count,
    2: list<ClearingOrder> clearingOrders
}
