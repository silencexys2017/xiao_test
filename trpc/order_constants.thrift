enum FromOrigin {
    DNX = 1,
    SELLER = 2
}

enum BillPayStatus {
    UNPAID = 1,
    PAID = 2,
    REFUND = 3
}

enum Courier {
    E_COURIER = 1,
    E_DESH = 2,
    SELF = 3,
    EXFCS = 4,
    SAGAWA = 5,
    X_ED = 7
}

const map<i16, string> MAP_LOGISTICS_ID_TO_NAME =
    {1: "eCourier", 2: "eDesh", 3: "self", 4: "exFcs", 5: "sagawa", -1: "other"}

enum PackageType {
    SHIP_PACKAGE = 1,
    DELIVERY_ORDER = 2
} // 为了区分派送的包裹类型

enum PaymentMethods {
    ONLINE = 1,
    COD = 2,
    PRE = 3
}

enum AvailablePayment {
    YES = 1,
    PART = 2,
    NO = 3
}

enum OrderTimeType {
    create = 1,
    confirm = 2
}

enum PromotionPlatform {
    ACTOR = 1
}

const list<i16> PAY_METHODS = [PaymentMethods.ONLINE, PaymentMethods.COD,
PaymentMethods.PRE]

const list<i16> CONTAIN_ONLINE_METHODS = [PaymentMethods.ONLINE, PaymentMethods.PRE]

const list<i16> CONTAIN_COD_METHODS = [PaymentMethods.COD, PaymentMethods.PRE]

enum PayStatus {
    UN_PAY = 1
    PAID = 2
}

const i16 UN_PAID_STATUS = 1

enum PaymentType {
    ONLINE = 1,
    COD = 2,
    REDEEM = 3,
    VOUCHER_REDEEM = 4
}

const list<i16> REDEEM_STYLES = [3, 4]

enum BillStatus {
    NEW_CREATE = 1,
    ONCE_PAID = 2, // valid
    COMPLETE = 3,
    CANCEL = -1,
    ALL = 0
}

enum PayBillStatus {
    PENDING = 1,
    IN_PROGRESS = 2,
    OVERDUE = 3,
    COMPLETE = 4,
    PART_COMPLETE = 5
}

enum SaleOrderStatus {
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

const map<i16, string> SO_STATE_MAP_TIME = {1: "createdAt", 2: "paidAt",
3: "confirmAt", 4: "shippedAt", 5: "closedAt", 7: "deliveredAt", -1: "closedAt",
-2: "closedAt", -3: "closedAt"}
// SaleOrderStatus._NAMES_TO_VALUES.values() --> [1,2,3,4,5,-1,-2,-3]
// SaleOrderStatus._ttype --> 8
// SaleOrderStatus.__dict__
const list<i16> SO_CLOSED_STATUS = [-1, -2, -3, 5]
const list<i16> SO_UN_COMPLETE_STATUS = [1, 2, 3, 4]
const list<i16> SO_CAN_CANCEL_STATUS = [1, 2, 3, 6]
const list<i16> SO_VALID_STATUS = [2, 3, 4, 5, 6]
const list<i16> SO_PG_CREATE_STATUS = [3, 4]
const list<i16> SO_CAN_CONFIRM = [2, 6]

// saleOrderType
enum SoType {
    NORMAL = 1,
    FLASH = 2,
    PRIZE = 3,
    REDEEM = 4,
    MIX = 5,
    GROUP = 6,
    ALL = 0
}
const list<i16> SO_TYPES = [1, 2, 3, 4, 5]

// PromotionType
enum PromotionType {
    FLASH = 1,
    PRIZE = 2,
    REDEEM = 3,
    GROUP = 5
}

// saleOrderType and PromotionType mapping
const map<i16, i16> PRO_MAP_SO_TYPE = {0: 1, 1: 2, 2: 3, 3: 4, 5: 6}

enum DeliveryMethod {
    PLATFORM_CARRIER = 1,  // 平台派送，平台统收
    SHOP_SELF_DELIVERY = 2,  // 店铺自己派送，⾮平台统收
    SHOP_SELF_SET = 3, // 平台派送, 运费自己设置，⾮平台统收
    ALL = 0
}

const i16 SOD_CANCEL_STATUS = -1

enum ShipOrderStatus {
    COLLECTING = 1,
    COLLECTED = 2,
    PACKAGED = 3,
    SHIPPED = 4,
    DISPATCHING = 5,
    SELLER_DELIVERED = 7,
    ACCEPT = 6,
    REJECT = -1,
    CANCEL = -2,
    RETURN = -3
}

enum ShipOrderSubform {
    NOT_SPLIT = 0,
    NATIVE = 1,
    OUT_OF_STOCK = 2,
    DERIVED = -1
}

const list<i16> SHO_UN_SHIPPED_STATUS = [1, 2, 3]
const list<i16> SHO_COMPLETE_STATUS = [6, -1, -2, -3]
const list<i16> SHO_REJECT_STATUS = [-1] //sho_type = 5
const list<i16> SHO_ACCEPT_STATUS = [6]  // sho_type = 3
const list<i16> SHO_IN_TRANSIT_STATUS = [4, 5] // sho_type = 2
const list<i16> SHO_IN_DISPATCH_STATUS = [5]

enum PackageStatus {
    UNSHIPPED = 1,
    SHIPPED = 2,
    DISPATCHING = 3,
    SELLER_DELIVERED = 5,
    ACCEPT = 4,
    REJECT = -1,
    CANCEL = -2,
    RETURN = -3
}

const list<i16> SPG_CLOSED_STATUS = [4, -1, -2]

enum USER_ORDER_LIST_TYPE {
    PENDING_DISPATCH = 1, // SO
    IN_TRANSIT = 2, // SPG
    ACCEPT = 3, // SPG
    CANCEL = 4, // SO
    REJECT = 5 // SPG
    IN_TRANSIT_UN_CONTAIN_DELIVERY = 6
    IN_DELIVERY = 7 // SPG
}
const list<i16> USER_SOS_TYPES = [1, 4] // 1: pendingDispatch, 2: cancel
const list<i16> USER_SPG_LIST_TYPES = [2, 3, 5, 6, 7] // 2: in_transit; 3: accept; 5: reject
const map<i16, list<i16>> USER_ORDER_STATUS_MAP =
    {1:[2, 3], 2: [2, 3, 5], 3: [4], 4: [-1], 5: [-1], 6: [2], 7: [3, 5]}

enum CANCEL_REASON {
    USER_APPLY = 1,
    NO_STOCK = 2,
    OTHER = 3,
    NO_REASON = 4
}
enum RejectionReason {
    DAMAGED = 1,
    NOT_SAME = 2,
    NO_REASON = 3
}
// ShortageOrder
//（0：所有， 1：尚未退款，  2：退款中，  3：退款已完成， 4：有退款， 5： 不需退款）
enum ShortageOrderType {
    ALL = 0
    UN_CREATED = 1,
    IN_REFUNDING = 2,
    REFUNDED = 3,
    HAVE_REFUND = 4,
    NO_REFUND = 5
}
const i16 ST_OD_ALL = 0
const i16 ST_OD_HAVE_REFUND = 4
const i16 ST_OD_NO_REFUND = 5

enum Vendor {
    SELF = 1,
    ALIEXPRESS = 2,
    SHOPPO = 3,
    NDBESTOFFER = 4
}

enum TradeSkuType {
    pendingDispatch = 1,
    inTransit = 2,
    inDelivery = 3,
    completed = 4,
    rejected = 5
}
const map<i16, i16> MAP_SKU_STATE_SO_STATUS = {1: 3}

enum ParcelLogStatus {
    NEW = 0,
    FAIL = -1,
    SUCCESS = 1
}
const list<i16> PARCEL_LOG_STATUS = [-1, 0, 1]

enum ParcelLogType {
    api = 1,
    manual = 2
}
const list<i16> PARCEL_LOG_TYPE = [1, 2]

enum ECourierPaymentMethod {
    COD, // Cash On Delivery
    POS, // Point of Sale
    MPAY, // Mobile Payment
    CCRD // Card Payment
}
const list<string> ECOURIER_PAY_METHOD = ["COD", "POS", "MPAY", "CCRD"]

enum ParcelIsAnonymous {
    ExposeIdentity = 0,
    Anonymous = 1
}
const list<i16> PARCEL_ANONYMOUS_TYPE = [0, 1]
# max cod rule
const i16 MAX_COD_IN_TRANSIT = 100  # 6
const i16 MAX_SO_COD_AMOUNT = 1200
const i16 MAX_BATCH_COD_AMOUNT = 3000
const i16 MAX_DAY_OVERSEA = 10
const i16 MAX_DAY_INTERNAL = 35
const string COD_AMOUNT_LIMIT = "The order amount exceeds the COD approved amount."
const string COD_IN_TRANSIT_LIMIT = "You have reached the maximum limit of COD orders. Please place order after former ones completed or choose online payment."
const string COD_REJECT_LIMIT = "You recently rejected more orders for no reason. Please use Online Payment After successful delivery, you will be allowed to submit a COD order."
# delivery time
const string DELIVERY_PERIOD_0 = "any"
const string DELIVERY_PERIOD_1 = "10:30am - 1:00pm"
const string DELIVERY_PERIOD_2 = "1:00pm - 4:00pm"
const string DELIVERY_PERIOD_3 = "4:00pm - 7:00pm"
const list<i16> DELIVERY_PERIOD = [0, 1, 2, 3]

# Error code
const i16 ERROR_SYS_DB = 1000
const i16 SALEORDER_NOT_FOUND = 7040
const i16 STARTINDEX_PARAM_ERROR = 7041
const i16 ERROR_INPUT_PARAMETER= 7042
const i16 SHIP_ORDER_NOT_FOUND = 7043
const i16 SHIPPACKAGE_NOT_FOUND = 7044
const i16 PARAM_PACKAGE_STATUS_ERROR = 7045
const i16 RECEIVE_AMOUNT_ERROR = 7046
const i16 PARAM_DELIVER_STATUS_ERROR = 7047
const i16 TRADE_SKU_TYPE_ERROR = 7048
const i16 ORDER_LOG_NOT_FOUND = 7049
const i16 ERROR_BILL_NOT_FOUND = 7050
const i16 ERROR_ORDER_PLACE_TOO_SHORT = 7051
const i16 ERROR_PARCEL_LOG_STATUS = 7052
const i16 ERROR_PARCEL_LOG_TYPE = 7053
const i16 ERROR_PARCEL_LOG_NOT_FOUND = 7054
const i16 ERROR_PARCEL_LOG_HAVE_EXISTED = 7055
const i16 ERROR_ECOURIER_PAY_METHOD_NOT_FOUND = 7056
const i16 ERROR_PARCEL_ANONYMOUS_TYPE = 7057
const i16 ERROR_REQUEST_EXCEPTION = 7059
const i16 ERROR_MAPPING_ADDRESS_NOT_FOUND = 7060
const i16 ERROR_ECOURIER_CITY_AND_AREA = 7061
const i16 ERROR_PAY_BILL_NOT_FOUND = 7062
const i16 ERROR_INITIATE_SSL_PAYMENT_FAIL = 7063
const i16 ERROR_HASH_VALIDATION_PARAMS_FAIL = 7064
const i16 ERROR_TRANS_HAVE_PAID = 7065
const i16 ERROR_FIND_TRANS_FAIL = 7066
const i16 ERROR_PAY_TRANS_NOT_FOUND = 7067
const i16 ERROR_SSL_RETURN_DATA = 7068
const i16 ERROR_PAY_SESSION_NOT_FOUND = 7070
const i16 ERROR_COLLECTION_NOT_FOUND = 7071
const i16 ERROR_OPERATION_FAILED = 7072
const i16 ERROR_OBJECT_ALREADY_EXISTS = 7073
const i16 ERROR_DOCUMENT_NOT_FOUND = 7074
//order log code
const string CREATE_CODE = "1"
const string CONFIRMED_CODE = "2"
const string CANCELLED_CODE = "3"
const string SHIPPING_CODE = "4"
const string ARRIVED_CODE = "5"
const string DISPATCH_CODE = "6"
const string COMPLETED_CODE = "7"
const string REJECTED_CODE = "8"
const string OVERSEA_TRANSPORT_CODE = "9"
const string RECEIPT_IN_DOMESTIC_TRANSFER = "10"
const string PRINT_IN_DOMESTIC_TRANSFER = "11"
// Language code
const string ENGLISH = "en"
const string CHINESE = "zh-CN"
const map<i16, string> REGION_LANGUAGE_CODE = {1: "en", 2: "zh-CN", 3: "en", 4: "en", 5: "jp"}

// code head
const string ORDER_BATCH_CODE = "A1"
const string ORDER_BILL_CODE = "B1"
const string PAY_BILL_CODE = "C1"
const string SALE_ORDER_CODE = "D1"
const string SHIP_ORDER_CODE = "E1"
const string SHIP_PACKAGE_CODE = "F1"
const string PURCHASE_ORDER_CODE = "G1"
const string SHORTAGE_ORDER_CODE = "H1"

// ids or document name
const string BILL = "Bill"
const string ORDER_BATCH = "OrderBatch"
const string SALE_ORDER = "SaleOrder"
const string SALE_ORDER_DETAIL = "SaleOrderDetail"
const string SHIP_ORDER = "ShipOrder"
const string SHIP_ORDER_DETAIL = "ShipOrderDetail"
const string SHIP_PACKAGE = "ShipPackage"
const string PAY_BILL = "PayBill"
const string PAY_BILL_DETAIL = "PayBillDetail"
const string PRE_ORDER = "PreOrder"
const string SHORTAGE_ORDER = "ShortageOrder"
const string SHORTAGE_ORDER_DETAIL = "ShortageOrderDetail"

// mongodb related
const i16 DNA_SERVICE_PORT = 8000
const i16 _MONGO_SELECT_TIMEOUT_MS = 15000

# 拒收件后续操作
enum SubsequentAction {
    UNTREATED = 0,
    INBOUND = 1,
    SECONDARY_DELIVERY = 2,
    MANUAL_HANDING = 3,
    RETURN = 4,
    DESTROY = 5
}

// related sslcommerz params
struct SslParam {
    1: optional i16 emiOption,
    2: optional string cusName,
    3: optional string cusEmail,
    4: optional string cusPhone
}
struct BkashParam {
    1: i64 accountId,
    2: bool isWithAgreement=true,
    3: optional string payerReference, // 不带agreement时,传
    4: optional string customerMsisdn
}

enum GMO_METHOD {
    CREDIT_CARD = 0
}

enum GMO_CARD_METHOD {
    ONE_TIME_PAYMENT = 1, // 一括
    INSTALLMENT = 2, // 分割
    ONE_TIME_BONUS_PAYMENT = 3, // ボーナス一括
    TWO_TIME_BONUS_PAYMENT = 4, // ボーナス分割
    REVO = 5 // リボ
}

struct CreditCardParam {
    1: string cardNo,
    2: string expire,
    3: GMO_CARD_METHOD method,
    4: optional string securityCode,
    5: optional string pin,
    6: optional string payTimes
}

struct GMOParam {
    1: GMO_METHOD gmoMethod,
    2: optional CreditCardParam cardParam
}

const i16 PAY_FEE_DIGITS = 2

enum PaymentGoodsType {
    REAl = 1,
    VIRTUAL = 2
}
struct PaymentGoods {
    1: string goodsName,
    2: string goodsQuantity,
    3: string goodsPrice,
    4: PaymentGoodsType goodsType,
    5: optional string goodsId,
    6: optional string goodsInfo,
    7: optional string goodsUrl
}
struct LipaPayParam {
    1: string expirationTime,
    2: list<PaymentGoods> paymentGoods,
    3: optional string email,
    4: optional string mobile,
    5: optional string sellerId,
    6: optional string sellerAccount,
    7: optional string buyerId,
    8: optional string buyerAccount,
    9: optional string customerIP,
    10: optional string channels,
    11: optional string paymentMethod = "OL", // OF 线下
    12: optional string countryCode,
    13: optional string remark,
    14: optional string customField1,
    15: optional string customField2,
    16: optional string customField3
}

enum PaymentAction {
    LOAD_LINK = 1,
    GENERATE_QR_CODE = 2,
    POST_URL = 3
}

struct PayPostData {
    1: string url,
    2: string signType,
    3: string merchantId,
    4: string notifyUrl,
    5: string returnUrl,
    6: string merchantOrderNo,
    7: double amount,
    8: string expirationTime,
    9: string sourceType,
    10: string currency,
    11: string countryCode,
    12: string version,
    13: string sellerId,
    14: string sellerAccount,
    15: string buyerId,
    16: string buyerAccount,
    17: string customerIP,
    18: string paymentMethod,
    19: bool useInstallment,
    20: string remark,
    21: string email,
    22: string mobile,
    23: string channels,
    24: string p1,
    25: string p2,
    26: string p3
    27: list<PaymentGoods> goods,
    28: string sign,
    29: string paramsStr
}

struct PaymentProduct {
     1: PaymentAction action,
     2: optional string gatewayPageUrl,
     3: optional string qrCode,
     4: optional PayPostData postData
}

struct LipaPaySignature {
    1: string merchantId,
    2: string merchantOrderNo,
    3: string orderId,
    4: string status,
    5: string signType,
    6: string sign,
    7: optional string p1
}

struct SignatureParam {
     1: optional LipaPaySignature lipaPay
}

enum Gateway {
    SSL = 1,
    BKASH = 2,
    VIRTUAL = -1
    KBZ = 3,
    GMO = 4,
    LIPA_PAY = 5
}

const set<i16> CAN_REfUND_GATE_WAYS = [1, 2, 3]

enum ExecuteWay {
    AGREEMENT = 1,
    PAYMENT = 2
}

enum BkashStatus {
    INITIATED = 1,
    COMPLETED = 2,
    CANCELLED = -1
}

struct BkashExecuteResult {
    1: bool isSuccess,
    2: string failReason
}

struct CreateBkashAgreementRes{
    1: string agreementStatus,
    2: optional string bkashURL,
    3: optional string agreementId
}
struct ExecuteBkashRes {
    1: optional string agreementId,
    2: optional string customerMsisdn
}
// platform
const string ANDROID_APP = "Android-App"
const string iOS_APP = "iOS-App"
const string WEB = "Web"
const string MOBILE_WEB = "Mobile-Web"
const string APP_CUBE = "App-Cube"
const map<string, i16> MAP_PLATFORM = {
    "Android-App": 1,
    "iOS-App": 2,
    "Web": 3,
    "Mobile-Web": 4,
    "App-Cube": 5
}
// order notify order_status
const i16 ORDER_STATUS_SO_CREATE = 1
const i16 ORDER_CONFIRM_STATE = 2
const i16 ORDER_SHIPPED_STATE = 3
const i16 ORDER_DISPATCHED_STATE = 4
const i16 ORDER_RECEIVED_STATE = 5
const i16 ORDER_STATUS_BILL_CREATE = 6
const i16 ORDER_STATUS_SO_CANCELLED = -1
const i16 ORDER_REJECTED_STATE = -2
const i16 ORDER_STATUS_BILL_CANCELLED = -3
// rest params
const string TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
const string LOCAL_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
const string _LOG_FILE = "order-service.log"
const i16 REQUESTS_TIMEOUT = 150
const i64 REVIEW_TTL = 2592000000 // unit: millisecond
const i32 TTL = 172800000  // unit: millisecond
const i32 TWO_HOUR_TTL = 7200000  // unit: millisecond
const i32 MINUTE_140_TTL = 8400000
const i32 TWO_DAY_TTL = 172800000
const i32 ONE_DAY_TTL = 86400000  // unit: millisecond
const i32 SEVEN_DAY_TTL = 604800000
const i32 EIGHT_DAY_TTL = 691200000
const i32 HOUR_36_TTL = 129600000
const i16 PAY_TRAN_EXPIRE = 2 // unit: days
const i16 PAY_SESSION_EXPIRE = 10 // unit: minutes
const i16 COUNT_GMV_DAY_LIMIT = 92 // unit: days
const string SECRET_KEY = "jklklsadhfjnhwbii9sdfdf"
const i16 TIMEOUT_ACCESS_TOKEN = 300 // seconds
const i16 TIMEOUT_REFRESH_TOKEN = 25920
//const i32 ONE_DAY_TTL = 120000
//const i32 TTL = 60000
const i16 HOUR_24 = 24
const i16 HOUR_48 = 48
const i16 HOUR_72 = 72
const i16 HOUR_120 = 120

struct CityAndArea {
    1: string city,
    2: string area
}

const map<string, i16> MAP_SESSION_STATUS = {
    "VALID": 2,
    "FAILED": 3,
    "CANCELLED": 4
}

const list<string> REGULAR_SPECIAL_CHARACTERS = ["*", ".", "?", "+", "$", "^",
 "[", "]", "(", ")","{", "}", "|", "/", "\\\\"]

const map<string, CityAndArea> MAP_ECOURIER_ADDRESS = {
  "1": {"city": "Dhaka", "area": "Azimpur"},
  "2": {"city": "Dhaka", "area": "Motijheel"}
}
const map<string, list<string>> ECOURIER_CITY_AND_AREA = {
  "Habiganj": ["Habiganj Sadar", "Nobiganj"]
  "Narsingdi": ["Narsingdi Sadar", "Palash"]
}

struct ShortageOrderDetail {
    1: required i64 shortageOrderDetailId,
    2: required i64 shortageOrderId,
    3: required i64 saleOrderDetailId,
    4: required i64 skuId,
    5: required i64 salePrice,
    6: required i64 dealPrice,
    7: required i32 discount,
    8: required i32 priceRevision,
    9: required i16 count,
    10: required i16 redeem,
    11: required i32 coin,
    12: required i16 voucherRedeem,
    13: required i32 warehouseId,
    14: required string createdAt
}
enum ShortageStatus {
    not_created = 1,
    pending_refund = 2,
    refunding = 3,
    complete = 4
}
// (1: 未创建，2: 待退款，3: 退款中，4: 退款已完成)
struct ShortageOrder{
    1: required i64 shortageOrderId,
    2: required string shortageOrderCode,
    3: required i64 accountId,
    4: required i64 saleOrderId,
    5: required i16 region,
    6: required i64 shipOrderId,
    7: required PaymentMethods paymethod,
    8: required i32 storeId,
    9: required bool isRefunded,
    10: required i32 itemTotal,
    11: required i64 billId,
    12: required i16 redeem,
    13: required i16 coin,
    14: required i16 voucherRedeem,
    15: required i16 discount,
    16: required i32 payAmount,
    17: required i32 amountPaid,
    18: required string createdAt,
    19: required ShortageStatus status,
    20: optional string refundedAt,
    21: required i32 staffId
}

struct ShortageOrderRelated {
    1: required ShortageOrder shortageOrder,
    2: required string saleOrderCode,
    3: required i16 saleOrderPayStatus
}

struct ShortageOrders {
    1: required i64 count,
    2: required list<ShortageOrderRelated> shortageOrders
}

struct SkuHistoryPriceRelated {
    1: required i64 price,
    2: required string createdAt,
    3: required i16 orderType
}
struct SkuActivity {
    1: i64 skuId,
    2: i16 activityType,
    3: i64 activityId
}
struct ActivitySkuCount {
    1: i64 skuId,
    2: i16 activityType,
    3: i64 activityId,
    4: i32 skuCount,
    5: i32 activityCount
}
struct OrderPromotionDetail {
    1: required i64 id,
    2: required i16 activityType,
    3: required i32 activityId,
    4: required i64 billId,
    5: required i64 saleOrderId,
    6: required i64 saleOrderDetailId,
    7: required i64 skuId,
    8: required i32 storeId,
    9: required i16 count,
    10: required i16 discount,
    11: required i64 accountId,
    12: required i16 region,
    13: required i64 salePrice,
    14: required i64 dealPrice,
    15: required i32 priceRevision,
    16: required string createdAt
}

enum china_express {
    ZTO = 1,
    YTO = 2,
    STO = 3,
    YUNDA = 4,
    BEST = 5,
    RR = 6,
    SF = 7,
    JD = 8,
    OTHER = 0
}

const map<i16, string> CHINA_EXPRESS_MAY = {1: "中通", 2: "圆通", 3: "申通",
4: "韵达", 5: "百世", 6: "人人", 7: "顺丰", 8: "京东", 0: "其他"}

struct SaleOrderSku {
    1: optional i64 saleOrderDetailId,
    2: optional i64 skuId,
    3: optional i64 saleOrderId,
    4: optional i64 storeId,
    5: optional i32 warehouseId,
    6: optional i32 count,
    7: optional string createdAt,
    8: optional i64 activityId,
    9: optional i64 activityType,
    10: optional bool ofsManageWarehouse
}

struct SaleOrderSkuList {
    1: required i64 count,
    2: required list<SaleOrderSku> saleOrderSkus
}

struct Sku {
    1: required i64 skuId,
    2: required i32 count,
    3: required ShipOrderStatus state
}

enum OrderOperateCode{
    place = 1,
    pay = 2,
    confirm = 3,
    dispatch = 4,
    arriveTransCenter = 5,
    clearance = 6,
    arriveDhaka = 7,
    packaged = 8,
    delivery = 9,
    received = 10,
    close = 11,
    cancel = 12,
    rejected = 13
}
const set<i16> so_op_li = [2, 12]
const set<i16> pg_op_li = [4, 5, 6, 7, 8, 9, 10, 11, 13]
enum OrderOperator {
    customer = 1,
    seller = 2,
    admin = 3,
    logistic = 4,
    system = 5
}
struct OrderOperateLog {
    1: required OrderOperateCode operateCode,
    2: required OrderOperator operator,
    3: required i64 operatorId,
    4: required string createdAt
}

struct ConfirmOrderRes {
    1: required i64 packageId,
    2: required i16 regionId,
    3: required i64 addressId,
    4: required i64 accountId,
    5: required i64 saleOrderId,
    6: required string saleOrderCode,
    7: required i64 storeId,
    8: required i32 itemCount,
    9: required string soCreatedAt,
    10: required string confirmedAt
}

struct SimpleSo {
    1: optional i64 saleOrderId,
    2: optional string code,
    3: optional i16 status,
    4: optional SaleOrderStatus oldState,
    5: optional i32 coin,
    6: optional list<SaleOrderSku> skus,
    7: optional i32 storeId
}
struct CancelSosReturn {
    1: optional bool isRefundVoucher,
    2: optional list<i64> voucherIds,
    3: list<SimpleSo> sos
}
struct SoCount {
    1: i32 completeCount,
    2: i32 rejectCount,
    3: i32 inProcessing
}

enum IsWithBattery {
    no = 0,
    yes = 1,
    partially = 2
}
struct OneSku {
     1: i64 skuId,
     2: i16 count,
     3: i64 dealPrice
}

struct OnePackage {
    1: i64 packageId,
    2: i64 accountId,
    3: string packageCode,
    4: i64 addressId,
    5: i16 region,
    6: i32 codAmount,
    7: i32 onlineAmount,
    8: PackageStatus status,
    9: string createdAt,
    10: optional i64 saleOrderId,
    11: optional i32 storeId,
    12: optional PaymentMethods payMethod,
    13: optional i64 warehouseId,
    14: optional i16 skuCount,
    15: required i16 itemCount,
    16: optional i16 deliveryId,
    17: optional string deliveryCode,
    18: optional i16 terminalDeliveryId,
    19: optional string terminalDeliveryCode,
    20: optional i16 shoCount,
    21: optional string earlyShoCreatedAt,
    22: optional string shippedAt,
    23: optional string dispatchedAt,
    24: optional string deliveredAt,
    25: optional string closedAt,
    26: optional list<OneSku> skus,
    27: optional i16 discount,
    28: optional i16 coinRedeem,
    29: optional i16 coin,
    30: optional i16 postage,
    31: optional i16 voucherRedeem,
    32: optional i16 vat,
    33: optional i64 voucherId,
    34: optional DeliveryMethod deliveryMethod,
    35: optional i64 payAmount
    36: optional bool ofsManageWarehouse
}
struct PackagesRes {
    1: optional i64 packageCount,
    2: list<OnePackage> packages
}
struct SaleOrderDetail {
    1: i64 id,
    2: i64 orderId,
    3: i64 skuId,
    4: i32 count,
    5: i64 salePrice,
    6: i64 dealPrice,
    7: i32 priceRevision,
    8: i32 coinRedeem,
    9: i32 coin,
    10: i32 voucherRedeem,
    11: i32 discount,
    12: i32 vat,
    13: i32 amount,
    14: i16 status,
    15: i32 warehouseId,
    16: string createdAt,
    17: optional i64 listingId,
    18: optional string foreignName,
    19: optional string chineseName,
    20: optional bool ofsManageWarehouse
}
struct SaleOrder{
    1: i64 id,
    2: SaleOrderStatus status,
    3: string code,
    4: i16 region,
    5: i64 billId,
    6: i64 batchId,
    7: i32 storeId,
    8: i64 accountId,
    9: i64 addressId,
    10: i32 warehouseId,
    11: i16 postage,
    12: i16 postageDiscount,
    13: i16 postageRedeem,
    14: i32 orderAmount,
    15: i32 itemTotal,
    16: i32 redeem,
    17: i32 coin,
    18: i32 voucherRedeem,
    19: i32 payAmount,
    20: i32 discount,
    21: i32 vat,
    22: i32 itemCount,
    23: i32 skuCount,
    24: i16 deliveryPeriod,
    25: PaymentMethods payMethod,
    26: i16 platform,
    27: string createdAt,
    28: optional string remark,
    29: optional SoType orderType,
    30: optional IsWithBattery withBattery,
    31: optional bool isMagnetic,
    32: optional bool isPowder,
    33: optional bool isCompressor,
    34: optional string paidAt,
    35: optional string confirmAt,
    36: optional string shippedAt,
    37: optional string closedAt,
    38: optional bool userConfirmed,
    39: optional string userConfirmedAt,
    40: optional string remarkUpdatedAt,
    41: optional i32 paidAmount,
    42: optional bool liquid,
    43: optional i32 preAmount,
    44: optional i32 dueAmount
    45: optional bool ofsManageWarehouse
}
struct OrderRelated {
   1: SaleOrder saleOrder,
   2: list<SaleOrderDetail> orderDetail
}
struct OrderList {
    1: i32 count,
    2: list<OrderRelated> orderRelated
}
struct OrderInfo {
    1: i64 saleOrderId,
    2: i64 shipOrderId,
    3: i64 packageId,
    4: string packageCode,
    5: string saleOrderCode
}
struct SimpleSoRelated {
    1: i64 soId,
    2: i32 orderAmount,
    3: string packageCode
}
struct PackageRelated {
    1: i64 packageId,
    2: i32 storeId,
    3: i32 warehouseId
    4: bool ofsManageWarehouse
}
struct IsUseCod {
    1: bool isUseCod,
    2: optional string reason
}
struct OrderCount {
    1: i32 submitted,
    2: i32 pendingConfirm,
    3: i32 pendingDispatch,
    4: i32 inTransit,
    5: i32 completed,
    6: i32 rejected,
    7: i32 cancelled
}
struct GMV {
    1: i32 submitted,
    2: i32 inTransit,
    3: i32 completed,
    4: i32 rejected,
    5: i32 cancelled
}
struct CountAndGMV {
    1: OrderCount orderCount,
    2: GMV gmv
}
struct OrderPlatform {
    1: PromotionPlatform platform,
    2: set<i64> saleOrderIds
}

struct AccountOrder {
    1: i64 accountId,
    2: i32 codCount,
    3: i32 batchCount,
    4: i32 orderCount,
    5: i32 completeCount,
    6: i32 codProcessCount,
    7: i32 cancelCount,
    8: i32 rejectCount,
    9: i64 completeAmount
    10: i32 onlineCount
}

struct EcourierPartner{
    1: i32 epId,
    2: optional string epName,
    3: optional string contactPerson,
    4: optional string division,
    5: string district,
    6: string thana,
    7: string pickUnion,
    8: string address,
    9: string mobile,
    10: i32 branchId
}

struct EcourierRecipient {
    1: string name,
    2: string mobile,
    3: optional string division,
    4: optional string district,
    5: string city,
    6: optional string area,
    7: string thana,
    8: string recipientUnion,
    9: optional string upazila,
    10: string address
}

struct ECourierBranch {
    1: i32 branchId,
    2: string branchName
}

struct ShipOrderDetail{
    1: required i64 id,
    2: required i64 shipOrderId,
    3: required i64 saleOrderDetailId,
    4: required i64 skuId,
    5: required i64 salePrice,
    6: required i64 dealPrice,
    7: required i16 collected,
    8: required i16 count,
    9: optional i32 warehouseId,
    10: optional i32 activityType,
    11: optional i32 activityId,
    12: optional i32 discount
    13: optional bool ofsManageWarehouse
}

struct OrderPackege {
    1: SaleOrder saleOrder,
    2: OnePackage shipPackage,
    3: list<SaleOrderDetail> skus,
    4: list<ShipOrderDetail> spds,
    5: optional string afterSaleCompletedAt
}

enum ReturnReason {
    reject = 1,    //拒收
    refund = 2     //退货
}

enum IncreaseStockResult {
    success = 1,    //拒收
    failed = 0     //退货
}

enum IncreaseStockFailedReason {
    NoDeriveSku = 1,    //中国发货商品，不存在派生sku，请先创建派生sku，不能入库
    NotStorageWH = 2,     //第三方卖家非备货仓商品，不能入库
    UnsuportedOP = 3      //不支持入库操作的商品，不能入库
}

enum VoucherOwner {
    PLATFORM = 1,
    STORE = 2
}

struct ClearingStatistic {
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
    22: i32 storeId,
    23: Courier terminalDeliveryId,
    24: DeliveryMethod deliveryMethod
    25: optional bool ofsManageWarehouse
}

struct ClearingStatisticList {
    1: i32 count,
    2: list<ClearingStatistic> clearingStatistics
}

struct SummaryOrderStatistics {
    1: i64 itemTotal,
    2: i64 totalPostage,
    3: i64 payAmount,
    4: i64 coinRedeem,
    5: i64 platVoucher,
    6: i64 storeVoucher,
    7: double payFee,
    8: i64 commission,
    9: i64 storePostage,
    10: i64 platePostage,
    11: i64 settlementCoinRedeem,
    12: i64 settlementPlatVoucher,
    13: i64 settlementStoreVoucher,
    14: map<i16, i32> warehouseOrderCount,
    15: map<string, i32> deliveryStatistics  // {"selfDelivery": 0, "platDelivery": 0}
    16: i64 selfDeliveryCODAmount,
    17: i64 selfDeliveryCODPostage
}

struct ActivityIdCount {
    1: i64 activityId,
    2: i32 soldCount
}
struct MiniSaleOrder {
    1: required i64 id,
    2: required i16 storeId,
    3: required string code,
    4: optional i16 status,
    5: optional string createdAt,
    6: optional i64 accountId,
    7: optional list<OneSku> items
}

struct MiniSaleOrders {
    1: optional i64 total,
    2: optional list<MiniSaleOrder> miniSaleOrders
}

struct MiniShipOrder {
    1: required i64 id,
    2: required i64 saleOrderId,
    3: required i16 storeId,
    4: required string code,
    5: optional i16 status,
    6: optional string createdAt,
    7: optional i64 accountId,
    8: optional list<OneSku> items
}

struct MiniShipOrders {
    1: optional i64 total,
    2: optional list<MiniShipOrder> miniShipOrders
}

enum ExFcsType {
    PLATFORM_CHINA = 1,
    PLATFORM_MM = 2,
    STORE = 3
}

struct ExFcsParameter {
    1: string fromUser,
    2: i64 fromCityId,
    3: string fromAddress,
    4: string fromMobile,
    5: string toUser,
    6: i64 toCityId,
    7: string toAddress,
    8: string toMobile,
    9: string itemDesc,
    10: double itemWeight,
    11: optional string fromEmail,
    12: optional string toEmail,
    13: optional i16 currencyId,
    14: optional bool insured,
    15: optional i64 insuredPrice,
    16: optional i16 payType,
    17: optional i16 payment,
    18: optional bool cod,
    19: optional i64 codAmount,
    20: optional string remark,
    21: optional ExFcsType accountType,
    22: optional i32 storeId
}

struct SagawaSku {
    1: string skuId,
    2: string itemName,
    3: string piece,
    4: string origin,
    5: string unitprice
}

struct SagawaParameter {
    1: string referenceNo,
    2: string shipDate, // YYYY/MM/DD
    3: string consigneeKana1,
    4: string consigneePostalCode,
    5: string address1, // 三级地址
    6: string address2, // 详细地址
    7: string phoneNumber,
    8: string itemTotal,
    9: string totalAmount, // 总金额
    10: string codCharge, // 货到付款费用
    11: string codFlg, // 0：Prepaid, 1：Collect
    12: list<SagawaSku> sagawaSkus,
    13: optional string weight,
    14: optional string appointedDeliveryDate, // YYYYMMDD
    15: optional string appointTimePeriod, // HHMM
    16: optional string trackingNo,
    17: optional string remark,
    18: optional string freight,
    19: string controlCode
}

struct MappingAddress{
    1: i16 regionId,
    2: i32 stateId,
    3: i32 cityId,
    4: i32 pfCityId,
    5: string stateName,
    6: string cityName
}

struct LogisticsSheet{
    1: string url,
    2: Courier deliveryId
}

enum QueryPackageSource{
    SO_ID = 1,
    PACKAGE_ID = 2,
    LOGISTICS_CODE = 3
}

struct SagawaLabel {
    1: string refNo,
    2: string routingCode1,
    3: string routingCode2,
    4: string routingBarCode,
    5: string trackingBarCode,
    6: string trackingNumber,
    7: string codYesNo,
    8: string shipDate,
}

enum SagawaSchType {
    HAWB = 1,
    REF = 2,
    WAYBILL_NO = 3
}

struct XedAddress {
    1: required string contact,
    2: required string intlTelCode,
    3: required string phoneNumber,
    4: required string country,
    5: required string city,
    6: required string detail,
}

struct XedUser {
    1: i64 id,
    2: string account,
    3: string name,
    4: string intlTelCode,
    5: string phoneNumber,
    6: string key,
    7: list<string> userTypes,
}

struct XedStore {
    1: i64 id,
    2: i64 userId,
    3: i64 userTypeId,
    4: string platformStoreId,
    5: string platformStoreName,
    6: i64 xedShippingAddressId
}

struct XedOrder {
    1: i32 saleOrderId,
    2: i32 packageId,
    3: i32 xedState,
    4: bool isReachTransitWarehouse
}

struct WmsAccount {
    1: i32 id,
    2: string name,
}

struct WmsStore {
    1: i64 id,
    2: string platformName,
    3: string storeName,
    4: string createdAt,
}

struct PagingWmsStore {
    1: i32 total,
    2: list<WmsStore> stores,
}

struct WmsWarehouse {
    1: i64 id
    2: string serialNumber
    3: string name
    4: string region
    5: string city
    6: i64 state
    7: i64 applyState
    8: string applyAt
    9: string passAt
}

struct PagingWmsWarehouse{
    1: i32 total,
    2: list<WmsWarehouse> warehouses,
}

struct WmsWarehouseApplication{
    1: i64 id
    2: string serialNumber
    3: string name
    4: i64 state
    5: string applyAt
    6: string auditedAt
}

struct PagingWmsWarehouseApplication{
    1: i32 total,
    2: list<WmsWarehouseApplication> warehouseApplications,
}

enum WarehousingOrderStatus {
    NOT_IN_STOREAGE = 1,
    STOREAGE = 2
}

enum StorageType {
    STOCK = 1,
    RETURN = 2,
    NO = -1
}

enum StorageSourceType {
    REJECT = 1,
    AFTERSALE = 2
}

struct WarehousingSku {
    1: i64 saleOrderDetailId,
    2: i64 skuId,
    3: i32 storageCount,
    4: i64 saleOrderId,
    5: optional i64 deriveSkuId,
    6: optional i64 sourceSkuId,
    7: optional StorageType storageType
}

struct WarehousingOrder {
    1: i64 id,
    2: i64 packageId,
    3: i64 saleOrderId,
    4: i32 accountId,
    5: i32 warehouseId,
    6: i32 storeId,
    7: string packageCreatedAt,
    8: string createdAt,
    9: WarehousingOrderStatus status,
    10: StorageType storageType,
    11: optional StorageSourceType sourceType,
    12: optional string storageAt,
    13: optional i32 operatorId,
    14: optional string packageCode,
    15: optional i64 addressId,
    16: optional DeliveryMethod deliveryMethod,
    17: optional string terminalDeliveryCode
}

struct WarehousingOrders {
    1: i32 count,
    2: list<WarehousingOrder> warehousingOrder
}

enum WarehousingOrdersTimeType {
    REJECT_TIME = 1,
    PACKAGE_CREATED_TIME = 2
}

enum SwitchState {
    ENABLE = 1,
    DISABLE = -1
}

enum PrepaymentPostageType {
    FIRST_PAY = 1,
    FINAL_PAY = 2
}

struct PrepaymentSetting {
    1: bool enable,
    2: double prepaymentRatio,
    3: PrepaymentPostageType postageType
}

const string PARAM_MODULE_PREPAYMENT = "prepayment"
const string PARAM_NAME_PREPAYMENT_SWITCH = "PREPAYMENT_SWITCH"
const string PARAM_NAME_PREPAYMENT_RATIO = "PREPAYMENT_RATIO"
const string PARAM_NAME_PREPAYMENT_POSTAGE_TYPE = "PREPAYMENT_POSTAGE_TYPE"

const map<string, map<string, string>> SAGAWA_CODE_MAP =
{
    "TF": {
        "en": "Translation Finished",
        "jp": "翻訳完了"
    },
    "CB": {
        "en": "Consol Break",
        "jp": "解体完了"
    },
    "CS": {
        "en": "Clearance Start",
        "jp": "通関開始"
    },
    "LC": {
        "en": "Local Comment",
        "jp": "カスタマーサービス対応しました。"
    },
    "DR": {
        "en": "Document Returned",
        "jp": "書類返却"
    },
    "DP": {
        "en": "Document PickUp",
        "jp": "書類受け取り"
    },
    "EM": {
        "en": "EMAIL",
        "jp": "EMAIL"
    },
    "PU": {
        "en": "Picked Up By Local Carrier",
        "jp": "集荷済み"
    },
    "TA": {
        "en": "Preparing for dispatch",
        "jp": "出荷準備中"
    },
    "TD": {
        "en": "Departed From Transit Point",
        "jp": "経由地を出発"
    },
    "OB": {
        "en": "On Board Aircraft",
        "jp": "現地へ輸送中"
    },
    "IA": {
        "en": "Arrived at international transit point",
        "jp": "経由地に到着"
    },
    "FD": {
        "en": "FLIGHT DELAY",
        "jp": "到着遅延"
    },
    "ID": {
        "en": "Departed from international transit point.",
        "jp": "経由地を出発"
    },
    "EA": {
        "en": "Estimated Arrival date at airport",
        "jp": "フライト到着予定日"
    },
    "NA": {
        "en": "NOT ARRIVED AT THE DESTINATION",
        "jp": "貨物未到着"
    },
    "IB": {
        "en": "Arrived At Destination",
        "jp": "現地に到着/通関中"
    },
    "EX": {
        "en": "Awaiting Customs Clearance",
        "jp": "通関手続き中"
    },
    "FC": {
        "en": "Formal customs clearance is under process",
        "jp": "通関手続き中"
    },
    "CU": {
        "en": "CUSTOMS INSPECTION",
        "jp": "税関審査中"
    },
    "AD": {
        "en": "AWAITING DOCUMENT",
        "jp": "通関書類待ち"
    },
    "CL": {
        "en": "COMPANY CLOSED",
        "jp": "定休日"
    },
    "N6": {
        "en": "No or  Incorrect Pin number",
        "jp": "荷受人認証番号確認中"
    },
    "CD": {
        "en": "CLEARANCE DELAY",
        "jp": "通関遅延"
    },
    "CP": {
        "en": "Shipment cannnot be procesed",
        "jp": "通関保留"
    },
    "CX": {
        "en": "Customs detained",
        "jp": "通関保留"
    },
    "PD": {
        "en": "Pending",
        "jp": "出荷保留"
    },
    "CR": {
        "en": "CLEARANCE RELEASE",
        "jp": "通関許可"
    },
    "BD": {
        "en": "Out For Delivery",
        "jp": "お荷物を発送しました"
    },
    "BN": {
        "en": "Broker Notified",
        "jp": "通関業者への引渡し完了"
    },
    "TR": {
        "en": "TRANSFER",
        "jp": "転送中"
    },
    "CN": {
        "en": "Scheduled for Customs Inspection",
        "jp": "税関検査中"
    },
    "EP": {
        "en": "Entrusted to Postal Service",
        "jp": "郵便へ引渡し済"
    },
    "CE": {
        "en": "Collected by Sagawa Express",
        "jp": "佐川急便集荷店　集荷"
    },
    "UN": {
        "en": "Unloading",
        "jp": "到着降"
    },
    "LO": {
        "en": "Loading",
        "jp": "積込"
    },
    "DD": {
        "en": "Dispatch from delivery branch",
        "jp": "佐川急便配達店　持出"
    },
    "DL": {
        "en": "Delivering",
        "jp": "配送中"
    },
    "SL": {
        "en": "Scheduled For Delivery",
        "jp": "荷受人指定日にて再配達手配済み"
    },
    "DS": {
        "en": "Disposed",
        "jp": "廃棄した"
    },
    "SD": {
        "en": "Shipment Damaged",
        "jp": "破損・汚損"
    },
    "AB": {
        "en": "ABSENCE",
        "jp": "不在"
    },
    "RD": {
        "en": "Re-delivery",
        "jp": "再配達中"
    },
    "ND": {
        "en": "Delivery imcomplete. Unable to contact Receiver",
        "jp": "配達先が不在の為、配達保留"
    },
    "PS": {
        "en": "Please contact SGH Global Japan.",
        "jp": "到着状況については営業店へお問い合わせください"
    },
    "BA": {
        "en": "INCORRECT ADDRESS",
        "jp": "住所不明"
    },
    "HP": {
        "en": "HELD FOR PAYMENT",
        "jp": "支払い確認待ち"
    },
    "RF": {
        "en": "REFUSED DELIVERY",
        "jp": "受取拒否"
    },
    "LD": {
        "en": "Delivered",
        "jp": "配達完了"
    },
    "CO": {
        "en": "Please contact SGH Global Japan.",
        "jp": "貨物の配達状況についてお問い合わせ下さい"
    },
    "CV": {
        "en": "COVID-19",
        "jp": "COVID-19"
    },
    "UD": {
        "en": "Undeliverable",
        "jp": "配達不能"
    }
}
