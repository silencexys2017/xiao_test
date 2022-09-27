const i32 GEN_STATUS_AUDIT_UNAUDITED = 0
const i32 GEN_STATUS_AUDITED = 1
const i32 GEN_STATUS_AUDIT_FAILED = 2
const i32 GEN_STATUS_ONLINE = 3
const i32 GEN_STATUS_OFFLINE = 4
const i32 STATUS_NOT_USE = 1
const i32 STATUS_USED = 2
const i32 STATUS_EXPIRED = 3
const i32 STATUS_INVALID = 4

const i32 GEN_TYPE_VOUCHER_CENTER = 1
const i32 GEN_TYPE_DISTRIBUTE = 2
const i32 GEN_TYPE_DISTRIBUTE_USED = 3
const i32 GEN_TYPE_SYSTEM = 4

const i32 DIS_TYPE_ADMIN = 1
const i32 DIS_TYPE_AUTO = 2
const i32 RULE_ACCOUNT_TYPE_NEW = 1
const i32 RULE_ACCOUNT_TYPE_ORDER = 2
const i32 RULE_ACCOUNT_TYPE_COMPLETE = 3
const i32 RULE_ACCOUNT_TYPE_ONLINE_PAIED = 4
const i32 RULE_ACCOUNT_TYPE_ONLINE_COMPLETE = 5
const i32 DIS_STATUS_AUDIT_UNAUDITED = 0
const i32 DIS_STATUS_AUDITED = 1
const i32 DIS_STATUS_AUDIT_FAILED = 2
const i32 DIS_STATUS_ONLINE = 3
const i32 DIS_STATUS_OFFLINE = 4
const i32 OWNER_TYPE_PLATFORM = 1
const i32 OWNER_TYPE_STORE = 2
const i32 LIMIT_TYPE_GENERAL = 1
const i32 LIMIT_TYPE_CATEGORY = 2
const i32 LIMIT_TYPE_LISTING = 3
const i32 LIMIT_TYPE_SKU = 4

enum VoucherType {
    NORMAL = 1            // 普通券
    COMPENSATORY = 2      // 补偿券
}

struct Item{
    1: optional i64 skuId,
    2: optional i64 categoryId,
    3: optional i64 storeId,
    4: optional i64 totalPrice,
    5: optional i64 listingId,
    6: optional list<i16> noOwnerTypes
}

struct VoucherLimit{
    1: optional list<i64> categoryIds,
    2: optional list<i64> skuIds,
    3: optional list<i64> storeIds,
    4: optional list<i64> listingIds
}

struct VoucherTemplate{
    1: required i64 id,
    2: required string name,
    3: required bool isLimit,
    4: required i32 limitType, # 1.general 2.limit category 3.limit sku
    5: required i32 limitBillAmount,
    6: required i32 limitAmount,
    7: required i32 personalCount,
    8: required i32 ownerType, # 1.platform  2.store
    9: required bool enable,
    10: required i32 regionId,
    11: optional VoucherLimit limiter,
    12: optional VoucherType templateType
}

struct VoucherGen{
    1: required i64 templateId,
    2: required i32 limitBillAmount,
    3: required i32 amount,
    4: required i32 limitType,
    5: required i32 number,
    6: required i32 prebuiltNum,
    7: required string startDate,
    8: required string endDate,
    9: required i32 expiredDays,
    10: required i32 genType,  # 1:voucher center; 2:distribute; 3:distribute(used)
    11: optional i64 operatorId,
    12: optional string operationTime
    13: optional VoucherLimit limiter,
    14: optional i64 id,
    15: optional i32 status,  # 0 Unaudited 1 Audited  2 Audit Failed 3 online  4 offline
    16: optional i64 creatorId,
    17: optional string createAt,
    18: optional i64 auditorId,
    19: optional string auditTime,
    20: optional string name,
    21: optional i32 regionId,
    22: optional i32 ownerType,
    23: optional bool isLimit,
    24: optional i32 personalCount,
    25: optional i32 generatedNum,
    26: optional bool isEarned,
    27: optional VoucherType voucherType
}

struct Voucher{
    1: required i64 id,
    2: required i64 genId,
    3: required string name,
    4: required string code,
    5: required i64 accountId,
    6: required i32 ownerType,
    7: required i32 isLimit,
    8: required i32 limitType,
    9: required i32 limitBillAmount,
    10: required i32 amount,
    11: required string genStartDate,
    12: required string genEndDate,
    13: required string startDate,
    14: required string endDate,
    15: required i32 expiredDays,
    16: required i32 status,    # 0 not get  1 get   2 used  3 expired  4  invalid
    17: required i32 getType,  # 0 get  1 prebuilt   2 Refund voucher  3 refund amount
    18: required string createAt,
    19: required i32 regionId,
    20: optional VoucherLimit limiter,
    21: optional string getTime,
    22: optional i64 operatorId,
    23: optional string operationTime,
    24: optional i64 payBillId,
    25: optional string usedTime,
    26: optional i64 creatorId,
    27: optional i64 refundOptId,
    28: optional string refundTime,
    29: optional VoucherType voucherType
}


//struct VoucherUseLog{
//    1: required i64 id,
//    2: required i64 voucherId,
//    3: required i64 accountId,
//    4: required i64 payBillId,
//    5: required i32 amount,
//    6: required string createAt,
//}
//
//
//struct VoucherReturnLog{
//    1: required i64 id,
//    2: required i64 oldVoucherId,
//    3: required i64 newVoucherId,
//    4: required i64 auditorId,
//    5: required string auditTime,
//    6: required i64 accountId,
//    7: required i64 billId,
//    8: required i32 amount,
//    9: required string createAt
//}

struct ValidVoucher{
    1: required i64 voucherId,
    2: required string name,
    3: required string code,
    4: required i32 amount,
    5: required i32 ownerType,
    6: required i32 status,
    7: required bool isLimit,
    8: required i32 limitType,
    9: required i32 limitBillAmount,
    10: required string genStartDate,
    11: required string genEndDate,
    12: required string startDate,
    13: required string endDate,
    14: required i32 expiredDays,
    15: optional list<Item> items,
    16: optional i64 genId,
    17: optional VoucherLimit limiter,
    18: optional VoucherType voucherType
}

struct PagingVoucherTemplate{
    1: required i32 total,
    2: required list<VoucherTemplate> data
}

struct PagingVoucherGen{
    1: required i32 total,
    2: required list<VoucherGen> data
}

struct PagingVoucher{
    1: required i32 total,
    2: required list<Voucher> data
}

struct ReceivableVouchers{
    1: required list<VoucherGen> gens
    2: required list<ValidVoucher> vouchers
}

struct ItemMapGens{
    1: required Item item,
    2: required list<VoucherGen> gens
}

struct Rule{
    1:required i32 range,
    2:optional list<string> phones,
    3:optional list<i64> accountIds,
    4:optional string startTime,
    5:optional string endTime,
    6:optional i32 accountType, #1.new, 2.order, 3.complete, 4.online paid, 5.online complete
    7:optional i32 totalBillAmount,
    8:optional i32 placeOrderNum,
    9:optional i32 completeOrderNum,
    10:optional string inviteCode
}

struct Reason{
    1:required i32 type,
    2:optional string source,
    3:optional string describe,
}

struct Distribute{
    1: required i64 id,
    2: required i64 genId,
    3: required Rule rule,
    4: required Reason reason,
    5: required i32 type,  # 1:admin; 2:auto 3.lucky draw
    6: required i32 status,  # 0:Unaudited; 1:Audited; 2:Audit Failed; 3:online; 4:offline
    7: required i64 creatorId,
    8: required string createAt,
    9: required i32 regionId,
    10: required i32 number,
    11: optional i32 distributedNum,
    12: optional i64 auditorId,
    13: optional string auditTime,
    14: optional i64 operatorId,
    15: optional string operationTime
}

struct PagingDistribute{
    1: required i32 total,
    2: required list<Distribute> data
}

# Invited logging
struct InviteLog{
    1: required i64 accountId,
    2: optional string inviteCode
}

# Invitation code of account
struct ReferralCode{
    1: required i64 accountId,
    2: required string inviteCode
}

struct FollowedStore {
    1: i32 accountId,
    2: i32 storeId,
    3: string createTime,
    4: bool deleted
}
