include "exceptions.thrift"
const i16 ERROR_PERMISSION_DENIED = 10001
const i16 ERROR_STORE_ACCOUNT = 10002
const i16 ERROR_STORE_ACCOUNT_PHONE_EXIST = 10003
const i16 ERROR_STORE_ACCOUNT_EMAIL_EXIST = 10004

enum StoreStatus {
    open = 1,
    shut = 2,
    close = 3
}

const list<i16> LIVE_STORE_STATUS = [1, 2]

const set<string> passData = [
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
'W', 'X', 'Y', 'Z', '!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '.', '+',
'1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
const string TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
const i16 IndividualSellerCount = 1
const i16 BusinessSellerCount = 10

enum Operator {
    CUSTOMER = 1,
    SELLER = 2,
    ADMIN = 3,
    LOGISTIC = 4,
    SYSTEM = 5
}

struct SimpleSellerAddress {
    1: required i16 regionId,
    2: required string region,
    3: required i32 stateId,
    4: required string state,
    5: required i32 cityId,
    6: required string city
}
enum SellerType {
    personal = 1,
    company = 2
}
struct Qualification {
    1: optional string name,
    2: optional string idNumber,
    3: optional list<string> images,
    4: optional bool isInheritSeller,
    5: optional SellerType type
}
const set<i16> seller_type = [1, 2]
struct Seller {
    1: required i64 id,
    2: required string name,
    3: required string createdAt,
    4: optional SellerType type,
    5: optional i16 regionId,
    6: optional string email,
    7: optional string phone,
    8: optional string landlineNumber,
    9: optional string fax,
    10: optional string contactName,
    11: optional Qualification qualification,
    12: optional list<string> attached,
    13: optional list<string> contractDocument,
    14: optional i16 storeCount,
    15: optional i16 status,
    16: optional SimpleSellerAddress location
}
enum MarginStatus {
    pending_pay = 1,
    paid = 2
}

struct Margin{
    1: required i32 amount,
    2: required MarginStatus status
}

enum StoreApplyStatus {
    unprocessed = 1,
    passed = 2,
    rejected = 3
}

struct StoreStation {
    1: i32 storeId,
    2: i16 regionId,
    3: StoreStatus status,
    4: i64 applyId,
    5: i64 sellerId,
    6: bool isBaseStation,
    7: i64 onlineCount,
    8: i64 follows,
    9: string createdAt
    10: optional i16 comTransWareId,
    11: optional i16 speTransWareId,
    12: optional string closedAt
}

enum ApplyStoreType {
    BASE = 1,
    EXTENTION = 2,
    ALL = 0
}

struct StoreApply {
    1: required i64 id,
    2: required i64 sellerId,
    3: required string name,
    4: required string storeIcon,
    5: required i16 regionId,
    6: required string grade,
    7: required bool isGood, // 是否为精选好店
    8: required i32 itemsCount,
    9: required StoreApplyStatus status,
    10: required string createdAt,
    11: optional Qualification qualification,
    12: optional Margin margin,
    13: optional string passedAt,
    14: optional string rejectedAt,
    15: optional i32 reviewerId,
    16: optional string city,
    17: optional list<string> attached, // 电子合同，拍照合同, 店铺入驻协议等
    18: optional SimpleSellerAddress location,
    19: optional double commissionRate,
    20: optional bool isBaseStation,
    21: i16 sellerRegionId,
    22: optional i16 baseRegionId
}

const list<i16> store_status = [1, 2]
struct Ratings {
    1: required string facticity,
    2: required string serviceScore,
    3: required string shipping,
    4: optional string totalScore
}

struct Store {
    1: required i64 id,
    2: required i64 applyId,
    3: required i64 sellerId,
    4: required string name,
    5: required string storeIcon,
    6: required i16 regionId,
    7: required string grade, // 评级
    8: required bool isGood, // 是否为精选好店
    9: required i32 itemsCount,
    10: required StoreStatus status,
    11: required string createdAt,
    12: optional Qualification qualification,
    13: optional Margin margin,
    14: optional i32 reviewerId,
    15: optional string city,
    16: optional Ratings ratings,
    17: optional list<string> attached, // 电子合同，拍照合同, 店铺入驻协议等
    18: optional string shutAt,
    19: optional string closedAt,
    20: optional SimpleSellerAddress location,
    21: optional bool isUseCoin,
    22: optional i64 follows,
    23: optional i64 onlineCount,
    24: optional i16 comTransWareId,
    25: optional i16 speTransWareId,
    26: optional bool isSelfDelivery,
    27: optional double commissionRate,
    28: i16 sellerRegionId,
    29: optional bool isBaseStation,
    30: optional set<StoreStation> storeStations,
    31: optional i16 baseRegionId,
    32: optional string mailbox
}

enum AccountType {
    seller = 1,
    store = 2
}

enum LoginStatus {
    enable = 1,
    Locked = 2,
    deleted = 3
}

enum StoreOperate {
    enable = 1,
    Locked = 2,
    deleted = 3
}

struct SellerLogin {
    1: required i64 id,
    2: required string account,
    3: required AccountType accountType,
    4: required bool isRoot,
    5: required LoginStatus status,
    6: required i16 regionId,
    7: optional string phone,
    8: optional string email,
    9: optional string createdAt,
    10: optional string lastLoginIp,
    11: optional string lastActiveTime,
    12: optional i64 sellerId,
    13: optional i64 storeId,
    14: optional string uKey,
    15: optional string password,
    16: optional string trueName,
}

struct Permissions {
    1: required list<i16> pagesUsable,
    2: required list<i16> elementsUsable
}

struct AccountPermissions {
    1: required SellerLogin userInfo,
    2: required Permissions permissions
}

struct VerifyPermissions {
    1: required bool accountUsable,
    2: optional bool pagesUsable,
    3: optional bool elementsUsable,
    4: optional bool permissionChanged
}

struct MarginLog {
    1: i32 storeId,
    2: MarginStatus operateType,
    3: i16 amount,
    4: i32 staffId,
    5: string createdAt
}
struct StoreApplyRelated {
    1: required StoreApply storeApply,
    2: optional string sellerName
}
struct ApplyStoreList {
    1: required i64 count,
    2: required list<StoreApplyRelated> storeApplys
}
struct ApplyStoreDetail {
    1: required StoreApply storeApply,
    2: required Seller seller
}
enum ReviewStoreOperate {
    adopt = 1,
    reject = 2
}
struct StoreList {
    1: required i64 count,
    2: required list<Store> stores
}
struct StoreDetail {
    1: required Store store,
    2: required Seller seller,
    3: required StoreApply storeApply,
    4: optional MarginLog marginLog
}
enum LoginType {
    account_password = 1,
    phone = 2,
    email = 3,
}
const set<string> store_type = ["A", "A+", "B", "C", "D"]
const map<string,i16> store_margin = {"D": 500, "C": 1000, "B": 2000, "A": 5000
                                      "A+": 30000}
const set<string> individual_apply_store_types = ["D"]
const set<string> business_apply_store_types = ["B", "C"]

enum StoreSetType {
    edit = 1,
    state = 2
}
const set<i16> store_set_types = [1, 2]
struct StoreUpdateApply {
    1: required i64 id,
    2: required i64 storeId,
    3: optional string storeName,
    4: optional string storeIcon,
    5: optional SimpleSellerAddress address,
    6: optional StoreApplyStatus status,
    7: required string createdAt,
    8: optional string passedAt,
    9: optional string rejectedAt
}
struct StoreCategory {
    1: required i64 id,
    2: required i64 storeId,
    3: required string name,
    4: required i32 listingCount,
    5: optional string image,
    6: required bool isDeleted,
    7: required string createdAt,
    8: optional string latestUpdatedAt,
    9: required bool isOthers,
    10: optional i64 onlineCount
}
struct StoreCategoryList {
    1: required i32 count,
    2: required list<StoreCategory> storeCategories
}
struct LoginList {
    1: required i32 count,
    2: required list<SellerLogin> sellerLogins
}

struct CoinAgreement {
    1: required i32 sellerId,
    2: required i64 storeId,
    3: required string storeName,
    4: required bool isJoin,
    5: required string createdAt
}

struct CoinAgreementlist {
    1: required i64 count,
    2: required list<CoinAgreement> coinAgreements
}

struct RecommendProduct {
    1: required i32 storeId,
    2: required i16 regionId,
    3: required set<i64> listingIds,
    4: required string createdAt
}
struct MultiAddress {
    1: required string contacts,
    2: required string phone,
    3: required string provinceCity,
    4: required string detail
}
struct ShipperAddress {
    1: required i32 storeId,
    2: optional MultiAddress zhAddress,
    3: optional MultiAddress enAddress,
    4: optional string createdAt,
    5: optional i16 regionId
}

struct Warehouse {
    1: i32 id,
    2: string name
}

enum DeliveryApplyState {
    PEND_REVIEW = 1,
    PASS = 2,
    REJECT = -1
}

struct SelfDelivery {
    1: i32 id,
    2: i32 storeId,
    3: i32 sellerId,
    4: list<Warehouse> warehouses,
    5: string createdAt,
    6: DeliveryApplyState status,
    7: optional string reviewer,
    8: optional string ecourierAccount,
    9: optional i32 ecourierAccountId,
    10: optional string reviewedAt,
    11: i16 regionId
}

struct SelfDeliveryRelate {
    1: SelfDelivery selfDelivery,
    2: string city,
    3: string storeName
}

struct PickupAddress {
    1: string contactPerson,
    2: string mobile,
    3: string division,
    4: string district,
    5: string thana,
    6: string pickUnion,
    7: string address,
    8: i32 branchId
}

struct ExpandStoreLog {
    1: StoreApplyStatus operateCode,
    2: i16 regionId,
    4: string appliedAt,
    3: string lastUpdatedAt
}

struct ExpandApplyResult {
    1: bool isSuccess,
    2: i16 regionId,
    3: optional string failReason
}

struct LoginInfo {
    1: Store store,
    2: SellerLogin login
}

struct StoreOperateLog {
    1: i32 sellerId,
    2: i32 storeId,
    3: i16 regionId,
    4: StoreOperate operate,
    5: string createdAt,
    6: optional string remark,
    7: optional i32 operatorId
}

struct FaultAndPunishmentConfig {
    1: i32 id,
    2: i16 regionId,
    3: i32 index,
    4: string name,
    5: string chDisplay,
    6: string flDisplay,
    7: bool isPunishment,
    8: double chPenaltyAmount,
    9: double localPenaltyAmount,
    10: bool isCompensatory,
    11: i32 compensationCouponId,
    12: string currency,
    13: string description,
    14: string paramModule
}

enum MarginRecordStatus {
    NEW_CREATE = 1,
    CONFIRMED = 2
}

struct MarginRecord {
    1: i32 id,
    2: i32 storeId,
    3: i32 paidAmount,
    4: string currency,
    5: MarginRecordStatus status,
    6: string platformReceivingAccount,
    7: string transferAccount,
    8: string transactionSerialNumber,
    9: string createdAt,
    10: string transferDate,
    11: optional string confirmedAt,
    12: optional i32 confirmOperatorId
}

struct MarginRecordList{
    1: i32 count,
    2: list<MarginRecord> marginRecords
}

struct MonthlyMarginAndDisclaimer {
    1: i32 storeId,
    2: string years,
    3: i16 disclaimerCount,
    4: i16 disclaimerDeducted,
    5: double marginDeducted,
    6: string currency,
    7: optional double marginAmount
}

enum FaultRecordStatus {
    NEW_CREATE = 1
}

enum PUNISHMENT_TYPE {
    DISCLAIMER = 1,
    DEDUCTION_MARGIN = 2,
    DEDUCTION_IN_CLEARING = 3
}

struct FaultRecord {
    1: i32 id,
    2: i16 regionId,
    3: i32 storeId,
    4: i16 faultConfigId,
    5: i64 saleOrderId,
    6: FaultRecordStatus status,
    7: bool isAppeal,
    8: optional string createdAt,
    9: optional string storeName,
    10: optional string faultItem,
    11: optional string faultName,
    12: optional string faultDescription,
    13: optional i32 punishmentRecordId,
    14: optional PUNISHMENT_TYPE punishmentType,
    15: optional double penaltyAmount,
    16: optional string currency,
    17: optional string saleOrderCode
}

struct FaultRecordList {
    1: i32 count,
    2: list<FaultRecord> records
}

struct PunishmentRecord {
    1: i32 id,
    2: PUNISHMENT_TYPE punishmentType,
    3: i16 regionId,
    4: double penaltyAmount,
    5: i64 faultRecordId,
    6: i64 saleOrderId,
    7: string saleOrderCode,
    8: i32 storeId
    9: i32 faultConfigId,
    10: string createdAt
}

enum MARGIN_LOG_DIRECTION {
    CREDIT = 1,
    OUTLAY = 0
}

enum MARGIN_CHANGE_REASON {
    CREDIT = 1,
    PUNISHMENT = 2,
    AFTERSALE_DEDUCTION = 3,
    RETURN = 4
}

struct MarginOperateLog {
    1: i32 id,
    2: i32 storeId,
    3: double amount,
    4: string currency,
    5: MARGIN_LOG_DIRECTION direction,
    6: double balanceBefore,
    7: double balanceAfter,
    8: MARGIN_CHANGE_REASON reason,
    9: i32 sourceId,
    10: string createdAt
}

struct MarginOperateLogList {
    1: i32 count,
    2: list<MarginOperateLog> logs
}

enum SizeCompare {
    LT = 1,
    LTE = 2,
    EQ = 3,
    GT = 4
    GTE = 5
} // 以中文为单位

const map<i16, string> SIZE_COMPARE_MAP = {1: "$lt", 2: "$lte", 3: "$eq", 4: "$gt", 5: "%gte"}

struct MarginCompare {
    1: i16 sellerRegionId,
    2: i32 amount,
    3: SizeCompare comparison
}

struct StoreMessage {
    1: i32 id,
    2: string title,
    3: string publishTime,
    4: string publisher,
    5: string content,
    6: list<i32> publishTo
}
struct StoreMessageList {
    1: required i64 count,
    2: required list<StoreMessage> storeMessages
}
