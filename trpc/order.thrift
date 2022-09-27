include "exceptions.thrift"
include "constants.thrift"
include "payment.thrift"
include "order_constants.thrift"
include "order_after_sale.thrift"


struct SaleOrderNotice {
    1: required i64 saleOrderId,
    2: required string code,
    3: i32 storeId,
    4: i32 payAmount,
    5: i32 postage,
    6: string createdAt,
    7: optional order_constants.DeliveryMethod deliveryMethod
}
struct Tax {
    1: required double taxRate,
    2: optional bool taxSwitch,
    3: optional i32 vat
}
struct Item {
    1: required i64 id, //SaleOrderDetailId or shipOrderDetailId
    2: required i64 skuId,
    3: required i64 salePrice,
    4: required i64 dealPrice,
    5: required i32 count,
    6: required i32 amount,
    7: optional i32 coinRedeem,
    8: optional i32 voucherRedeem,
    9: optional i32 warehouseId,
    10: optional i16 collected,
    11: optional i16 status,
    12: optional i32 priceRevision,
    13: optional i64 orderId,
    14: optional i16 discount,
    15: optional i16 coin,
    16: optional string createdAt,
    17: optional i32 activityType,
    18: optional i32 activityId,
    19: optional i32 validAmount
    20: optional bool ofsManageWarehouse
}

struct SimpleSaleOrderDetail {
    1: required i64 skuId,
    2: optional i64 saleOrderId,
    3: optional i64 salePrice,
    4: optional i64 dealPrice,
    5: optional i32 count,
    6: optional i32 amount,
    7: optional i32 warehouseId,
    8: optional i32 activityType,
    9: optional i32 activityId,
    10: optional i32 ofsManageWarehouse
}

struct SimpleSaleOrder{
    1: required i64 saleOrderId,
    2: required i16 storeId,
    3: required string code,
    4: optional i16 status,
    5: optional i16 region,
    6: optional string createdAt,
    7: optional string paidAt,
    8: required list<SimpleSaleOrderDetail> simpleSaleOrderDetail,
    9: optional i32 postage,
    10: optional order_constants.DeliveryMethod deliveryMethod,
    11: optional order_constants.SoType orderType,
    12: optional i32 preAmount,
    13: optional i32 dueAmount
}

struct PayBill {
    1: required i64 payBillId,
    2: required string payBillCode,
    3: required i64 billId,
    4: required i16 region,
    5: required i64 amount,
    6: required i16 type,
    7: required i16 status,
    8: required string createdAt,
    9: optional i64 receivedAmount,
    10: optional string expiredAt,
    11: optional string paidAt
}

struct VoucherBill {
    1: required i64 billId,
    2: required i64 payBillId,
    3: required i64 voucherId,
    4: required i32 amount,
    5: required i16 status,
    6: required list<i64> saleOrderDetailIds,
    7: optional string createdAt
}

struct PayAmount {
    1: required i16 type,
    2: required i32 amount
}

struct OrderBatch {
    1: required i64 batchId,
    2: required string code,
    3: required i16 region,
    4: required string createdAt,
    5: optional list<SaleOrderNotice> saleOrderNotices,
    6: optional list<Item> items,
    7: optional i32 itemTotal,
    8: optional i32 orderAmount,
    9: optional i16 postage,
    10: optional i32 discount,
    11: optional i32 redeem,
    12: optional i32 coin,
    13: optional list<PayAmount> payAmount,
    14: optional i64 billId,
    15: optional string billCode,
    16: optional list<PayBill> payBills,
    17: optional list<VoucherBill> voucherBills,
    18: optional double taxRate,
    19: optional i32 vat,
    20: optional i32 postageDiscount,
    21: optional i32 postageRedeem,
    22: optional order_constants.Gateway gatewayId,
    23: optional order_constants.PaymentMethods payMethod,
    24: optional double prepaymentRatio,
    25: optional i32 preAmount,
    26: optional i32 dueAmount
}

struct SimpleBatch {
    1: required i64 batchId,
    2: required string batchCode,
    3: required i64 accountId,
    4: required i16 region,
    5: required i64 addressId,
    6: required i16 ordersCount,
    7: required string createdAt,
    8: optional i64 billId,
    9: optional string billCode,
    10: optional list<SimpleSaleOrder> simpleSaleOrder,
    11: optional order_constants.PaymentMethods payMethod
}

struct OrderItem {
    1: required i64 skuId,
    2: required i64 storeId,
    3: required i64 salePrice,
    4: required i64 dealPrice,
    5: required i32 priceRevision,
    6: required i32 count,
    7: optional i32 discount,
    8: optional i16 paymentMethodId,
    9: optional i64 listingId,
    10: optional i32 warehouseId,
    11: optional i64 activityId,
    12: optional i16 activityType,
    13: optional bool isUseCoin = true,
    14: optional order_constants.IsWithBattery withBattery,
    15: optional bool isMagnetic,
    16: optional bool isPowder,
    17: optional bool isCompressor,
    18: optional list<i64> voucherIds = [],
    19: optional bool isPostageDiscount = true,
    20: optional i16 warehouseRegionId,
    21: optional bool isSelfDelivery,
    22: optional double commissionRate,
    23: optional i64 promotionId,
    24: optional bool isUsePromotion,
    25: optional bool isPlatformPostage,
    26: optional bool liquid,
    27: optional bool ofsManageWarehouse,
}

struct PostageInfo {
    1: required i32 postage=0,
    2: required i32 postageDiscount=0,
    3: required i32 postageRedeem=0,
    4: bool isPlatformPostage,
    5: bool isSelfDelivery,
    6: optional i32 storeId,
    7: optional i32 warehouseId
}

struct StoreItem {
    1: required i32 storeId,
    2: optional string remark,
    3: optional bool isContainSelfDelivery,
    4: optional i32 postage,
    5: optional double commissionRate
}

struct Bill {
    1: required i64 billId,
    2: required i64 batchId,
    3: required i64 accountId,
    4: required string billCode,
    5: required i16 region,
    6: required i16 status,
    7: required i32 itemTotal,
    8: required i32 orderAmount,
    9: required i32 postage,
    10: required i32 discount,
    11: required i32 redeem,
    12: required i32 payAmount,
    13: required i64 receivedAmount,
    14: required i16 payMethod,
    15: required string createdAt,
    16: optional i64 coin,
    17: optional i32 postageDiscount,
    18: optional i32 postageRedeem,
    19: optional string paidAt,
    20: optional string doneAt,
    21: optional i32 voucherAmount,
    22: optional double taxRate,
    23: optional i32 vat,
    24: optional order_constants.Gateway gatewayId,
    25: optional order_constants.SoType orderType,
    26: optional double prepaymentRatio,
    27: optional i32 preAmount,
    28: optional i32 dueAmount
}

struct PendingPaymentOrderDetail {
    1: required string batchCode,
    2: required i32 addressId,
    3: required list<SimpleSaleOrder> simpleSaleOrder,
    4: required Bill bill,
    5: required order_constants.PayStatus payStatus,
    6: required string batchCreatedAt,
    7: required list<PayAmount> payAmounts
    8: optional order_constants.SoType orderType
}

struct PendingPaymentOrder {
    1: required i64 batchId,
    2: required string batchCode,
    3: required i64 billId,
    4: required string billCode,
    5: required i64 payAmount,
    6: required list<Item> items,
    7: required string batchCreatedAt,
    8: required string billCreatedAt
}

struct SaleOrder {
    1: required i64 orderId,
    2: required string code,
    3: required i16 region,
    4: required string createdAt,
    5: required string paidAt,
    6: required list<Item> items,
    7: required i32 itemTotal,
    8: required i16 postage,
    9: required i32 discount,
    10: required i32 redeem,
    11: required list<PayAmount> payAmount,
    12: required i64 addressId,
    13: optional order_constants.ShipOrderStatus status,
    14: optional order_constants.PaymentMethods paymentMethod,
    15: optional i32 voucherAmount,
    16: optional double taxRate,
    17: optional i32 vat,
    18: optional order_after_sale.RefundSlip refundSlip,
    19: optional i64 storeId,
    20: optional bool userConfirmed,
    21: optional string userConfirmedAt,
    22: optional string remark,
    23: optional string remarkUpdatedAt,
    24: optional i32 amount,
    25: optional order_constants.PayStatus payStatus,
    26: optional order_constants.SoType orderType,
    27: optional i32 preAmount,
    28: optional i32 dueAmount,
    29: optional i32 needPayAmount
}

struct ShipOrder {
    1: required i64 orderId,
    2: required string code, // packageCode
    3: required i16 region,
    4: required string createdAt,
    5: required string paidAt,
    6: optional string collectedAt,
    7: optional string packedAt,
    8: optional string shippedAt,
    9: optional string deliveredAt,
    10: optional i64 saleOrderId,
    11: required string saleOrderCreatedAt,
    12: required list<Item> items,
    13: required i32 itemTotal,
    14: required i32 postage,
    15: required i32 discount,
    16: required i32 redeem,
    17: required list<PayAmount> payAmount,
    18: required i64 addressId,
    19: optional order_constants.ShipOrderStatus status,
    20: optional string saleOrderCode,
    21: optional order_constants.PaymentMethods paymentMethod,
    22: optional i32 voucherAmount,
    23: optional order_constants.ShortageOrder shortageOrder,
    24: optional list<order_constants.ShortageOrderDetail> shortageOrderDetails,
    25: optional order_constants.ShipOrderSubform subform,
    26: optional i32 amount,
    27: optional i64 packageId,
    28: optional double taxRate,
    29: optional i32 vat,
    30: optional order_constants.DeliveryMethod deliveryMethod,
    31: optional string dispatchedAt,
    32: optional string sellerDeliveredAt,
    33: optional order_constants.SoType orderType,
    34: optional i32 preAmount,
    35: optional i32 dueAmount
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

struct SaleOrderDetail {
    1: required i64 id,
    2: required i64 skuId,
    3: required i64 orderId,
    4: required i64 salePrice,
    5: required i64 dealPrice,
    6: required i32 priceRevision,
    7: required i16 count,
    8: required i32 discount,
    9: required i32 redeem,
    10: required i32 amount,
    11: required i16 status,
    12: required string createdAt,
    13: optional i16 warehouseId,
    14: optional i16 coin,
    15: optional i16 voucherRedeem
    16: optional bool ofsManageWarehouse
}

struct StateAndCoin {
    1: required i16 saleOrderState,
    2: optional i32 saleOrderCoin,
    3: optional bool isRefundVoucher,
    4: optional list<i64> voucherIds
}

// 后台
struct UserValidSaleorder{
    1: required i64 saleOrderId,
    2: required string saleOrderCode,
    3: required i32 itemTotal,
    4: required i32 payAmount,
    5: required i16 status,
    6: required string createdAt,
    7: required i64 addressId,
    8: required i16 region,
    9: optional string doneAt,
    10: optional i16 packageStatus
}

struct UserOrders {
    1: required i32 orderBatchCount,
    2: required i32 saleOrderCount,
    3: required i32 cancelCount,
    4: optional i32 unpaidCount,
    5: optional i32 unconfirmedCount,
    6: optional i32 unshippedCount,
    7: optional i32 inTransitCount,
    8: optional i32 completeCount,
    9: optional i32 rejectCount,
    10: required list<UserValidSaleorder> saleOrders
}

struct BackstageSaleOrder {
    1: required string saleOrderCode,
    2: required i64 saleOrderId,
    3: required i64 accountId,
    4: required i64 addressId,
    5: required i32 itemTotal,
    6: required i32 postage,
    7: required order_constants.SaleOrderStatus status,
    8: required string createdAt,
    9: required i32 storeId,
    10: optional i32 paid,
    11: optional string paidAt,
    12: optional i16 shipOrderCount,
    13: required i16 paymentMethod,
    14: optional i32 coinRedeem,
    15: optional i32 voucherRedeem,
    16: optional i16 platform,
    17: optional i16 region,
    18: optional i32 orderAmount,
    19: optional i16 discount,
    20: optional order_constants.SoType orderType,
    21: optional string closedAt,
    22: optional i32 vat,
    23: optional i64 warehouseId,
    24: optional bool userConfirmed,
    25: optional order_constants.DeliveryMethod deliveryMethod,
    26: optional i64 packageId,
    27: optional bool is_robot,
    28: optional i32 preAmount,
    29: optional i32 dueAmount,
    30: optional string confirmAt
    31: optional bool ofsManageWarehouse
}

struct SaleOrderList {
    1: required i32 saleOrderNum,
    2: required list<BackstageSaleOrder> saleOrders
}

struct ShipInfo {
    1: required i64 shipOrderId,
    2: required string shipOrderCode,
    3: required i16 shipOrderStatus,
    4: optional i64 packageId,
    5: optional string packageCode,
    6: optional i16 packageStatus,
    7: optional string packageCreatedAt,
    8: optional i16 rejectReason
}

struct SODList {
    1: required i64 batchId,
    2: required i64 saleOrderId,
    3: required i64 accountId,
    4: required i64 addressId,
    5: required i32 itemTotal,
    6: required i32 postage,
    7: required i16 status,
    8: required string createdAt,
    9: optional i32 paid,
    10: optional string paidAt,
    11: optional i16 shipOrderCount,
    12: required string code, // so code
    13: required i32 orderAmount,
    14: required list<Item> saleOrderDetail,
    15: required list<ShipInfo> shipInfos,
    16: optional i32 coin,
    17: required i32 storeId,
    18: required i16 paymentMethod,
    19: optional i16 paymentStatus,
    20: optional i32 coinRedeem,
    21: optional i32 voucherRedeem,
    22: optional order_constants.SoType orderType,
    23: optional string remark,
    24: optional order_constants.SaleOrderStatus cancelStatus,
    25: optional i32 vat,
    26: optional i64 warehouseId,
    27: optional bool userConfirmed,
    28: optional i32 discount,
    29: optional i16 region,
    30: optional i32 payAmount,
    31: optional i32 preAmount,
    32: optional i32 dueAmount,
    33: optional i32 postageDiscount,
    34: optional bool ofsManageWarehouse
}

struct ShipOrderInfo{
    1: required i64 id,
    2: required string code,
    3: required i64 saleOrderId,
    4: required i16 items,
    5: required i32 amount,
    6: required i16 status,
    7: required i32 coin,
    8: required list<ShipOrderDetail> skuLi,
    9: required string packedAt,
    10: required string collectedAt,
}

enum RejectStatus {
    shipped = 1,
    dispatched = 2,
    arrived = 3
}

enum RejectReason {
    goodsDamaged = 1,
    goodsNotSame = 2,
    noReason = 3,
    cancel = 4,
    timeout = 5
}

struct OneShipPackage {
    1: required i64 id,
    2: required i64 accountId,
    3: required string code,
    4: required i64 addressId,
    5: required i16 region,
    6: required order_constants.PackageStatus status,
    7: required i16 skuCount,
    8: required i16 itemCount,
    9: optional i32 storeId,
    10: optional i64 warehouseId,
    11: required i32 codAmount,
    12: optional i32 onlineAmount,
    13: optional i16 payMethod,
    14: optional order_constants.PayStatus payStatus,
    15: optional i16 sourceInventoryId,
    16: optional i16 deliveryId,
    17: optional string deliveryCode,
    18: optional i16 terminalDeliveryId,
    19: optional string terminalDeliveryCode,
    20: required string createdAt,
    21: optional string shippedAt,
    22: optional string dispatchedAt,
    23: optional string deliveredAt,
    24: required ShipOrderInfo shipOrder,
    25: required i16 shoCount,
    26: required string earlyShoCreatedAt,
    27: required i64 saleOrderId,
    28: optional string saleOrderCode,
    29: optional order_constants.IsWithBattery withBattery,
    30: optional bool isMagnetic,
    31: optional bool isPowder,
    32: optional bool isCompressor,
    33: optional order_constants.SoType saleOrderType,
    34: optional order_constants.RejectionReason rejectReason,
    35: optional RejectStatus rejectStatus,
    36: optional order_constants.DeliveryMethod deliveryMethod,
    37: optional string sellerDeliveredAt,
    38: optional i32 discount,
    39: optional bool liquid,
    40: optional i32 payAmount,
    41: optional order_constants.SubsequentAction subsequentAction,
    42: optional string againLogisticsNo,
    43: optional list<string> stockReceivingIds
    44: optional bool ofsManageWarehouse,
    45: optional string fullLogistics,
    46: optional string fullLogisticsCode
}

struct TradeSkuInfo {
    1: required i64 skuId,
    2: required i64 skuCount,
    3: required i64 orderCount,
    4: required i64 accountCount
}

struct TradeSkuCount {
    1: required i64 skuCount,
    2: required list<TradeSkuInfo> skus
}

struct TradeSkuOrder {
    1: required i64 shipOrderId,
    2: required string shipOrderCode,
    3: required string createdAt,
    4: required i64 accountId,
    5: required i32 skuCount,
    6: required i64 saleOrderId,
    7: required string saleOrderCode,
    8: required i64 packageId
}

struct TradeOneSku {
    1: required i64 total,
    2: list<TradeSkuOrder> relateOrders
}

struct OrderLog {
    1: required string createdAt,
    2: required string content
}

struct SetParameter{
    1: required i64 id,
    2: required string value,
}

struct Parameter{
    1: required i64 id,
    2: required i32 regionId,
    3: required string name,
    4: required string value,
    5: required string dataType,
    6: required string paramModule
}

struct ParcelLog {
    1: required i64 packageId,
    2: required i64 accountId,
    3: required i16 deliverId,
    4: required i64 addressId,
    5: required i32 operatorId,
    6: required string operatorName,
    7: required i16 status,
    8: required string createdAt,
    9: optional i16 createdBy,
    10: optional string deliveryCode,
    11: optional string updatedAt,
    12: optional string productId
}

struct ParcelInsertionResponse{
    1: required list<string> errors,
    2: required i16 responseCode,
    3: required bool success,
    4: optional string message,
    5: optional string ID,
    6: optional string trackCode
}

struct MappingCityAndArea {
    1: required string city,
    2: required string area,
    3: optional string pincode
}

struct Sku {
    1: required i64 skuId,
    2: required i16 vendor,
    3: optional string matchSkuId,
    4: optional i32 count,
    5: optional i64 sodId
}

struct OutOrder {
    1: required i64 saleOrderId,
    2: required i16 vendor,
    3: required string createdAt,
    4: required i16 status,
    5: required string soCreatedAt,
    6: required list<i64> skuIds,
    7: optional string failedReason,
    8: optional string failedAt,
    9: optional string vendorOrderId,
    10: optional i64 accountId
}

struct OutOrderList{
    1: required i64 count,
    2: required list<OutOrder> outOrders
}

struct Voucher {
    1: required i64 voucherId,
    2: required i32 amount,
    3: required list<i64> skuIds,
    4: required order_constants.VoucherOwner ownerType
}

enum OrderType {
    BATCH_ORDER = 1,
    BILL = 2,
    SALE_ORDER = 3,
    SHIP_ORDER = 4,
    SHIP_PACKAGE = 5
}

enum OrderTradeState {
    ALL = 1,
    SUCCESS = 2,
    FAIL = 3
}

enum ComparisonOperation {
    GT = 1,
    GTE = 2,
    LT = 3,
    LTE = 4,
    E = 5
}

enum UserType {
    PLACE_ORDER = 1, // 下单用户
    TRTADE_SUCCESS = 2, // 交易成功用户
    ONLINE_PAID = 3, // Online Pay支付完成用户
    ONLINE_PAID_TRADE_SUCCESS = 4, // Online Pay交易成功用户
}

enum ConfirmOrderType {
    ALL = 1,
    PART = 2,
    WAIT = 3
}

struct OrderCreated {
    1: required i32 times,
    2: required ComparisonOperation comparison
}

struct OrderNumber {
    1: required OrderType order_type,
    2: required OrderTradeState order_trade_state,
    3: required OrderCreated created_times,
}

struct PurchaseAmount {
    1: required i32 amount,
    2: required bool isAllPuchases,
    3: required ComparisonOperation comparison
}

struct SaleOrderRelated {
    1: required BackstageSaleOrder saleOrder,
    2: required i32 amountPaid,
    3: required i32 sumPayable,
    4: required list<SaleOrderDetail> saleOrderDetails
}

struct ShortageOrderDetail {
    1: required order_constants.ShortageOrder shortageOrder,
    2: required SaleOrderRelated saleOrderRelated,
    3: optional order_after_sale.RefundSlip refundSlip
}

struct UserShipPackageRelated {
    1: required i64 packageId,
    2: required string packageCode,
    3: required i16 packageStatus,
    5: required i16 region,
    6: required i64 saleOrderId,
    7: required string saleOrderCreatedAt,
    8: required string saleOrderCode,
    9: required i64 shipOrderId,
    10: required i16 shipOrderStatus,
    11: required list<ShipOrderDetail> shipOrderDetails
}

struct PayBillDetail {
    1: required i64 payBillId,
    2: required i64 payBillDetailId,
    3: required i32 amount,
    4: required string paidAt,
    5: optional i64 packageId
}

struct OrderRelatedInfo {
    1: required BackstageSaleOrder saleOrder,
    2: required list<order_after_sale.ShipOrderDetailRelated> shipOrderDetails
    3: required order_constants.PayStatus paymentStatus,
    4: optional list<order_after_sale.AfterSaleOrder> afterSaleOrders,
    5: optional list<PayBill> payBills,
    6: optional list<PayBillDetail> payBillDetails,
    7: optional string tranId
}

struct RefundSlipDetail {
    1: required order_after_sale.RefundSlip refundSlip,
    2: required list<BackstageSaleOrder> saleOrders,
    3: required list<PayBill> payBills,
    4: optional order_constants.ShortageOrder shortageOrder,
    5: optional order_after_sale.AfterSaleOrder afterSaleOrder,
    6: optional payment.PayTransactions payTransaction,
    7: optional string terminalDeliveryCode
}

enum PacelType {
    shipPackage = 1,
    deliveryOrder = 2
}

struct PromotionRule {
    1: optional i64 priceBreak,
    2: optional i64 discount,
    3: optional bool per
}

enum PromotionType {
    PRICE_BREAK_DISCOUNT = 1
}

struct PromotionDiscount {
    1: i64 promotionId,
    2: PromotionType type,
    3: PromotionRule rule,
    4: bool noStoreVoucher,
    5: bool noPlatformVoucher,
    6: bool noCoins,
    7: i64 regionId
}


service OrderService {
    i64 create_pre_order(
        1: i64 accountId, 2: i16 region, 3: list<OrderItem> skuItems),

    i64 patch_pre_order(
        1: i64 preOrderId, 2: i64 accountId, 3: list<OrderItem> skuItems),

    OrderBatch create(
    1:list<OrderItem> items, 2:i64 accountId, 3:i32 region, 4:i64 addressId,
    5:PostageInfo postageInfo, 6:optional i32 redeem) throws (
    1:exceptions.InvalidOperationException ioe,
    2:exceptions.DatabaseException ie),

    order_constants.IsUseCod get_user_use_cod_info(
        1: i64 account_id, 2: optional list<OrderItem> sku_items,
        3: optional i16 postage, 4: optional list<PromotionDiscount> discounts,
        5: optional i16 region_id),

    order_constants.SoCount get_user_so_count(
    1: i16 region_id, 2: i64 account_id,
    3: optional order_constants.SoType so_type, 4: optional string start_time,
    5: optional string end_time),

    OrderBatch place_order(
    1: i64 accountId, 2: i32 region, 3: i64 addressId, 4: order_constants.PaymentMethods paymethod,
    5: set<PostageInfo> postage_infos, 6: list<OrderItem> items, 7: i32 redeem=0,
    8: i32 coin=0, 9: i64 preOrderId, 10: optional i16 timeSelected,
    11: optional list<Voucher> vouchers=[], 12: optional string platform,
    13: optional list<StoreItem> store_items=[],
    14: optional order_constants.Gateway pay_channel,
    15: optional list<PromotionDiscount> discounts, 16: optional bool is_robot,
    17: optional order_constants.PrepaymentSetting prepayment_config)
    throws (1:exceptions.DatabaseException ie,
    2:exceptions.InvalidOperationException ioe),

    void complete_online_pay(1: i64 bill_id)
    throws(1:exceptions.NotFoundException nfe),

    list<PendingPaymentOrder> get_pending_payment_order(
    1: i64 account_id, 2: i16 region, 3: i64 last_id, 4: i16 limit) throws (
    1:exceptions.InvalidOperationException ioe,
    2:exceptions.InternalException ie),

    PendingPaymentOrderDetail get_order_bill_detail(
    1: i64 bill_id, 2: i64 account_id) throws(
    1:exceptions.NotFoundException nfe),

    list<SaleOrder> getPendingDispatch(
    1: i64 accountId, 2: i16 region, 3: optional list<i16> saleOrderTypes)
    throws (1:exceptions.InvalidOperationException ioe,
    2:exceptions.InternalException ie), // old

    list<SimpleSaleOrder> get_user_sale_orders(
    1: i64 account_id, 2: i16 region,
    3: order_constants.USER_ORDER_LIST_TYPE order_type, 4: i64 last_id,
    5: i16 limit) throws (1:exceptions.InvalidOperationException ioe),

    SaleOrder get_sale_order_detail(
        1: i64 saleOrderId, 2: optional i64 accountId, 3: optional i32 store_id)
    throws(1:exceptions.NotFoundException nfe),

    SaleOrder user_confirm_order(1: i64 so_id, 2: i64 account_id, 3: optional string remark)
    throws(1:exceptions.NotFoundException nfe),

    list<ShipOrder> getShipOrders(
    1: i64 accountId, 2: i16 region, 3: optional i16 shipOrderType) throws (
    1:exceptions.InvalidOperationException ioe,
    2:exceptions.InternalException ie),// old

    list<UserShipPackageRelated> get_user_ship_packages(
    1: i64 account_id, 2: i16 region, 3: order_constants.USER_ORDER_LIST_TYPE order_type,
    4: i64 last_id, 5: i16 limit) throws (1:exceptions.InvalidOperationException ioe),

    ShipOrder get_ship_order_detail(
        1: i64 shipOrderId, 2: optional i64 accountId, 3: optional i32 store_id)
    throws(1:exceptions.NotFoundException nfe),

    ShipOrder get_ship_package_detail(1: i64 package_id, 2: i64 account_id)
    throws(1:exceptions.NotFoundException nfe), // no use

    void user_confirm_receipt(1: i64 account_id, 2: i64 ship_order_id)
    throws(1:exceptions.NotFoundException nfe),

    UserOrders get_user_orders(
    1: i32 account_id, 2: optional i32 start_index, 3: optional i32 limit,
    4: optional i16 region_id) throws (1: exceptions.InternalException ie,
    2:exceptions.InvalidOperationException ioe),

    SaleOrderList get_sale_order_li(
    1: i16 status, 2: i16 region, 3: i16 time_type, 4: string start_time,
    5: string end_time, 6: i32 start_index, 7: optional i16 limit,
    8: optional list<i64> account_ids, 9: optional string code_or_id,
    10: optional list<i64> sku_ids, 11: optional order_constants.PaymentMethods pay_method,
    12: optional list<i64> address_ids, 13: optional order_constants.PayStatus pay_status,
    14: optional i32 warehouse_id, 15: optional list<i32> store_ids,
    16: optional bool user_confirmed, 17: optional order_constants.SoType so_type,
    18: optional order_constants.FromOrigin origin,
    19: optional order_constants.DeliveryMethod delivery_method,
    20: optional bool is_robot, 21: optional i64 activity_id,
    22: optional list<i64> listing_ids, 23: optional bool delivery_from_china,
    24: optional list<order_constants.PaymentMethods> pay_methods,
    25: optional list<i32> perfee_warehouse_ids),

    SODList getBackstageOrderDetail(1: i64 saleOrderId) throws(
        1:exceptions.NotFoundException nfe),

    order_constants.OrderList get_order_list(
    1: order_constants.SaleOrderStatus status=0, 2: i16 region_id,
    3: list<i32> store_ids=[], 4: string start_time, 5: string end_time,
    6: optional order_constants.OrderTimeType time_type=1,
    7: optional i32 start_index=0, 8: optional i16 limit=0,
    9: optional string code_or_id, 10: optional i16 pay_method=0,
    11: optional i16 pay_status=0, 12: optional list<i32> warehouse_ids,
    13: optional list<i64> sku_ids=[], 14: optional list<i64> account_ids=[],
    15: optional list<i64> address_ids=[],
    16: optional order_constants.FromOrigin origin,
    17: optional bool delivery_from_china),

    order_constants.OrderRelated get_one_sale_order(
        1: i64 so_id, 2: optional i64 package_id) throws(
        1:exceptions.NotFoundException nfe),

    list<order_constants.SimpleSoRelated> get_simple_so_li(1: list<i64> so_ids),

    SaleOrderList get_sale_orders() throws (
        1:exceptions.InvalidOperationException ioe),

    order_constants.SaleOrder get_so_info(1: i64 so_id),

    list<order_constants.SaleOrder> get_sale_orders_by_bill_id(1: i64 bill_id),

    list<order_constants.Sku> get_in_transit_so_info(1: i64 so_id),

    order_constants.ConfirmOrderRes confirm_order(
    1: i64 sale_order_id, 2: ConfirmOrderType confirm_type,
    3: list<Sku> sku_info, 4: order_constants.OrderOperator operator,
    5: i64 operator_id)throws(
    1: exceptions.NotFoundException nfe,
    2: exceptions.InvalidOperationException ioe),

    order_constants.PackagesRes get_ship_packages(
    1: i16 status, 2: i16 region, 3: i16 time_type, 4: string start_time,
    5: string end_time, 6: i32 start_index, 7: optional i16 limit,
    8: optional i64 so_id, 9: optional string package_code,
    10: optional list<i64> account_ids, 11: optional list<i64> address_ids,
    12: optional string sho_code, 13: optional i64 sku_id,
    14: optional i16 pay_method, 15: optional list<i32> store_ids,
    16: optional i32 warehouse_id, 17: optional bool is_export,
    18: optional order_constants.SoType so_type,
    19: optional order_constants.FromOrigin origin,
    20: optional order_constants.DeliveryMethod delivery_method,
    21: optional list<i64> listing_ids,
    22: optional bool delivery_from_china,
    23: optional list<i16> pay_methods,
    24: optional list<i32> perfee_warehouse_ids),

    OneShipPackage get_package_detail(1: i64 package_id) throws(
    1:exceptions.NotFoundException nfe),

    OneShipPackage get_package_detail_by_so_id(1: i64 order_id) throws(
    1:exceptions.NotFoundException nfe),

    order_constants.OrderInfo get_order_info(
        1: i64 so_id)throws(1:exceptions.NotFoundException nfe),

    order_constants.PackageRelated get_package_related(1: i64 package_id)
    throws(1:exceptions.NotFoundException nfe),

    OneShipPackage dispatch_package(
    1: i64 package_id, 2: order_constants.OrderOperator operator,
    3: i64 operator_id, 4: optional string delivery_code,
    5: optional order_constants.china_express delivery_id,
    6: optional i16 source_id,
    7: optional string full_logistics,
    8: optional string full_logistics_no)throws (
    1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    OneShipPackage append_global_logistic_number(
    1: i64 package_id, 2: order_constants.OrderOperator operator,
    3: i64 operator_id, 4: optional string delivery_code,
    5: optional order_constants.china_express delivery_id,
    6: optional i16 source_id)throws (
    1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    void append_domestic_logistics_codes(
        1: list<i64> package_ids, 2: order_constants.china_express logistics_id,
        3: string logistics_code, 4: i32 store_id) throws (
        1:exceptions.NotFoundException nfe),

    OneShipPackage append_whole_logistics_number(
        1: i64 package_id, 2: order_constants.OrderOperator operator,
        3: i64 operator_id, 4: string delivery_code,
        5: order_constants.Courier delivery_id),

    OneShipPackage delivery_package(
    1: i64 package_id, 2: order_constants.OrderOperator operator,
    3: i64 operator_id, 4: string delivery_code, // code or remarks
    5: order_constants.Courier delivery_id, 6: optional i16 source_id)throws (
    1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    OneShipPackage seller_delivered_package(
    1: i64 package_id, 2: order_constants.OrderOperator operator,
    3: i64 operator_id)throws (1:exceptions.NotFoundException nfe),

    OneShipPackage receive_package(
    1: i64 package_id, 2: order_constants.OrderOperator operator,
    3: optional i64 operator_id, 4: optional string operate_time,
    5: optional bool is_callback)throws (
    1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    OneShipPackage reject_package(
        1: i64 package_id, 2: order_constants.OrderOperator operator,
        3: i64 operator_id, 4: RejectReason reason,
        5: RejectStatus old_status,
        6: optional order_constants.StorageType storage_type,
        7: optional bool has_subsequent) throws (
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.NotFoundException nfe),

    TradeSkuCount get_trade_skus(
        1: order_constants.TradeSkuType trade_type, 2: i32 start_index,
        3: i16 limit, 4: optional string start_time, 5: optional string end_time,
        6: optional i64 sku_id, 7: optional i64 account_id,
        8: optional i16 warehouse_id, 9: optional i16 region_id,
        10: optional string field,
        11: optional list<i32> perfee_warehouse_ids) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),

    order_constants.SaleOrderSkuList get_sale_order_sku_list(
        1: order_constants.TradeSkuType sku_state, 2: i32 start_index,
        3: i16 limit, 4: optional string start_time, 5: optional string end_time,
        6: optional list<i32> store_ids, 7: optional i32 warehouse_id,
        8: optional i16 region_id, 9: optional list<i32> perfee_warehouse_ids)
        throws (1:exceptions.InvalidOperationException ioe),

    list<OrderLog> getOrderTrackingLog(
        1: i64 saleOrderId,2: optional i64 shipOrderId) throws (
        1:exceptions.InvalidOperationException ioe),

    TradeOneSku get_related_orders(
        1: i64 sku_id, 2: i16 trade_type, 3: i32 start_index, 4: i32 limit,
        5: optional string start_time, 6: optional string end_time,
        7: optional i64 account_id, 8: optional i16 region_id) throws (
        1:exceptions.InvalidOperationException ioe),

    StateAndCoin cancel_sale_order(
    1: i64 saleOrderId, 2: i64 accountId, 3: optional list<Sku> skuInfo)
    throws (1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    void is_cancel_outer_order(1: i64 so_id, 2: list<Sku> sku_info),

    StateAndCoin cancel_backstage_order(
    1: i64 saleOrderId, 2: optional list<Sku> skuInfo,
    3: order_constants.OrderOperator operator, 4: optional i64 operator_id,
    5: optional order_constants.CANCEL_REASON cancel_reason,
    6: optional string reason_detail)
    throws (1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    list<Parameter> get_parameter_list(1:i32 region_id, 2:string param_module),

    Parameter get_parameter(
        1:i32 region_id, 2:string param_module, 3:string name),

    void set_parameters(1:list<SetParameter> parameters),

    ParcelLog add_parcel_logs(
        1: i64 accountId, 2: i64 addressId, 3: i64 packageId,
        4: order_constants.Courier deliverId, 5: i32 operatorId,
        6: string operatorName, 7: i16 status, 8: string product_id,
        9: PacelType parcel_type, 10: optional i16 createdBy,
        11: optional string deliveryCode) throws (
        1:exceptions.InvalidOperationException ioe),

    ParcelLog patch_parcel_logs(
        1: i64 packageId, 2: i16 createdBy, 3: i16 status,
        4: PacelType parcel_type, 5: order_constants.Courier deliver_id,
        6: optional string deliveryCode) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),

    ParcelInsertionResponse create_e_courier_order(
        1: string recipientName, 2: string recipientMobile,
        3: string recipientCity, 4: string recipientArea,
        5: string recipientAddress, 6: string packageCode,
        7: i64 productPrice, 8: string paymentMethod,
        9: optional string recipientLandmark, 10: optional string parcelType,
        11: optional i16 isAnonymous, 12: optional string requestedDeliveryTime,
        13: optional string deliveryHour, 14: optional string recipientZip,
        15: optional string productId, 16: optional string pickAddress,
        17: optional string comments) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie,
        3: exceptions.NotFoundException nfe),

    ParcelInsertionResponse place_child_e_courier_order(
        1: order_constants.EcourierPartner ep_info,
        2: order_constants.EcourierRecipient recipient_info,
        3: string package_code, 4: string shipping_price,
        5: optional i16 payment_method, // cod: 1, other:2
        6: optional i64 product_price, 7: optional i64 actual_product_price,
        8: optional i16 number_of_item, 9: optional string comments,
        10: optional string parcel_detail, 11: optional string order_code, // product_id
        )throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie,
        3: exceptions.NotFoundException nfe),

    ParcelInsertionResponse create_e_desh_order(
        1: string recipient_name, 2: string recipient_mobile,
        3: string recipient_city, 4: string recipient_area,
        5: string recipient_address, 6: i64 order_id, 7: i32 package_amount,
        8: string pay_method, 9: string products_desc,
        10: order_constants.PackageType package_type, 11: i64 package_id,
        12: string pincode)
        throws (1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie,
        3: exceptions.NotFoundException nfe),

    ParcelInsertionResponse create_logistics_order(
        1: i16 region_id, 2: order_constants.Courier delivery_id,
        3: i64 package_id, 4: order_constants.PackageType package_type,
        5: optional order_constants.ExFcsParameter ex_fcs_p,
        6: optional order_constants.SagawaParameter sagawa_p,
        7: optional string x_ed_params) throws(
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie),

    order_constants.LogisticsSheet get_logistics_sheet(
        1: order_constants.Courier delivery_id,
        2: order_constants.PackageType package_type,
        3: i64 package_id) throws(
        1: exceptions.NotFoundException nfe),

    void print_sagawa_label(
        1: string control_code, 2: order_constants.PackageType package_type,
        3: order_constants.SagawaSchType sch_type, 4: list<string> order_keys)
    throws(1: exceptions.InternalException ie),

    MappingCityAndArea get_mapping_city_and_area (
        1: order_constants.Courier courier, 2: i32 areaId) throws (
        1: exceptions.NotFoundException nfe),

    order_constants.MappingAddress get_mapping_address(
        1: order_constants.Courier courier, 2: i32 perfee_city_id) throws (
        1: exceptions.NotFoundException nfe),

    list<order_constants.ECourierBranch> get_e_courier_reseller_branches(),

    string get_perfee_bkash(1: i64 account_id, 2: i64 bill_id),

    string get_perfee_kbz_url(1: i64 account_id, 2: i64 bill_id),

    string get_initial_payment_url(
        1: i64 account_id, 2: i64 bill_id, 3: order_constants.Gateway gateway)
    throws(1: exceptions.NotFoundException nfe),

    payment.PaySession get_pay_session(1: i64 session_id),

    payment.PayTransactions get_pay_transaction(
        1: i64 bill_id, 2: optional order_constants.Gateway gateway_id),

    order_constants.CreateBkashAgreementRes initiate_bkash_agreement(
        1: i64 bill_id, 2: string payer_reference, 3: i64 account_id,
        4: string platform) throws(1: exceptions.NotFoundException nfe,
        2: exceptions.InternalException ie),

    order_constants.BkashExecuteResult execute_bkash(
        1: string payment_id, 2: order_constants.ExecuteWay execute_way,
        3: string token)throws (1: exceptions.NotFoundException nfe,
        2: exceptions.InternalException ie),

    string get_user_bkash_account(1: i64 account_id), // not found, return ""

    void delete_user_bkash_account(1: i64 account_id) throws (
        1: exceptions.InternalException ie, 2: exceptions.NotFoundException nfe),

    order_constants.PaymentProduct initiate_online_payment(
        1: i64 bill_id, 2: string currency, 3: order_constants.Gateway gateway,
        4: string platform, 5: optional order_constants.SslParam ssl_params,
        6: optional order_constants.BkashParam bkash_params,
        7: optional order_constants.GMOParam gmo_params,
        8: optional order_constants.LipaPayParam lipa_pay) throws(
        1: exceptions.NotFoundException nfe, 2: exceptions.InternalException ie,
        3: exceptions.InvalidOperationException ioe),

    i64 get_bill_by_payment_id(
        1: string payment_id, 3: order_constants.Gateway gateway) throws(
        1: exceptions.NotFoundException nfe),

    void validate_ssl_payment(
        1: payment.SslNoticeParams notice_params, 2: i16 gateway) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.NotFoundException nfe),

    void validate_payment_with_ipn(
        1: string param, 2: order_constants.Gateway gateway) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.NotFoundException nfe),

    void validate_refund_with_ipn(
        1: string param, 2: order_constants.Gateway gateway) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.NotFoundException nfe),

    order_constants.PayStatus get_payment_status(1: i64 bill_id) throws (
        1: exceptions.NotFoundException nfe, 2: exceptions.InternalException ie),

    void virtual_payment(1: i64 bill_id, 2: string currency, 3: i16 gateway_id),

    payment.PaySession verify_transaction(
        1: order_constants.Gateway pay_channel,
        2: optional i64 bill_id,
        4: optional string reference,
        5: optional i64 session_id,
        6: optional order_constants.SignatureParam params),

    void user_logout(1: i64 account_id),

    SimpleBatch get_batch_by_bill_id(1: i64 bill_id) throws (
        1: exceptions.NotFoundException nfe),

    SimpleBatch get_batch_by_so_id(1: i64 so_id) throws (
        1: exceptions.NotFoundException nfe),

    Bill get_one_bill(1: i64 bill_id),

    StateAndCoin cancel_bill_order(1: i64 bill_id, 2: i64 account_id) throws (
        1: exceptions.NotFoundException nfe,
        2: exceptions.InvalidOperationException ioe,
        3: exceptions.InternalException ie),

    StateAndCoin consume_online_bill_queue(
        1: i64 bill_id, 2: i64 account_id) throws (
        1: exceptions.NotFoundException nfe,
        2: exceptions.InvalidOperationException ioe,
        3: exceptions.InternalException ie),

    order_constants.CancelSosReturn is_cancel_batch_so(
    1: i64 bill_id, 2: i64 account_id,
    3: order_constants.OrderOperator operator, 4: i64 operator_id),

    void vendor_order_cancelled_notice(
        1: i64 order_id, 2: i16 vendor) throws (
        1: exceptions.NotFoundException nfe),

    void create_outer_order(1: string order_items, 2: i64 order_id),

    void payoff_vendor_order(1: string vendor_order_id, 2: i64 sale_order_id),

    void vendor_order_shipped_notice(
        1: i64 order_id, 2: i16 vendor) throws (
        1: exceptions.NotFoundException nfe),

    OutOrderList get_failed_out_orders(1: i32 start_index, 2: i16 limit,
        3: i16 vendor, 4: string start_time, 5: string end_time, 6: i16 region_id)
    throws (1: exceptions.InvalidOperationException ioe),

    list<PayBill> get_pay_bill_by_conditions(
        1: optional i64 so_id, 2: optional string so_code) throws (
        1: exceptions.NotFoundException nfe),

    i32 get_order_count(
        1: i16 region, 2: i64 order_type, 3: optional i16 order_status,
        4: optional i64 account_id),

    i64 get_recent_address_id(1: i64 account_id, 2: i16 region_id),

    list<i64> get_account_ids(
        1: string start_time, 2: string end_time,  3: optional UserType user_type,
        4: optional list<i64> user_ids, 5: optional PurchaseAmount purchase_amount,
        6: optional list<OrderNumber> order_number, 7: optional i16 region_id),

    order_constants.ShortageOrders get_shortage_orders(
        1: string start_time, 2: string end_time,
        3: order_constants.ShortageOrderType shortage_order_type,
        4: i32 start_index, 5: i32 limit, 6: i16 region_id,
        7: optional string sort_field),

    ShortageOrderDetail get_shortage_order_details(1: i64 shortage_order_id)
    throws(1: exceptions.NotFoundException nfe),

    list<order_constants.SkuHistoryPriceRelated> get_history_sku_price(
        1: i64 sku_id, 2: i16 region_id),

    list<order_constants.ActivitySkuCount> get_user_activity_skus(
        1: i64 account_id, 2: i16 region,
        3: list<order_constants.SkuActivity> sku_li),

    order_constants.ActivitySkuCount get_user_activity_sku(
        1: i64 account_id, 2: i16 region,
        3: order_constants.SkuActivity sku_item),

    list<Sku> get_promotion_skus_sold(
        1: i16 activity_type, 2: i32 activity_id, 3: list<i64> sku_ids,
        4: i16 region_id),

    void update_package_track(1: i64 package_id),

    list<order_after_sale.ShipOrderDetailRelated> get_user_completed_skus(
        1: i64 account_id, 2: i16 region, 3: i32 start_index,
        4: i16 limit, 5: optional string order_by, 6: optional i16 days),

    list<order_after_sale.SimpleAfterSaleOrder> get_user_after_sale_orders(
        1: i64 account_id, 2: i16 region, 3: i32 start_index, 4: i16 limit,
        5: optional list<i16> status, 6: optional string order_by),

    order_after_sale.AfterSaleOrder create_after_sale_order (
        1: i64 account_id, 2: i64 ship_order_detail_id, 3: i64 sku_id,
        4: i16 count, 5: order_after_sale.AfterSaleReason reason,
        6: order_after_sale.AfoInitiator initiator, 7: string reason_detail,
        8: list<string> images, 9: order_after_sale.AfterSaleWay after_sale_way,
        10: order_after_sale.AfoOrigin origin, 11: order_after_sale.ApplyScale application_scale,
        12: i16 region, 13: optional order_after_sale.PostageBurden postage_burden,
        14: optional string account_source, 15: optional i32 staff_id,
        16: optional i64 sale_order_id, 17: optional string video_name)
        throws(1: exceptions.NotFoundException nfe,
        2: exceptions.InvalidOperationException ioe),

    order_after_sale.ShipOrderDetailRelated get_after_sale_sku_detail (
        1: i64 account_id, 2: i16 region, 3: i64 ship_order_detail_id)
        throws(1: exceptions.NotFoundException nfe),

    bool check_order_is_in_after_sale(
        1: i64 account_id, 2: i16 region, 3: i64 ship_order_detail_id)
        throws(1: exceptions.InvalidOperationException ioe),

    order_after_sale.AfterSaleOrderDetail get_after_sale_detail(
        1: i64 account_id, 2: i16 region, 3: i64 after_sale_id)
        throws(1: exceptions.NotFoundException nfe),

    order_after_sale.AfterSaleOrder get_after_sale_order(1: i64 after_sale_id)
        throws(1: exceptions.NotFoundException nfe),

    void cancel_after_sale(
        1: i64 account_id, 2: i16 region, 3: i64 after_sale_id)
        throws(1: exceptions.NotFoundException nfe),

    OrderRelatedInfo get_order_related_info(
        1: OrderType order_type, 2: string order_code, 3: i16 region)
        throws(1: exceptions.NotFoundException nfe,
        2: exceptions.InvalidOperationException ioe),

    order_after_sale.AfterSaleOrderList get_after_sale_orders(
        1: list<i16> status, 2: i64 start_index, 3: i16 limit,
        4: string start_time, 5: string end_time, 6: i16 region,
        7: optional i32 store_id, 8: optional i64 account_id,
        9: optional string so_code, 10: optional string package_code,
        11: optional string order_by, 12: optional bool is_appeal),

    order_after_sale.AfterSaleOrderRelated get_after_sale_order_detail(
        1:i64 after_sale_order_id, 2: i64 account_id, 3: i16 region),

    void seller_auto_reject_after_sale(1: i64 after_sale_order_id) throws(
        1: exceptions.NotFoundException nfe),

    void auto_end_reject_after_sale(1: i64 after_sale_order_id),

    order_after_sale.SellerAfterSaleLog seller_review_after_sale(
        1: i64 after_sale_order_id, 2: order_after_sale.AfterSaleWay method,
        3: order_after_sale.ReviewResult review_res, 4: i64 store_id,
        5: i32 staff_id, 6: order_after_sale.PostageBurden postage_burden,
        7: i32 refund_amount) throws(1: exceptions.NotFoundException nfe,
        2: exceptions.InvalidOperationException ioe),

    order_after_sale.PlatformAfterSaleLog platform_review_after_sale(
        1: i64 after_sale_order_id, 2: order_after_sale.AfterSaleWay method,
        3: order_after_sale.ReviewResult review_res, 4: i32 staff_id,
        5: order_after_sale.PostageBurden postage_burden, 6: i32 refund_amount)
        throws(1: exceptions.NotFoundException nfe,
        2: exceptions.InvalidOperationException ioe),

    order_after_sale.RefundSlipList get_refund_slips(
        1: i64 start_index, 2: i16 limit, 3: string start_time,
        4: string end_time, 5: i16 region, 6: list<i16> status,
        7: optional i64 account_id, 8: optional string code_or_id,
        9: optional i32 store_id, 10: optional i64 refund_id),

    RefundSlipDetail get_refund_slip_detail(1: i64 refund_slip_id)
    throws(1: exceptions.NotFoundException nfe),

    RefundSlipDetail initiate_refund_operation(
        1: i64 refund_slip_id, 2: order_after_sale.RefundOperateType operate,
        3: i32 staff_id, 4: optional order_after_sale.RefundMethod method,
        5: optional i32 refund_amount, 6: optional string user_name,
        7: optional string account_num)
        throws(1: exceptions.NotFoundException nfe,
        2: exceptions.InternalException ie),

    order_after_sale.ReturnOrderList get_return_orders(
        1: i64 start_index, 2: i16 limit, 3: string start_time,
        4: string end_time, 5: i16 region, 6: list<i16> status,
        7: optional i64 account_id, 8: optional string code_or_id),

    order_after_sale.ReturnOrderListRelated initiate_return_order_operation(
        1: i64 return_order_id, 2: order_after_sale.ReturnOperateType operate,
        3: i32 staff_id)throws(1: exceptions.NotFoundException nfe),

    order_after_sale.RepairOrderList get_repair_orders(
        1: i64 start_index, 2: i16 limit, 3: string start_time,
        4: string end_time, 5: i16 region, 6: list<i16> status,
        7: optional i64 account_id, 8: optional string code_or_id),

    order_after_sale.RepairOrderListRelated initiate_repair_order_operation(
        1: i64 repair_order_id, 2: order_after_sale.RepairOperateType operate,
        3: i32 staff_id, 4: optional string repair_des,
        5: optional i16 cost_amount)throws(1: exceptions.NotFoundException nfe),

    order_after_sale.RepairOrderDetail get_repair_order_detail(
        1: i64 repair_order_id) throws(1: exceptions.NotFoundException nfe),

    order_after_sale.DeliveryOrderList get_delivery_orders(
        1: i64 start_index, 2: i16 limit, 3: string start_time,
        4: string end_time, 5: i16 region, 6: list<i16> status,
        7: optional i64 account_id, 8: optional string code_or_id),

    order_after_sale.DeliveryOrderListRelated initiate_delivery_order_operation(
        1: i64 delivery_order_id, 2: order_after_sale.DeliveryOperateType operate,
        3: i32 staff_id, 4: optional string terminal_delivery_code,
        5: optional i16 terminal_delivery_id)
        throws(1: exceptions.NotFoundException nfe),

    order_after_sale.DeliveryOrderDetail get_delivery_order_detail(
        1: i64 delivery_order_id) throws(1: exceptions.NotFoundException nfe),

    list<order_after_sale.AfterSaleWay> get_optional_after_sale_methods(
    1: i64 order_id, 2: order_after_sale.ApplyScale apply_scale,
    3: order_after_sale.AfoInitiator initiator,
    4: optional order_after_sale.AfoOrigin origin,
    5: optional OrderType order_type) throws(1: exceptions.NotFoundException nfe),

    list<order_after_sale.AfterSaleReason> get_optional_after_sale_reasons(
    1: i64 order_id, 2: order_after_sale.AfoInitiator initiator,
    3: optional order_after_sale.AfoOrigin origin,
    4: optional OrderType order_type) throws(1: exceptions.NotFoundException nfe),

    Tax calculate_taxes(
    1: i16 region, 2: list<OrderItem> sku_items, 3: i32 redeem,
    4: optional list<Voucher> vouchers, 5: optional i32 discount),

    order_constants.OrderOperateLog add_order_operate_log(
    1: i64 so_id, 2: order_constants.OrderOperateCode operate,
    3: order_constants.OrderOperator operator, 4: i64 operator_id,
    5: optional i64 package_id) throws(1: exceptions.NotFoundException nfe,
    2: exceptions.InvalidOperationException ioe),

    list<order_constants.OrderOperateLog> get_order_operate_log(
    1: i64 so_id, 2: optional i64 package_id),

    void receipt_domestic_transfer(
    1: i64 package_id, 2: order_constants.OrderOperator operator,
    3: i64 operator_id),

    void print_express_order_domestic_transfer(
    1: i64 package_id, 2: order_constants.OrderOperator operator,
    3: i32 operator_id, 4: bool is_confirm_receive),

    order_constants.CountAndGMV count_store_order_and_gmv(
    1: string start_time, 2: string end_time, 3: i32 store_id,
    4: optional i16 region_id)throws(
    1: exceptions.InvalidOperationException ioe),

    void specify_orders_promotion_platform(
        1: set<order_constants.OrderPlatform> platform_orders),

    list<order_constants.SaleOrderDetail> get_user_order_detail_li(
        1: i64 account_id, 2: i32 skip, 3: i32 limit,
        4: optional i16 region_id),

    order_constants.AccountOrder get_account_order_count_info(1: i64 account_id),

    map<i64, i32> get_skus_history_min_price(1: set<i64> sku_ids, 2: i16 region_id),

    order_constants.OrderPackege get_reject_order_info(
        1: optional i64 so_id, 2: optional string so_code, 3: optional i64 pg_id,
        4: optional string pg_code),

    order_constants.OrderPackege get_return_order_info(
        1: optional i64 so_id, 2: optional string so_code, 3: optional i64 pg_id,
        4: optional string pg_code),

    order_constants.OrderPackege get_order_package_info(1: optional i64 pg_id) throws(
        1: exceptions.NotFoundException nfe),

    order_constants.ClearingStatisticList get_clearing_statistics(
        1: i32 store_id, 2: string start_time, 3: string end_time,
        4: optional i32 skip, 5: optional i32 limit, 6: optional i16 region_id),

    order_constants.SummaryOrderStatistics get_summary_clearing_statistics(
        1: i32 store_id, 2: string start_time, 3: string end_time,
        4: optional i16 region_id),

    order_after_sale.RefundDetail get_refund_details(
        1: order_after_sale.RefundSource source_type, 2: i64 source_id) throws(
        1: exceptions.NotFoundException nfe),

    void refund_transaction(
        1: bool is_reviewed, 2: i64 refund_id, 3: i64 bill_id,
        4: i32 refund_amount, 5: string refund_reason, 6: optional i64 so_id,
        7: optional i64 sku_id, 8: optional i32 delivery_times) throws(
        1: exceptions.InternalException ie,
        2: exceptions.NotFoundException nfe,
        3: exceptions.InvalidOperationException ioe),

    order_after_sale.RefundApiRes get_refund_status_by_api(1: i64 refund_slip_id)
    throws(1: exceptions.NotFoundException nfe,
        2: exceptions.InternalException ie),

    list<order_constants.ActivityIdCount> get_sold_sku_count(
    1: order_constants.PromotionType activity_type, 2: list<i64> activity_ids),

    order_constants.MiniSaleOrders get_mini_sales_orders(
        1: optional set<order_constants.SaleOrderStatus> state,
        2: optional i32 skip, 3: optional i32 limit, 4: optional i32 store_id,
        5: optional bool only_get_total=false, 6: optional i16 region_id),

    order_constants.MiniShipOrders get_mini_ship_orders(
        1: optional set<order_constants.ShipOrderStatus> state,
        2: optional i32 skip, 3: optional i32 limit, 4: optional i32 store_id,
        5: optional bool only_get_total=false, 6: optional i16 region_id),

    void close_store_effect(1: i32 store_id, 2: set<i16> region_ids),

    order_constants.OnePackage get_ship_package(
        1: order_constants.QueryPackageSource source, 2: string source_code),

    order_constants.SagawaLabel get_sagawa_label_info(
        1: order_constants.Courier delivery_id,
        2: order_constants.PackageType package_type, 3: i64 package_id),

    list<order_constants.SaleOrder> get_fault_orders(
        1: string start_time, 2: string end_time, 3: i16 fault_id),

    order_constants.XedUser xed_user_verification(
        1: required string account,
        2: required string intl_tel_code,
        3: required string phone_number,
        4: optional string password
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.NotFoundException nfe
    )

    order_constants.XedUser xed_create_user(
        1: required string account,
        2: required string name,
        3: required string intl_tel_code,
        4: required string phone_number,
        5: required string password
    ) throws (
        1: exceptions.InvalidOperationException ioe
    )

    order_constants.XedUser xed_create_user_store(
        1: required i64 xed_user_id,
        2: required i64 store_id,
        3: required string store_name,
        4: required order_constants.XedAddress en_shipping_address
        5: required order_constants.XedAddress zh_shipping_address
    ) throws (
        1: exceptions.InvalidOperationException ioe
    )

    list <order_constants.XedStore> xed_get_user_stores (
        1: required i64 xed_user_id
    ) throws (
        1: exceptions.InvalidOperationException ioe
    )

    order_constants.XedUser xed_get_store_user(
        1: required i64 store_id,
    ) throws (
        1: exceptions.InvalidOperationException ioe
        2: exceptions.NotFoundException nfe
    )

    order_constants.XedUser xed_update_shipping_address(
        1: required i64 xed_user_id,
        2: required i64 store_id,
        3: required order_constants.XedAddress en_shipping_address
        4: required order_constants.XedAddress zh_shipping_address
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    void cancel_x_ed_order(
        1: optional i64 package_id,
        2: optional i32 so_id)throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),

    order_constants.XedOrder get_logistics_xed_order(
        1: optional i32 so_id,
        2: optional i32 package_id)throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),

    order_constants.WarehousingOrders get_warehousing_orders(
        1: order_constants.WarehousingOrdersTimeType time_type,
        2: optional string start_time, 3: optional string end_time,
        4: optional string so_param, 5: optional list<i32> store_ids,
        6: optional list<i32> account_ids, 7: optional i32 status,
        8: optional i64 start_index, 9: optional i32 limit),

    void rejected_order_storage(
        1: i64 package_id, 2: i32 operator_id,
        3: order_constants.StorageSourceType source_type,
        4: list<order_constants.WarehousingSku> sku_li),

    order_constants.WarehousingOrder get_warehousing_order(
        1: optional i64 package_id, 2: optional i64 so_id),

    list<order_constants.OrderRelated> get_state_changed_orders(
        1: string start_time, 2: string end_time,
        3: optional list<order_constants.SaleOrderStatus> operations
    )

    order_constants.WmsAccount create_wms_account(
        1: required i64 xed_account_id,
    )throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),

    order_constants.WmsAccount get_wms_account(
        1: required i64 xed_account_id,
    )throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),


    order_constants.PagingWmsStore get_wms_store_bindings(
        1: required i64 xed_account_id,
    )throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),

    void create_wms_store_binding(
        1: required string partner,
        2: required string store_id,
        3: required string store_name,
        4: required string logo,
        5: required string xed_account_id,
        6: required string refresh_token,
    )throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),

    order_constants.PagingWmsWarehouse get_wms_warehouses(
        1: required i64 xed_account_id,
        2: optional i64 skip,
        3: optional i64 limit,
    )throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),

    order_constants.PagingWmsWarehouseApplication get_wms_warehouse_applications(
        1: required i64 xed_account_id,
        2: required i64 warehouse_id,
        3: optional i64 skip,
        4: optional i64 limit,
    )throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),

    void create_wms_warehouse_application(
        1: required i64 xed_account_id,
        2: required i64 warehouse_id
    )throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe),

    OneShipPackage update_ship_package_subsequent(
        1: i32 package_id,
        2: i16 subsequent_action,
        3: optional list<string> stock_receiving_ids) throws(
            1: exceptions.NotFoundException nfe,
            2: exceptions.InvalidOperationException ioe),

}
