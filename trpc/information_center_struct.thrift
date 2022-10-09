enum ReportType {
    STANDARD_SALES_REPORT = 1,
    SALES_TOP_REPORT = 2
}

const map<i16, string> REPORT_TYPE_MAY = {1: "sales_normal", 2: "sales_top"}
const string REPORT_SALES_NORMAL = "sales_normal"
const string REPORT_SALES_TOP = "sales_top"

const string DIMENSION_DATE_TIME = "dateTime"
const string DIMENSION_CATEGORY = "category"
const string DIMENSION_SELLER = "seller"
const string DIMENSION_SALES_REGIONS = "salesRegions"
const string DIMENSION_STORE = "store"
const string DIMENSION_LISTING = "listing"
const string DIMENSION_SKU = "sku"
const string DIMENSION_PAYMENT_METHOD = "paymentMethod"
const string DIMENSION_DELIVERY_REGION = "deliveryRegion"
const string DIMENSION_DELIVERY_WAREHOUSE = "deliveryWarehouse"

const list<string> DIMENSION_SPECIAL = ["listing", "sku", "paymentMethod"]

const string DIMENSION_DATE_TIME_ID = "dateTimeId"
const string DIMENSION_CATEGORY_ID = "categoryId"
const string DIMENSION_SELLER_ID = "sellerId"
const string DIMENSION_SALES_REGIONS_ID = "salesRegionsId"
const string DIMENSION_STORE_ID = "storeId"
const string DIMENSION_LISTING_ID = "listingId"
const string DIMENSION_SKU_ID = "skuId"
const string DIMENSION_PAYMENT_METHOD_ID = "paymentMethodId"
const string DIMENSION_DELIVERY_REGION_ID = "deliveryRegionId"
const string DIMENSION_DELIVERY_WAREHOUSE_ID = "deliveryWarehouseId"

const map<string, string> DIMENSION_SPECIAL_MAP_ID = {"listing": "listingId",
"sku": "skuId", "paymentMethod": "paymentMethodId"}

const string TARGETE_GMV = "gmv"
const string TARGETE_ORDER_COUNT = "orderCount"
const string TARGETE_SUCCESS_GMV = "successGmv"
const string TARGETE_REJECT_AMOUNT = "rejectAmount"
const string TARGETE_ITEM_TOTAL = "itemTotal"
const string TARGETE_PRODUCT_QTY = "productQty"
const string TARGETE_POSTAGE = "postage"
const string TARGETE_COINS_REDEEM = "coinsRedeem"
const string TARGETE_VOUCHER_REDEEM = "voucherRedeem"
const string TARGETE_RANK = "rank"
const string TARGETE_SUCCESS_ORDER_COUNT = "successOrderCount"

enum TimeDimensionType {
    YEAR = 1,
    QEARTERLY = 2,
    MONTH = 3,
    WEEK = 4,
    DAY = 5
}

enum CategoryDimensionType {
    FIRST = 1,
    SECONDARY = 2,
    THIRD = 3
}

enum SalesRegionsDimensionType {
    REGION = 1,
    STATE = 2,
    CITY = 3,
    AREA = 4
}

enum ListingDimensionType {
    LISTING = 1,
    SKU = 2
}

enum SellerDimensionType {
    SELLER = 1,
    STORE = 2
}

enum OrderWay {
    INC = 1,
    DEC = 2
}

struct SalesTarget {
    1: i16 id,
    2: string target,
    3: bool isSelected,
    4: optional string displayName
}

struct DimensionStructure {
    1: i16 depthId,
    2: string depthName
}

struct SalesDimension {
    1: i16 id,
    2: string dimension,
    3: bool isSelected,
    4: i16 depth,
    5: optional string displayName,
    6: optional string selectType,
    7: optional list<DimensionStructure> structure
}

struct NormalSaleData {
    1: optional string category,
    2: optional i64 categoryId,
    3: optional string paymentMethod,
    4: optional string paymentMethodId,
    5: optional string dateTime,
    6: optional i64 dateTimeId,
    7: optional string deliveryRegion,
    8: optional i16 deliveryRegionId,
    9: optional string seller,
    10: optional i64 sellerId,
    11: optional string deliveryWarehouse,
    12: optional i64 deliveryWarehouseId,
    13: optional double gmv,
    14: optional i64 orderCount,
    15: optional double itemTotal,
    16: optional double postage,
    17: optional double coinsRedeem,
    18: optional double voucherRedeem,
    19: optional string salesRegions,
    20: optional i64 salesRegionsId,
    21: optional double successGmv,
    22: optional double rejectAmount,
    23: optional i64 productQty,
    24: optional i64 successOrderCount
}

struct SalesDataList {
    1: i32 count,
    2: list<NormalSaleData> dataList
}

struct TopSaleData {
    1: optional string category,
    2: optional i64 categoryId,
    3: optional string paymentMethod,
    4: optional string paymentMethodId,
    5: optional string dateTime,
    6: optional i64 dateTimeId,
    7: optional string deliveryRegion,
    8: optional i16 deliveryRegionId,
    9: optional string seller,
    10: optional i64 sellerId,
    11: optional string deliveryWarehouse,
    12: optional i64 deliveryWarehouseId,
    13: optional double gmv,
    14: optional i64 orderCount,
    15: optional double itemTotal,
    16: optional double postage,
    17: optional double coinsRedeem,
    18: optional double voucherRedeem,
    19: optional string salesRegions,
    20: optional i64 salesRegionsId,
    21: optional double successGmv,
    22: optional double rejectAmount,
    23: optional i64 productQty,
    24: optional i32 rank,
    25: optional string store,
    26: optional i64 storeId,
    27: optional string listing,
    28: optional i64 listingId,
    29: optional string sku,
    30: optional i64 skuId,
    31: optional i64 successOrderCount
}

struct TopDataList {
    1: i32 count,
    2: list<TopSaleData> dataList
}

enum SaleOrderState {
    UNPAID = 1,
    UNCONFIRMED = 2,
    UNSHIPPED = 3,
    INTRANSIT = 4,
    ACCEPT = 5,
    WAIT = 6,
    CANCEL = -1,
    REJECT = -2,
    PART_ACCEPT = -3,
    ALL = 0
}

const map<i16, string> ORDER_STATE_MAY = {
    1: "pend_pay", 2: "pend_confirm", 3: "pend_ship", 4: "in_transit",
    5: "accept", -1: "cancel", -2: "reject"}

enum PaymentMethod {
    ONLINE = 1,
    COD = 2,
    PRE = 3
}

const map<i16, string> PAYMENT_TYPE_MAY = {1: 'online', 2: 'cod', 3: 'pre'}

struct SaleOrderDetail {
    1: i64 id,
    2: i64 orderId,
    3: i64 skuId,
    4: i32 count,
    5: i64 salePrice,
    6: i64 dealPrice,
    7: i32 priceRevision,
    8: i32 coinRedeem,
    9: i32 coins,
    10: i32 voucherRedeem,
    11: i32 discount,
    12: i32 vat,
    13: i32 amount,
    16: string createdAt,
    17: optional i64 listingId,
    18: optional i32 categoryId
}

enum OrderType {
    NORMAL = 1,
    FLASH = 2,
    PRIZE = 3,
    REDEEM = 4,
    MIX = 5,
    GROUP = 6,
    ALL = 0
}

const map<i16, string> ORDER_TYPE_MAP = {
1: 'normal', 2: 'flash', 3: 'luckyDraw', 5: 'mixed', 4: 'redeem',
6: 'groupBuy', 7: 'promotion'}

const string DW_ORDER_END_TIME = "2099-12-31T00:00:00.000Z"

struct SaleOrder{
    1: i64 id,
    2: SaleOrderState state,
    3: string code,
    4: i16 regionId,
    5: i64 billId,
    6: i64 batchId,
    7: i32 storeId,
    8: i64 accountId,
    9: i64 addressId,
    10: i32 warehouseId,
    11: i32 warehouseRegionId,
    12: i16 postage,
    13: i16 postageDiscount,
    14: i16 postageRedeem,
    15: i32 orderAmount,
    16: i32 itemTotal,
    17: i32 coinRedeem,
    18: i32 coins,
    19: i32 voucherRedeem,
    20: i32 payAmount,
    21: i32 discount,
    22: i32 vat,
    23: i32 itemCount,
    24: i32 skuCount,
    25: PaymentMethod paymentMethod,
    26: OrderType orderType,
    27: string createdAt,
    28: optional string paidAt,
    29: optional string confirmAt,
    30: optional string shippedAt,
    31: optional string closedAt,
    32: optional bool userConfirmed,
    33: optional string userConfirmedAt,
    34: optional i32 sellerId,
    35: optional i32 areaId,
    36: optional i32 cityId
}

struct OrderList {
    1: SaleOrder order,
    2: list<SaleOrderDetail> orderDetails
}

struct ActualUserAndContact {
    1: i32 userId,
    2: string nick,
    3: string createdTime,
    4: i16 regionId,
    5: string phoneNumber,
    6: string mailbox,
    7: string facebookAccount
}

struct DimSeller {
    1: i32 id,
    2: i16 regionId,
    3: string name,
    4: string phone
}

struct DimStore {
    1: i32 id,
    2: i16 regionId,
    3: i16 sellerRegionId,
    4: i32 sellerId,
    5: string name
}

struct DimWarehouse {
    1: i32 id,
    2: string name,
    3: i16 regionId
}

struct DimCat1 {
    1: i32 id,
    2: string name
}

struct DimCat2 {
    1: i32 id,
    2: string name,
    3: i32 cat1Id
}

struct DimCat3 {
    1: i32 id,
    2: string name,
    3: i32 cat1Id,
    4: i32 cat2Id
}