# 收件详单状态
enum ReceiptDetailStatus {
    PENDING = 1,  #待收件
    RECEIVED = 2,  #已收件
    PROBLEM = 3,  #问题件
    INVALID = -1  #已作废
}

# 收件单状态
enum ReceiptStatus {
    PENDING = 1,  #待集件
    RECEIVING = 2,  #集件中
    COMPLETED = 3,  #集件完成
}

# 问题类型
enum ReceiptProblemType {
    LOST = 1,  #缺件
    DAMAGE = 2,  #损坏
    NOT_MATCH = 3,  #不符
    OTHER = 4  #其他
}

# 是否带电
enum WithBatteryStatus {
    no = 0,  # 不带电
    yes = 1,  # 全部带电
    partially = 2  # 部分带电
}

# 支付方式
enum PaymentMethods {
    ONLINE = 1,  # 在线
    COD = 2,  # 货到付款
    PRE = 3  # 预付部分
}

enum AllocateState {
    unallocated = 1,
    allocated = 2
}

enum ProblemType {
    missingPackage = 1,
    damagePackage = 2,
    other = 3
}
enum ConfirmState {
    unconfirm = 1,
    confirmed = 2,
    problem = 3
}
enum OperateType {
    create = 1,
    update = 2,
    remove = 3
}
enum BoxType {
    scatterOrders = 1,
    stock = 2
}
enum DeliveryBatchState {
    penddingSortOut = 1,
    pendingPackage = 2,
    transitWarehouseDelivery = 3,
    logisticsChannelDelivery = 4,
    penddingClearance = 5,
    customsClearing = 6,
    clearanceCompleted = 7,
    locallyReceived = 8
}
enum EpTimeType {
    orderTime = 1,
    confimTime = 2,
    shipTime = 3,
    receiveTime = 4
}
enum EpStatus {
    pendingReceipt = 1,
    pendingPrintOrder = 2,
    deliveryLead = 3,
    problemPackage = -1,
    overdue = -2
}
enum EpState {
    pendingShip = 1
    pendingReceipt = 2,
    pendingPrintOrder = 3,
    deliveryLead = 4,
    problemPackage = -1
}
const set<i16> ep_status = [-1, 1, 2, 3]
const map<i16, list<i16>> ep_state_map = {-1: [-1], 1: [1, 2], 2: [3], 3: [4]}
enum RrStatus {
    normal = 1,
    abnormal = 2
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
struct ReceivingLog {
    1: i64 id,
    2: i16 operatorId,
    3: ConfirmState confirmState,
    4: string createdAt,
    5: i64 expressPackageId
}
struct ProblemPackage {
    1: i64 id,
    2: ProblemType problemType,
    3: string createdAt,
    4: string remark,
    5: i64 expressPackageId,
    6: i16 creatorId
}
struct ExpressPackage {
    1: required i64 id,
    2: required i64 packageId,
    3: required i16 regionId,
    4: required i64 addressId,
    5: required i64 accountId,
    6: required EpState status,
    7: required i32 tranWareId,
    8: optional i16 deliveryId,
    9: optional string deliveryCode,
    10: optional i64 saleOrderId,
    11: optional string saleOrderCode,
    12: optional i64 storeId,
    13: optional i32 itemCount,
    14: optional string soCreatedAt,
    15: optional string confirmedAt,
    16: optional string createdAt,
    17: optional string shippedAt,
    18: optional string receivedAt,
    19: optional string printedAt,
    20: optional i32 shipOperatorId,
    21: optional i64 receiveOperatorId,
    22: optional i32 printOperatorId,
    23: optional string preLocation,
    24: optional string receivingLocation,
    25: optional ConfirmState confirmState,
    26: optional i64 deliveryBatchId
    27: optional i64 boxId
}

struct ExpressPackageList {
    1: required i64 count,
    2: required list<ExpressPackage> packages
}

struct Sku {
    1: required i64 skuId,
    2: required i32 count,
    3: required i64 price
}

struct ReceivingRecord {
    1: required i64 id,
    2: required i64 packageId,
    3: required i32 receiveOperatorId,
    4: required RrStatus status,
    5: required string receivedAt,
    6: optional string receivingLocation,
    7: optional i64 saleOrderId
}

struct ProblemProduct {
    1: required i64 id,
    2: required i64 recordId,
    3: required i64 packageId,
    4: required i64 skuId,
    5: required i32 count,
    6: required i64 price,
    7: required string createdAt
}
enum EnableSwitch {
    enable = 1,
    disable = -1,
    all = 0
}
enum ProductNature {
    common = 1,
    withBattery = 2,
    withMagnetic = 3,
    Powder = 4,
    compressor = 5,
    liquid = 6
}
const set<i16> ComTrWhNature = [1]
const set<i16> SpeTrWhNature = [2, 3, 4, 5]
struct TransferWarehouse {
    1: i16 id,
    2: string location,
    3: string name,
    4: string contact,
    5: string phone,
    6: EnableSwitch status,
    7: list<i16> supportedLogistics,
    8: list<i16> regions,
    9: list<i16> supportNatures,
    10: string address,
    11: optional string createdAt
}

struct HeadTransportChannel {
    1: i16 id,
    2: string location,
    3: string name,
    4: string contact,
    5: string phone,
    6: EnableSwitch status,
    7: list<i16> regions,
    8: list<i16> supportNatures,
    9: optional string createdAt
}

struct Box {
    1: i64 id,
    2: string name,
    3: i16 creatorId,
    4: BoxType type,
    5: bool confirmed,
    6: i16 packageTotal,
    7: i16 confirmedPackageNum,
    8: i16 confirmedorId,
    9: i64 deliveryBatchId,
    10: list<i64> expressPackageIds,
    11: optional string createdAt,
    12: optional string confirmedAt
}

struct DeliveryBatch {
    1: i64 id,
    2: i16 transferWarehouseId,
    3: i16 headTransChannelId,
    4: i16 destinationCountryId,
    5: list<i64> boxIds,
    6: DeliveryBatchState state,
    7: i32 numOfboxes,
    8: i16 confirmedBoxNum,
    9: bool isAlive,
    10: optional string createdAt,
    11: optional string remark
}

struct DeliveryBatchLog {
    1: i64 id,
    2: i16 operatorId,
    3: OperateType operateType,
    4: DeliveryBatchState newState,
    5: string dateTime,
    6: i64 deliveryBatchId,
    7: optional string remark
}

struct BoxLog {
    1: i64 id,
    2: i16 operatorId,
    3: OperateType operateType,
    4: i64 boxId,
    5: string boxName,
    6: string dateTime,
    7: i64 deliveryBatchId
}

struct DeliveryBatchs {
    1: i64 total,
    2: list<DeliveryBatch> deliveryBatchs,
    3: optional Box box
}

# 收件详单
struct ReceiptOrderDetail {
    1: i64 id,
	2: i32 regionId,
    3: i64 receiptOrderId,
    4: i64 receivableOrderId,
    5: i64 saleOrderId,
    6: i64 storeId,
    7: i64 accountId,
    8: string trackingNumber,  #供应商运单号
    9: i64 skuId,
    10: string skuTitle,
    11: string skuSpec,
    12: i16 receivableQty,  #应收商品数量
    13: i16 pendingQty,  #待收商品数量
    14: i16 receivedQty,  #已收商品数量
    15: i16 problemQty,  #问题商品数量
    16: string inputTime,  #录入时间/创建时间
    17: ReceiptDetailStatus status,  #状态：1.待收件 2.已收件 3.问题件 -1.已作废
    18: string senderContact, #发货人联系方式
    19: i64 inputOperatorId,  #录入操作员ID
    20: optional i64 receiverOperatorId,  #收件操作员ID
    21: optional string problemRemark,  #问题商品描述
    22: optional ReceiptProblemType problemType, #问题类型
}

# 应收详单
struct ReceivableOrder {
    1: i64 id,
	2: i32 regionId,
    3: i64 receiptOrderId,
    4: i64 saleOrderId,
    5: i64 saleOrderDetailId,
    6: i64 storeId,
    7: i64 accountId,
    8: i64 skuId,
    9: string skuTitle,
    10: string skuSpec,
    11: i16 receivableQty,  #应收商品数量
    12: i16 pendingQty,  #待收商品数量
    13: i16 receivedQty,  #已收商品数量
    14: i16 problemQty,  #问题商品数量
    15: string inputTime,  #录入时间/创建时间
    16: i64 inputOperatorId,  #录入操作员ID
}

# 发件地址
struct SenderAddress {
	1: string regionName,
	2: string regionCode,
    3: string name,
    4: string phone,
    5: string provinceCity,
    6: string detail
}
# 收件地址
struct DeliveryAddress {
	1: i64 id
	2: string regionName,
	3: string regionCode,
	4: string name,
	5: string phone,
	6: string state,
	7: string city,
	8: string area,
	9: string address1,
	10: optional string address2,
}

# 收件单
struct ReceiptOrder {
    1: i64 id,  # 收件单ID
	2: i32 regionId,  # 国家/地区ID
    3: i64 saleOrderId,  # Sale Order订单ID
    4: WithBatteryStatus withBattery,  # 是否带电，0.不带点 1.带电 2.部分带电
    5: bool isMagnetic,  # 是否带磁性
    6: bool isPowder,  # 是否为粉末
    7: bool isCompressor,  # 是否压缩
    8: PaymentMethods payMethod,  # 支付方式，1.在线 2.货到付款 3.预付部分
    9: i32 payAmount,  # 实际所要支付的订单金额
    10: i64 storeId,  # 店铺ID
    11: string storeName,  # 店铺名称
    12: i64 accountId,   # 用户ID
    13: ReceiptStatus status,  #状态：1.待集件 2.集件中 3.集件完成
    14: i16 receivableOrders,  #应收订单数
    15: i16 pendingOrders,  #待收订单数
    16: i16 receivedOrders,  #已收订单数
    17: i16 problemOrders,  #问题订单数
    18: i16 pendingDetailsCount, #进行中收件详情数
    19: i16 problemDetailsCount, #问题收件详情数，问题数增加时，同时减去进行中数
    20: string orderCreateTime,  #订单创建时间
    21: string createTime,  #创建时间
    22: DeliveryAddress address, #用户收货地址
    23: SenderAddress senderAddress, #发货地址
    24: i64 inputOperatorId,  #录入操作员ID
    25: optional string firstArrivalTime,  #初次到件时间
    26: optional string receiptUpdateTime,  #收件更新时间
    27: optional string completedTime,  #集件完成时间
    28: optional string printedTime,  #打印标签时间
    29: optional list<ReceivableOrder> receiveList,  #应收详单列表
    30: optional bool liquid,  # 是否为液体
#    20: optional list<ReceiptOrderDetail> detailList
}


struct PagingReceiptOrderDetail{
    1: required i32 total,
    2: required list<ReceiptOrderDetail> data
}


struct PagingReceiptOrder{
    1: required i32 total,
    2: required list<ReceiptOrder> data
}

# 批量操作统计
struct BatchResult{
    1:i16 total,
    2:i16 success,
    3:i16 failed
}

# 批量操作详情
struct BatchDetail{
    1:string resourceId,
    2:i16 code,
    3:optional string msg
}

# 批量操作返回值
struct BatchOperation{
    1:BatchResult result,
    2:list<BatchDetail> details
}

# 接口入参：问题详情
struct ProblemDetailCondition{
    1:i64 detailId,
    2:i16 problemQty,
    3:ReceiptProblemType problemType,
    4:optional string problemRemark
}

struct InputPurchaseOrderCondition{
    1:i32 regionId,
    2:i64 skuId,
    3:i64 saleOrderId,
    4:i32 qty,
    5:string trackingNumber,
    6:optional string senderContact
}
