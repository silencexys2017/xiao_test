enum AddressType {
    NORMAL = 1,
    PICKUP = 2
}

struct AreaIdName {
    1: i64 id,
    2: string name
}

enum AddressStatus {
    AVAILABLE = 1,
    UNAVAILABLE = 2
}

struct Address {
	1: i64 id,
	2: i64 accountId,
	3: i32 regionId,
	4: string regionCode,
	5: string name,
	6: map<string, AreaIdName> areaNames,
	7: string address1,
	8: string address2,
	9: string pickupStationAddress,
	10: AddressType addressType,
	11: string phone,
	12: bool verified,
	13: bool isDefault,
	14: optional bool deleted,
	15: optional i64 pickupStationId,
	16: optional bool isDraw,
	17: optional string postcode,
	18: optional bool isSelected,
	19: optional string familyName,
	20: optional string givenName,
	21: optional i16 areaLevel,
    22: optional bool isSupportToDoor,
    23: optional list<AreaIdName> areaNameList,
    24: optional AddressStatus status
}
enum DeliveryType {
    INTERNATIONAL = 1,
    LOCAL = 2,
}

enum BillType {
    NORMAL = 1,
    COMPLEX = 2
}

enum AvailablePayment {
    YES = 1,
    PART = 2,
    NO = 3
}

enum PayMethod {
    ALL = 1,
    PRE = 2,
    MIX = 3
}

enum PayType {
    ONLINE = 1
    COD = 2
}

const map<i16, string> PAY_TYPE_MAP = {1: "Online", 2: "COD"}

struct CurrencyAmount {
    1: double defaults,
    2: double display
}

enum BillState {
    NEW_CREATE = 1,
    VALID = 2,
    INVALID = -1
}

enum PayState {
    PENDING_PAY = 1,
    PART_PAID = 2,
    PAID = 3
}

const list<i16> PAID_STATUS = [2,3]

enum GatewayStatus {
    ENABLE = 1,
    DISABLE = -1
}

struct PartnerProduct {
    1: string skuId,
    2: i64 uomnifySkuId,
    3: string spec,
    4: i32 count,
    5: string title,
    6: list<string> images,
    7: double salePrice,
    8: map<string, AreaIdName> mapStr
}

struct PartnerOrder {
    1: optional string orderId,
    2: optional string orderNo,
    3: optional string regionCode,
    4: optional PayMethod payMethod,
    5: optional string currency,
    6: optional double codAmount,
    7: optional double preAmount,
    8: optional double payAmount,
    9: optional double itemTotal,
    10: optional string storeId,
    11: optional list<PartnerProduct> products,
    12: optional string createdTime
}

struct Bill {
    1: i32 id,
    2: string regionCode,
    3: BillType type,
    4: list<i32> complexIds,
    5: i32 accountId,
    6: i32 addressId,
    7: PayMethod payMethod,
    8: list<PayType> payTypes,
    9: string displayCurrency,
    10: string defaultCurrency,
    11: double exchangeRate,
    12: double taxRate,
    13: CurrencyAmount vat,
    14: CurrencyAmount itemTotal,
    15: CurrencyAmount discount,
    16: CurrencyAmount redeem,
    17: CurrencyAmount postage,
    18: CurrencyAmount postageDiscount,
    19: CurrencyAmount orderAmount,
    20: CurrencyAmount payAmount,
    21: CurrencyAmount collectedAmount,
    22: CurrencyAmount preAmount,
    23: CurrencyAmount dueAmount,
    24: double prepaymentRatio,
    25: BillState state,
    26: PayState payState,
    27: string createdTime,
    28: string expiredTime,
    29: string lastUpdatedTime,
    30: string code,
    31: optional list<SaleOrder> saleOrders,
    32: optional list<OrderDetail> orderDetails,
    33: optional i32 skuCount,
    34: optional i32 itemCount,
    35: optional i32 orderCount,
    36: optional OrderType orderType,
    37: optional i32 thirdPlatformId,
    38: optional i32 thirdStoreId,
    39: optional PartnerOrder thirdOrder
}

const i16 PAY_TRANSACTION_DEADLINE = 2880 // minute
const i16 PAY_SESSION_DEADLINE = 10 // minute

enum PayChannel {
    COD = -1,
    SSLCommerz = 1,
    KBZPay = 2,
    payStack = 3,
    lipaPay = 5,
    bKash = 6,
    PayPal = 7
}

enum PayTypeReason {
    CLOSED = 1
}

const i16 SSLCOMMERZ_EMI_ENABLE = 1
const i16 SSLCOMMERZ_EMI_DISABLE = 0

struct SslcommerzParam {
    1: optional i16 emiOption,
    2: optional string cusName,
    3: optional string cusEmail,
    4: optional string cusPhone
}

struct BkashParam {
    1: bool isWithAgreement=true,
    2: optional string payerReference
}

struct PayPalParam {

}

struct PayStackParam {
    1: string mailbox
}

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
    11: optional string paymentMethod = "OL",
    12: optional string countryCode,
    13: optional string remark,
    14: optional string customField1,
    15: optional string customField2,
    16: optional string customField3
}

struct ChannelParam {
    1: optional SslcommerzParam sslcommerzParam,
    2: optional PayStackParam payStackParam,
    4: optional LipaPayParam lipaPayParam,
    5: optional BkashParam bkashParam,
    6: optional PayPalParam payPalParam
}

enum PayBillState {
    PENDING_PAY = 1,
    IN_PAYING = 2,
    PAID = 3
}

enum RefundState {
    PENDING_REFUND,
    PARD_REFUNDED,
    REFUNDED
}

struct PayBill {
    1: i32 id,
    2: string code,
    3: i32 billId,
    4: i32 accountId,
    5: PayMethod payMethod,
    6: PayType payType,
    7: PayChannel lastPayChannel,
    8: PayBillState state,
    9: string displayCurrency,
    10: string defaultCurrency,
    11: CurrencyAmount payAmount,
    12: CurrencyAmount collectedAmount,
    13: string createdTime,
    14: string lastInitiatedTime,
    15: string lastUpdatedTime,
    16: string closedTime,
    17: string expiredTime
}

enum PayTransactionState {
    PENDING_PAY = 1,
    PAID = 2
}

struct PayTransaction {
    1: i32 id,
    2: PayChannel payChannel,
    3: PayTransactionState state,
    4: i32 billId,
    5: i32 payBillId,
    6: i32 accountId,
    7: string currency,
    8: double payAmount,
    9: bool isValidated,
    10: string createdTime,
    11: string expiredTime,
    12: string paidTime,
    13: string lastUpdatedTime,
    14: string successResponse,
    15: RefundState refundState,
    16: double refundAmount,
    17: list<string> refunds,
    18: string tran_code
}

enum PaySessionState {
    PENDING_PAY = 1,
    PAID = 2,
    CANCEL = -1,
    FAILED = -2,
    UNKNOWN = -3
}

struct PaySession {
    1: i32 id,
    2: i32 tranId,
    3: i32 billId,
    4: i32 payBillId,
    5: PayChannel payChannel,
    6: PaySessionState state,
    7: string sourceFrom,
    8: bool isValidated,
    9: string createdTime,
    10: string expiredTime,
    11: string closedTime,
    12: string responseData,
    13: optional string tranCode
}

enum SaleOrderState{
    PENDING_PAY = 1,
    PENDING_SHIP = 2,
    IN_TRANSIT = 3,
    IN_DELIVERING = 4,
    DELIVERED = 5,
    COMPLETED = 6,
    CANCEL = -1,
    REJECT = -2
}

const list<i16> SO_CAN_BE_CANCELLED_STATUS = [1, 2]
const list<i16> SO_CAN_BE_CLOSED_STATUS = [3, 4, 5]

enum PromotionType {
    NORMAL = -1,
}

enum OrderType {
    NORMAL = 1,
    E_COMMERCE = 2,
    E_COMMERCE_DROP_SHIP = 3
}

enum FulFillType {
    SHIP = 1,
    DROP_SHIP = 2
}

enum OrderFrom {
    NORMAL = 1,
    E_COMMERCE = 2
}

struct OrderDetail {
    1: i32 id,
    2: string regionCode,
    3: i32 accountId,
    4: i32 saleOrderId,
    5: SaleOrderState state,
    6: i32 vendorId,
    7: i32 warehouseId,
    8: bool withMagnetism,
    9: bool withPowder,
    10: bool withLiquid,
    11: bool withCompressor,
    12: bool withBattery,
    13: i64 listingId,
    14: i64 skuId,
    15: i32 itemCount,
    16: string displayCurrency,
    17: string defaultCurrency,
    18: i32 promotionType,
    19: i32 promotionId,
    20: CurrencyAmount salePrice,
    21: CurrencyAmount originalPrice,
    22: CurrencyAmount amount,
    23: CurrencyAmount discount,
    24: CurrencyAmount redeem,
    25: CurrencyAmount vat,
    26: CurrencyAmount postage,
    27: CurrencyAmount postageDiscount,
    28: CurrencyAmount preAmount,
    29: CurrencyAmount dueAmount,
    30: double prepaymentRatio,
    31: string createdTime,
    32: string lastUpdatedTime,
    33: i32 billId
}

struct CancelInfo {
    1: i16 reason,
    2: string reasonDetail
}

enum LogisticsProvider {
    XED = 1
}

struct Package {
    1: optional string domesticLogistics,
    2: optional string domesticNo,
    3: optional RejectReason rejectReason,
    4: optional LogisticsProvider logisticsId,
    5: optional string logisticsNo,
    6: optional string logisticsCreatedTime,
    7: optional string localLogistics,
    8: optional string localNo
}

struct PartnerUser {
    1: optional string userId,
    2: optional string name,
    3: optional string phoneNumber,
    4: optional string mailbox
}

struct ThirdDeliveryAddress {
    1: optional string familyName,
    2: optional string givenName,
    3: optional string address,
    4: optional string address2,
    5: optional string postCode,
    6: optional string regionCode,
    7: optional string state,
    8: optional string city,
    9: optional string area,
    11: optional string receiver,
    12: optional string phone,
    13: optional i32 areaId,
    14: optional i32 cityId,
    15: optional i32 stateId
}

struct SaleOrder {
    1: i32 id,
    2: string code,
    3: string regionCode,
    4: i32 accountId,
    5: i32 billId,
    6: SaleOrderState state,
    7: string sourceFrom,
    8: PayMethod payMethod,
    9: list<PayType> payTypes,
    10: string displayCurrency,
    11: string defaultCurrency,
    12: list<i32> vendorIds,
    13: i32 warehouseId,
    14: i32 addressId,
    15: bool withMagnetism,
    16: bool withPowder,
    17: bool withLiquid,
    18: bool withCompressor,
    19: bool withBattery,
    20: list<i64> listingIds,
    21: list<i64> skuIds,
    22: list<i32> promotionIds,
    23: i32 skuCount,
    24: i32 itemCount,
    25: CurrencyAmount itemTotal,
    26: CurrencyAmount discount,
    27: CurrencyAmount redeem,
    28: CurrencyAmount postage,
    29: CurrencyAmount orderAmount,
    30: CurrencyAmount postageDiscount,
    31: CurrencyAmount vat,
    32: CurrencyAmount payAmount,
    33: CurrencyAmount preAmount,
    34: CurrencyAmount dueAmount,
    35: double prepaymentRatio,
    36: PromotionType promotionType,
    37: OrderType orderType,
    38: FulFillType fulFillType,
    39: FulFillType thirdFulFillType,
    40: i16 thirdPlatformId,
    41: i32 thirdStoreId,
    42: string createdTime,
    43: string paidTime,
    44: string shippedTime,
    45: string deliveringTime,
    46: string deliveredTime,
    47: string closedTime,
    48: string lastUpdatedTime,
    49: optional PartnerOrder thirdOrder,
    50: optional PartnerUser thirdAccount,
    51: optional ThirdDeliveryAddress thirdAddress,
    52: optional PayState payState,
    53: optional list<OrderDetail> orderDetails,
    54: optional CancelInfo cancelInfo,
    55: optional Package package,
    56: optional CurrencyAmount onlinePaid,
    57: optional i32 salesAccountId,
    58: optional i16 salesAccountRole
    59: optional string remark
}

struct PaymentObject {
     1: PayMethod payMethod,
     2: list<PayType> payTypes,
     3: optional PayChannel payChannel,
     4: optional double prepaymentRatio,
     5: optional PrepaymentPostage prepaymentPostage,
     6: optional PayType finalPayType
}

struct SkuObject {
    1: i32 vendorId,
    2: i32 warehouseId,
    3: bool withMagnetism,
    4: bool withPowder,
    5: bool withLiquid,
    6: bool withCompressor,
    7: bool withBattery,
    8: i64 listingId,
    9: i64 skuId,
    10: FulFillType fulFillType,
    11: i32 itemCount,
    12: i32 promotionType,
    13: i32 promotionId,
    14: double salePrice,
    15: double originalPrice,
    16: double amount,
    17: double discount,
    18: double redeem,
    19: double vat,
    20: double postage,
    21: double postageDiscount,
    22: double preAmount,
    23: double dueAmount,
    24: double prepaymentRatio,
    25: double payAmount,
    26: optional bool ladderPriceUsed
    27: optional i32 ladderPriceId
    28: optional i32 dimension
}

struct SkuGroup {
    1: list<i32> vendorIds,
    2: i32 warehouseId,
    3: bool withMagnetism,
    4: bool withPowder,
    5: bool withLiquid,
    6: bool withCompressor,
    7: bool withBattery,
    8: PromotionType promotionType,
    9: FulFillType vendorFulFillType,
    10: FulFillType thirdFulFillType,
    11: list<SkuObject> skuObjects,
    12: double postage,
    13: double postageDiscount
    14: string remark
}

struct BillAndOrders {
    1: Bill bill,
    2: list<SaleOrder> saleOrders,
    3: list<PayBill> payBills
}

struct PayGateway {
    1: string appId,
    2: string name,
    3: list<string> currencyCodes=[],
    4: string logo,
    5: GatewayStatus status,
    6: optional i32 id,
    7: optional string updateTime,
    8: optional string logoUrl
}

struct PagingPayGateway {
    1: required i64 total,
    2: required list<PayGateway> data=[]
}

enum SaleOrderTimeType {
    CREATE_TIME = 1,
    EFFECTIVE_TIME = 2
}

struct BillList {
    1: i32 count,
    2: list<Bill> bills
}

struct SaleOrderList {
    1: i32 count,
    2: list<SaleOrder> orders
}

struct SaleOrderDetail {
    1: SaleOrder order,
    2: optional list<PayBill> payBills
    3: optional Bill bill
}

enum OperateCode{
    CREATE = 1,
    PAID = 2,
    CONFIRMED = 3,
    DISPATCH = 4,
    DELIVERED = 5,
    COMPLETED = 6,
    CANCEL = -1,
    REJECTED = -2
}

const string ORDER_PLACED = "Order Placed."
const string ORDER_PAID = "Order Paid."
const string ORDER_PREPAID  = "Order Prepaid."
const string ORDER_CONFIRMED = "Order confirmed."
const string ORDER_CANCELLED = "Order cancelled."
const string ORDER_DISPATCHED = "Goods dispatched from the vendor."
const string ORDER_IN_DELIVERY = "Goods being delivered."
const string ORDER_COMPLETED = "Order completed."
const string ORDER_REJECTED = "Order rejected."
const string ORDER_IN_DELIVERY_ADD_CODE = " by [{}] package#{}."

enum Operator {
    RESELLER = 1,
    E_COMMERCE_PLATFROM = 2,
    ADMIN = 3,
    VENDOR = 4,
    LOGISTICS = 5,
    SYSTEM = -1
}

struct OrderTrack {
    1: Operator operator,
    2: OperateCode operateCode,
    3: string description,
    4: i64 operatorId,
    5: string createdTime
}

enum RejectReason {
    GOODS_DAMAGED = 1,
    ITEM_DOES_NOT_MATCH  = 2,
    NO_REASON = 3,
    TIME_OUT = 4
}

struct AccountOrderStatistics {
    1: i32 billCount,
    2: i32 orderCount,
    3: i32 pendingPayOrderCount,
    4: i32 completeOrderCount,
    5: i32 cancelOrderCount,
    6: double successGMV
}

enum ApplyScale {
    ORDER = 1,
    SKU = 2,
    BILL = 3
}

enum AfterSaleMethod {
    RETURN_DELIVERY = 1,
    RETURN_REFUND = 2,
    REPAIR = 3,
    REFUND = 4,
    DELIVERY = 5
}

enum RefundBillState {
    NEW_CREATE = 1,
    PENDING_REVIEW = 2,
    PENDING_REFUND = 3,
    IN_REFUND = 4,
    COMPLETE = 5
}

enum ProcessState {
    NOT_STARTED = 1,
    IN_PROGRESS = 2,
    COMPLETE = 3
}
enum RefundMethod {
    ORIGINAL_ROAD = 1,
    BKASH = 2,
    BANK_CARD = 3,
    VOUCHER = 4
}

enum RefundReason {
    AFTER_SALE = 1,
    CANCEL_ORDER = 2,
    REJECT_ORDER = 3,
    OUT_OF_STOCK = 4
}

enum RefundWay {
    AUTO = 1,
    MANUAL = 2
}

struct RefundSourceOrder {
    1: i32 billId,
    2: list<i32> saleOrderIds,
    3: list<i32> orderDetailIds,
    4: double payAmount,
    5: list<i32> payBillIds
}

struct RefundSku {
    1: i64 skuId,
    2: i16 itemCount
}

struct RefundPayment {
    1: PayType sourcePayType,
    2: PayChannel sourcePayChannel,
    3: optional i32 payTransactionId,
    4: string refundDetail
}

struct RefundBill {
    1: i64 id,
    2: i64 accountId,
    3: i64 afterSaleId,
    4: string regionCode,
    5: list<i32> vendorIds,
    6: CurrencyAmount refundAmount,
    7: AfterSaleMethod afterSaleMethod,
    8: ApplyScale applicationScale,
    9: ProcessState processState,
    10: RefundMethod refundMethod,
    11: RefundReason refundReason,
    12: RefundWay refundWay,
    13: RefundBillState state,
    14: bool isNeedCheck,
    15: RefundSourceOrder sourceOrder,
    16: list<RefundSku> skus,
    17: RefundPayment refundPayment,
    18: optional i32 reviewerId,
    19: optional i32 refunderId,
    20: optional string createdTime,
    21: optional string effectedTime,
    22: optional string confirmedTime,
    23: optional string initiatedTime,
    24: optional string refundedTime
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
    8: i64 shippingAddressId 
}

enum PackageType {
    SALE_ORDER = 1
}

struct XedLogisticsOrder{
    1: i32 saleOrderId,
    2: string orderNo,
    3: string xedState
}

enum PreAmountType {
    AMOUNT_GT_ZERO = 1,
    AMOUNT_EQ_ZERO = -1
}

enum PrepaymentPostage {
    FIRST_PAY = 1,
    FINAL_PAY = 2
}

struct PrepaymentSetting {
    1: GatewayStatus state,
    2: double prepaymentRatio,
    3: PrepaymentPostage prepaymentPostage,
    4: PayType finalPayType
}

enum PaymentAction {
    LOAD_LINK = 1,
    GENERATE_QR_CODE = 2
}

struct PaymentProduct {
     1: PaymentAction action,
     2: optional string gatewayPageUrl,
     3: optional string qrCode
}

struct Voucher {
    1: i64 voucherId,
    2: list<i64> skuIds,
    3: i64 amount,
    4: i16 ownerType
}



