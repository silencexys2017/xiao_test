const string SELLER_REJECT_MSG = "The seller rejected your aftersale request and the case automatically escalated to intervention by platform. Please wait for the final solution given by platform."
const string PLATFORM_REJECT_MSG = "The platform has rejected your after-sale application, if you need, send an email to support@perfee.com to appeal."
// 售后发起者 (1:admin, 2:user)
enum AfoInitiator {
    ADMIN = 1,
    USER = 2
}
// 售后方式 (1: 换货，2：退货并退款，3：维修，4：退款，5：补发)
enum AfterSaleWay {
    RETURN_DELIVERY = 1,// 换货
    RETURN_REFUND = 2, // 退货并退款
    REPAIR = 3, // 维修
    REFUND = 4, // 退款
    DELIVERY = 5 // 补发
}
const list<i16> REFUND_METHOD = [AfterSaleWay.RETURN_REFUND, AfterSaleWay.REFUND]
// 申请来源类型(1:app, 2:wap, 3:email, 4:facebook)
enum AfoOrigin {
    APP = 1,
    WAP = 2,
    EMAIL = 3,
    FACEBOOK = 4,
    PHONE = 5
}
// 申请维度(1: order，2：sku, 3: bill)
enum ApplyScale {
    ORDER = 1, // saleOrder
    SKU = 2,
    BILL = 3,
    SHORTAGE = 4
}
// 运费承担者 (1: 平台，2：卖家，3：用户)
enum PostageBurden {
    PLATFORM = 1,
    SELLER = 2,
    USER = 3
}
enum RefundMethod {
    ORIGINAL_ROAD = 1,
    BKASH = 2,
    BANK_CARD = 3,
    VOUCHER = 4
}

enum RefundOperateType {
    REVIEW = 1,
    START = 2,
    COMPLETE = 3
}

enum ReturnOperateType {
    RECEIPT = 1,
    CHECK_SUCCESS = 2,
    CHECK_FAIL = 3
}

enum RepairOperateType {
    START = 1,
    REPAIR_SUCCESS = 2,
    REPAIR_FAIL = 3
}

enum DeliveryOperateType {
    SHIP = 1,
    DISPATHCH = 2,
    DELIVERY = 3
}

enum ReviewResult {
    PASS = 1,
    REJECT = 2
}

enum ReceiveStandard {
    RESALE = 1,
    REPAIR = 2,
    NON_HUMAN_QUALITY = 3
}

enum AfterSaleReason {
    QUALITY_ISSUES = 1,
    DELIVERY_DAMAGED = 2,
    SHODDY_VERSION = 3
}
enum WorkOrderState {
    NOT_STARTED = 1,
    IN_PROGRESS = 2,
    COMPLETE = 3
}
enum WorkOrderType {
    RETURN = 1,
    REPAIR = 2,
    DELIVERY = 3,
    REFUND = 4
}
enum OrderCloseType {
    COMPLETED = 1,
    REJECTED = 2
}

enum RefundType {
    AFTER_SALE = 1,
    CANCEL_ORDER = 2,
    REJECT_ORDER = 3,
    OUT_OF_STOCK = 4
}

const map<i16, string> REFUND_REASON = {
1: "AfterSaleRefund", 2: "CancelOrder", 3: "RejectOrder", 4: "OutOfStock"}

enum RefundSource {
    AFTER_SALE = 1,
    SALE_ORDER = 2,
    BILL = 3
}

struct ShipOrderDetailRelated {
    1: required string saleOrderCode,
    2: required string transactionCloseAt,
    3: required i64 shipOrderDetailId,
    4: required i64 shipOrderId,
    5: required i64 skuId,
    6: required i16 count,
    7: required i64 salePrice,
    8: required i64 dealPrice,
    9: optional i32 voucherRedeem,
    10: optional i32 coinRedeem,
    11: optional i32 discount,
    12: optional i32 amountPaid,
    13: optional string createdAt, // saleOrder
    14: optional string paidAt // bill
}

struct SimpleAfterSaleOrder {
    1: required i64 afterSaleOrderId,
    2: required string createdAt,
    3: required i64 skuId,
    4: required i16 count,
    6: required i64 salePrice,
    7: required i64 dealPrice,
    8: required i16 afterSaleMethod,
    9: required i16 status
}
enum AfterSaleStatus {
    pending_sl_review = 1,
    pending_pf_review = 2,
    processing = 3,
    complete = 4,
    sl_rejected = -1,
    pf_rejected = -2,
    cancel = -3
}

enum RefundSlipStatus {
    new_create = 1, // 在AfterSaleOrder中表示为待生成
    pending_review = 2,
    pending_refund = 3,
    in_refund = 4,
    complete = 5,
    no = 0
}

struct AfterSaleOrder {
    1: required i64 afterSaleOrderId,
    2: required i64 accountId,
    3: required i16 region,
    4: required i64 saleOrderId,
    5: required i64 shipOrderId,
    6: optional i64 shipOrderDetailId,
    7: optional i64 skuId,
    8: optional i16 count,
    9: optional i64 salePrice,
    10: optional i64 dealPrice,
    11: required i32 voucherRedeem,
    12: required i32 coinRedeem,
    13: required i32 coin,
    14: required i32 discount,
    15: required OrderCloseType orderCloseType,
    16: required i32 payAmount, // 实付金额
    17: required i32 refundAmount, // 退款金额
    18: required i16 reason, // (1: 质量问题，2：送达时损坏，3：货不对版)
    19: required string reasonDetail,
    20: required list<string> images,
    21: required AfoInitiator initiator,
    22: required AfoOrigin origin,
    23: required i16 status, // (1: 待商家审核，2：待平台审核，3：处理中，4：售后完成, -1: 商家拒绝， -2：平台拒绝, -3: 用户取消)
    24: required ApplyScale applicationScale,
    25: required AfterSaleWay afterSaleMethod, // (1: 换货，2：退货并退款，3：维修，4：退款，5：补发)
    26: required PostageBurden postageBurden,
    27: required string accountSource, // fb匿称、电话、邮件地址,根据origin
    28: required i32 staffId,
    29: optional RefundSlipStatus refundStatus, // (0: 无， 1：待生成，2:待审核，3：待退款 4：退款中，5：已退款)
    30: required string createdAt,
    31: optional string sellerVerifiedAt,
    32: optional string verifiedAt,
    37: optional string completedAt,
    38: optional WorkOrderType inProcess,
    39: optional i32 vat,
    40: optional i32 storeId,
    41: optional bool isAppeal,
    42: optional string videoName
}
struct WorkOrderDetail{
    1: optional string receiver,
    2: optional string address,
    3: optional string phone,
}

struct WorkOrder {
    1: required WorkOrderType woType,
    2: required i64 id,
    3: required i16 status,
    4: required WorkOrderState processState,
    5: required WorkOrderDetail detail
}

struct AfterSaleOrderDetail {
    1: required AfterSaleOrder afterSaleOrder,
    2: optional WorkOrder workOrder
}

struct AfterSaleOrderListRelated {
    1: required AfterSaleOrder afterSaleOrder,
    2: required string orderClosedAt,// so or sho
    3: required i32 orderAmount, // so
    4: required i32 payAmount // so
}

struct AfterSaleOrderList {
    1: required i64 orderCount,
    2: required list<AfterSaleOrderListRelated> afterSaleOrders
}

struct UserTranOrder {
    1: required i32 orderBatchCount,
    2: required i32 saleOrderCount,
    3: optional i32 completeCount,
    4: optional i32 rejectCount,
    5: required i32 afterSaleCount,
    6: required i32 soAfterSaleCount
}
enum ReturnOrderStatus {
    new_create = 1,
    pending_receipt = 2,
    pending_inspection = 3,
    complete = 4,
    failure = 5
}
struct ReturnOrder{
    1: required i64 returnOrderId,
    2: required i64 accountId,
    3: required i16 region,
    4: required i64 afterSaleOrderId,
    5: required i64 saleOrderId,
    6: required i64 skuId,
    7: required i32 count,
    8: required WorkOrderState processState,
    9: required AfterSaleWay afterSaleMethod,
    10: required i16 standard, // (1: 可二次销售， 2：维修要求，3：非人为损坏的质量问题[退货并退款{质量问题}，换货{质量问题}])
    11: required i16 status, // （1:新创建，2：待收货，3：待验货，4：取货完成，5：验货失败）
    12: required WorkOrderType nextOperate, // (0:无, 1:退货，2: 维修，3: 送货，4：退款)
    13: required i32 consigneeId,
    14: required i32 inspectorId,
    15: required string createdAt,
    16: required string effectedAt,
    17: optional string receivedAt,
    18: optional string completedAt,
    19: optional string failedAt,
    20: optional i32 sellerAddressId,
}
enum DeliveryOrderStatus {
    new_create = 1,
    pending_ship = 2,
    shipped = 3,
    dispatch = 4,
    arrived = 5
}
struct DeliveryOrder {
    1: required i64 deliveryOrderId,
    2: required i64 afterSaleOrderId,
    3: required i64 saleOrderId,
    4: required i64 addressId,
    5: required i64 skuId,
    6: required i32 count,
    7: required i64 accountId,
    8: required i16 status,//（1: 新创建，2: 待发货，3：已发货，4：派送中，5：已送达）
    9: required WorkOrderState processState,
    10: required AfterSaleWay afterSaleMethod,
    11: required WorkOrderType nextOperate, // (0:无, 1:退货，2: 维修，3: 送货，4：退款)
    12: required i32 operatorId,
    13: required i16 region,
    14: required string terminalDeliveryCode,
    15: required string createdAt,
    16: optional string effectedAt,
    17: optional string shippedAt,
    18: optional string dispatchedAt,
    19: optional string deliveredAt,
    20: optional i16 terminalDeliveryId,
    21: optional i32 amount // 这个订单价值amount(包括postage)
}
enum RepairOrderStatus {
    new_create = 1,
    pending_handle = 2,
    in_repair = 3,
    repaired = 4,
    cnt_fix = 5
}
struct RepairOrder {
    1: required i64 repairOrderId,
    2: required i64 accountId,
    3: required i64 saleOrderId,
    4: required i64 skuId,
    5: required i32 count,
    6: required i64 afterSaleOrderId,
    7: required WorkOrderState processState,
    8: required i16 status,// （1:新创建，2：待处理，3：维修中，4：已修复，5：无法修复）
    9: required AfterSaleWay afterSaleMethod,
    10: required WorkOrderType nextOperate,
    11: optional i16 repairerId,
    12: optional string details,
    13: optional i32 cost,
    14: required i16 region,
    15: required string createdAt,
    16: optional string effectedAt,
    17: optional string startedAt,
    18: optional string completedAt,
}

enum RefundWay {
    AUTO = 1,
    MANUAL = 2
}

struct RefundSlip {
    1: required i64 refundSlipId,
    2: required i64 accountId,
    3: optional i64 afterSaleOrderId,
    4: required i16 payMethod,
    5: required ApplyScale applicationScale,
    6: required i64 billId,
    7: optional i64 saleOrderId,
    8: optional i64 skuId,
    9: optional i32 count,
    10: required i32 amount, // 退款额里展示的是 审核时 确认的退款额,可更改
    11: required AfterSaleWay afterSaleMethod,
    12: required RefundSlipStatus status,// (1:新创建， 2: 待审核，3：待退款，4：退款中，5：退款完成)
    13: required i16 region,
    14: optional i32 reviewerId,
    15: optional i32 refunderId,
    16: optional WorkOrderState processState,
    17: optional RefundMethod refundMethod, // (1:原路退回，2: bkash, 3: 银行卡，4：退为无门槛长期券)
    18: optional string userName,
    19: optional string accountNum,
    20: required string createdAt,
    21: optional string effectedAt,
    22: optional string confirmedAt,
    23: optional string initiatedAt,
    24: optional string refundedAt,
    25: optional RefundType refundType,  // (1:售后， 2：取消， 3: 用户拒收 4：缺货)
    26: optional i64 shortageOrderId,
    27: optional bool isNeedCheck,
    28: optional i32 storeId,
    29: optional RefundWay refundWay
}

struct RelatedWorkOrder {
    1: optional ReturnOrder returnOrder,
    2: optional DeliveryOrder deliveryOrder,
    3: optional RepairOrder repairOrder
    4: optional RefundSlip refundSlip
}
struct SimpleSo {
    1: required i64 saleOrderId,
    2: required i32 payAmount,
    3: required i32 postage,
    4: required i32 vat
}

struct AfterSaleAppeal {
    1: i64 afterSaleOrderId,
    2: string complainant,
    3: i32 complainantId,
    4: string description,
    5: i16 status,
    6: string appealedAt
}

struct AfterSaleOrderRelated {
    1: required AfterSaleOrder afterSaleOrder,
    2: required UserTranOrder userTranOrder,
    3: required RelatedWorkOrder workOrders,
    4: required SimpleSo saleOrder,
    5: optional AfterSaleAppeal appeal
}

struct SellerAfterSaleLog {
    1: required i64 sellerAfterSaleLogId,
    2: required i64 storeId,
    3: required i64 afterSaleOrderId,
    4: required AfterSaleWay applicationWay,
    5: required AfterSaleWay confirmWay,
    6: required ReviewResult status,
    7: required i64 accountId,
    8: required string createdAt,
    9: required PostageBurden postageBurden,
    10: required i32 refundAmount,
    11: required i32 staffId
}

struct PlatformAfterSaleLog {
    1: required i64 sellerAfterSaleLogId,
    2: required i64 id,
    3: required i64 afterSaleOrderId,
    4: required i16 applicationWay,
    5: required i16 confirmWay,
    6: required ReviewResult status,
    7: required i64 accountId,
    8: required string createdAt,
    9: required PostageBurden postageBurden,
    10: required i32 refundAmount,
    11: required i32 staffId,
    12: required bool isPaid
}

struct RefundSlipListRelated {
    1: required RefundSlip refundSlip,
    2: required string saleOrderCode,
    3: i16 saleOrderStatus
}

struct RefundSlipList {
    1: required i64 count,
    2: required list<RefundSlipListRelated> refundSlips
}

struct ReturnOrderListRelated {
    1: required ReturnOrder returnOrder,
    2: required string saleOrderCode
}

struct ReturnOrderList {
    1: required i64 count,
    2: required list<ReturnOrderListRelated> returnOrders
}

struct RepairOrderListRelated {
    1: required RepairOrder repairOrder,
    2: required string saleOrderCode
}

struct RepairOrderList {
    1: required i64 count,
    2: required list<RepairOrderListRelated> repairOrders
}

struct DeliveryOrderListRelated {
    1: required DeliveryOrder deliveryOrder,
    2: required string saleOrderCode
}

struct DeliveryOrderList {
    1: required i64 count,
    2: required list<DeliveryOrderListRelated> deliveryOrders
}

struct RepairOrderDetail {
    1: required AfterSaleOrder afterSaleOrder,
    2: required RepairOrder repairOrder
}

struct DeliveryOrderDetail {
    1: required DeliveryOrder deliveryOrder,
    2: required string saleOrderCode
}

struct RefundDetail {
    1: string orderSerial,
    2: i64 refundSlipId,
    3: RefundSlipStatus refundStatus,
    4: RefundMethod refundChannel,
    5: RefundWay refundWay,
    6: string refundAccount,
    7: string createdAt,
    8: optional i64 afterSaleOrderId
}

enum RefundState {
    NO = 1,
    YES = 2,
    PROCESSING = 3
}

struct RefundApiRes {
    1: i64 amount,
    2: RefundMethod refundMethod,
    3: RefundState refundState,
    4: i64 billId,
    5: string message
}


