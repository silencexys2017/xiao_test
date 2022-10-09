# Error code
# common[1000-1999]
const i16 ERROR_COMMON_REGION_NOT_EXIST = 1000
const i16 ERROR_COMMON_SEND_FAILED = 1001
const i16 ERROR_COMMON_PHONE_ABNORMAL = 1002
const i16 ERROR_COMMON_SMS_RESEND = 1003
const i16 ERROR_COMMON_CODE_EXPIRED = 1004
const i16 ERROR_COMMON_CODE_INVALID = 1005
const i16 ERROR_COMMON_APP_VERSION_LOW = 1006
const i16 ERROR_COMMON_EMAIL_CODE_INVALID = 1007
const i16 ERROR_COMMON_EMAIL_CODE_EXPIRED = 1008

# actor[2000-2999]
const i16 ERROR_ACTOR_ACCOUNT_NOT_EXIST = 2000
const i16 ERROR_SYS_TOKEN_EXPIRED = 2001
const i16 ERROR_SYS_REFRESH_TOKEN_EXPIRED = 2002
const i16 ERROR_SYS_TOKEN_INVALID = 2003
const i16 ERROR_ACTOR_BALANCE_NOT_EXIST = 2004
const i16 ERROR_BALANCE_INSUFFICIENT = 2005
const i16 ERROR_ACTOR_NICKNAME_MODIFIED = 2006
const i16 ERROR_ACTOR_PIN_ERROR = 2007
const i16 ERROR_WITHDRAW_AMOUNT_INVALID = 2008
const i16 ERROR_PIN_ERROR_COUNTS = 2009
const i16 ERROR_ACTOR_EMAIL_INVALID = 2010
const i16 ERROR_ACTOR_PIN_NULL = 2011
const i16 ERROR_WITHDRAW_NOT_EXIST = 2012
const i16 ERROR_WITHDRAW_ONLY_ONCE = 2013
const i16 ERROR_WITHDRAW_IN_PROCES = 2014
const i16 ERROR_WITHDRAW_STATUS_ERROR = 2015
const i16 ERROR_WITHDRAW_NOTSET_PIN = 2020


# advertiser[3000-3999]
const i16 ERROR_INVITED_USER_NOT_EXIST = 3000
const i16 ERROR_ADVERTISER_NOT_EXIST = 3001

# convert[4000-4999]
const i16 ERROR_INVITE_ORDER_CONVERT_HAVE_EXIST = 4000

# admin[5000-5999]
const i16 ERROR_ADMIN_ACCOUNT = 5000
const i16 ERROR_PERMISSION_DENIED = 5001

# article[6000-6999]
const i16 ERROR_ARTICLE_NOT_FOUND = 6000

const string TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
const i16 REGION_BANGLADESH = 1
const i16 ADVERTISER_PLAT_PERFEE = 1

# 账号类型: 1:normal、2:star
enum ActorType {
    NORMAL = 1
    STAR = 2
}
# 验证码类型: 1:登录、2:设置密码
enum VerifyCodeType {
    LOGIN = 1
    SET_PIN = 2
}
# 密码类型：1.普通密码
enum PinType {
    NORMAL = 1
}
# 账户变更日志类型：1.获得；2.花费
enum BalanceLogType {
    GET = 1,
    SPEND = 2,
    REFUND = 3
}
# 账户日志变更来源类型：1.邀请转化；2.文章转化；3.分享转化；4.提现
enum BalanceLogSource {
    INVITE_CONVERT = 1,
    ARTICLE_CONVERT = 2,
    SHARE_CONVERT = 3,
    WITHDRAW = 4
}
# 银行账户类型：1.bKash
enum AccountType {
    BKASH = 1
}
# 提现申请：1.待审核；2.待转账；3.转账中；4.完成提现； -1.取消；-2.拒绝
enum WithdrawApplyStatus{
    AUDITING = 1,
    AUDITED = 2,
    CASHING = 3,
    COMPLETE = 4,
    CANCEL = -1,
    REFUSE = -2
}

enum AdminUserState {
    ACTIVATED = 1,
    LOCKED = 2
}

enum AdminUserLevel {
    SUPER_ADMIN = 1,
    SENIOR_ADMIN = 2,
    GENERAL_ADMIN = 3
}

struct Token {
    1: required string refreshToken,
    2: required i32 refreshTokenTimeout,
    3: required string accessToken,
    4: required i32 accessTokenTimeout,
//    5: optional i32 id,
//    6: optional string phone,
}

struct Region {
    1: required i32 id,
    2: required string callingCode
    3: required string code,
    4: required string name,
    5: required string intro,
    6: required string flag,
    7: required i16 currencyId,
    8: required string currencySymbol,
    9: required i16 currencyConversion,
    10: required string language,
    11: required string timeZone,
    12: required string currency,
    13: required i16 index,
    14: required i16 minAppVersion,
}

struct PromoteTotal {
    1: required i64 actorId,
    2: required i64 adPlatformId,
    3: required i64 advertiserId,
    4: required i32 newCustomers, #新邀请用户数
    5: required i32 verifiedCustomers, #邀请用户认证数
    6: required i32 inviteOrders, #邀请用户订单数
    7: required i32 completeInviteOrders, #邀请用户成功交易订单数
    8: required i32 commissionOrders, #佣金订单数
    9: required i64 commissionAmounts, #佣金金额
    10: required i32 articles, #文章数
    11: optional i32 completeArticleOrders, #文章转化成功交易订单数
    12: optional i32 completeShareOrders, #分享转化成功交易订单数
}

struct PayPin {
    1: required i64 actorId,
    2: required PinType type,
    3: required string pin
}

struct Balance {
    1: required i64 actorId,
    2: required i64 current,
    3: required i64 available,
    4: required i64 locked,
    5: required i64 used,
    6: required i64 historyTotal,
    7: required string lastUpdateTime,
}

struct BalanceLog {
    1: required i64 actorId,
    2: required i64 amount,
    3: required BalanceLogType type,
    4: required string createTime,
    5: required BalanceLogSource sourceType,
    6: optional i64 sourceId
}

struct WithdrawApply {
    1: required i64 id,
    2: required i64 actorId,
    3: required i64 amount,
    4: required WithdrawApplyStatus status,
    5: required AccountType accountType,
    6: required string accountNumber,
    7: required string applyTime,
    8: optional string auditTime,
    9: optional string startCashTime,
    10: optional string completeTime,
    11: optional i64 auditOperator,
    12: optional i64 transferOperator
}

struct Actor {
    1: required i64 id,
    2: required i32 regionId,
    3: required string phone,
    4: required ActorType type,
    5: required bool isEnabled,
    6: required bool isDeleted,
    7: required string createTime,
    8: required string lastActiveTime,
    9: optional string email,
    10: optional string country,
    11: optional string nick
}

struct Advertiser {
    1: i64 id
    2: i64 actorId
    3: i64 adPlatformId
    4: string inviteCode
    5: string loginName
    6: optional string openId
    7: optional string nick
    8: optional string adpRegisterTime
}

struct ActorDetail {
    1: required Actor actor,
    2: optional Balance balance,
    3: optional PromoteTotal promoteTotal,
    4: optional Advertiser advertiser
}

struct LoginInfo {
    1: required Token token,
    2: required Actor actor,
    3: optional bool isRegister,
    4: optional bool existAdUser,
    5: optional bool existPayPin,
    6: optional string inviteCode
}

struct PagingActorDetail{
    1: required i64 total=0,
    2: required list<ActorDetail> data=[]
}

struct PagingBalanceLog{
    1: required i64 total=0,
    2: required list<BalanceLog> data=[]
}

struct InvitedUser {
    1: string invitedOpenId
    2: string phone
    3: string invitedTime
    4: bool isVerified
    5: optional i64 actorId
    6: optional string nick
    7: optional string email
    8: optional i64 regionId
    9: optional string regionCode
    10: optional string lastActiveTime
    11: optional string inviteCode
    12: optional i64 orderPlaced
    13: optional i64 orderCompleted
    14: optional i64 rewardAmount
}

struct FilterInvitedUserResult {
    1: i64 total,
    2: list<InvitedUser> invitedUsers
}

struct InviteConvert {
    1: string inviteCode,
    2: string accountId,
    3: i32 validAmount
}

struct ArticleOrderConvert {
    1: string authorCode,
    2: string accountId,
    3: i32 validAmount,
    4: string articleId,
    5: string skuId
}

enum AfterSaleOption {
    EXISTS = 1,
    NOT_EXIST = 2,
    ALL = 0
}

enum ShareSourceType {
    ARTICLE = 1,
    LISTING = 2,
    GROUP_BUYING = 3,
    GROUP_BUYING_TEAM = 4
}

struct ShareOrderConvert {
    1: string referCode,
    2: string accountId,
    3: i32 validAmount,
    4: string sourceType,
    5: string sourceId,
    6: string skuId
}

struct SaleOrderConverts{
    1: string orderId,
    2: string orderCode,
    3: string storeName,
    4: i32 storeId,
    5: i32 payAmount,
    6: i32 postage,
    7: InviteConvert invite,
    8: list<ArticleOrderConvert> articles,
    9: list<ShareOrderConvert> shares
}

enum PayMethod {
    ONLINE = 1,
    COD = 2,
    ALL = 0
}

enum OrderStatus {
    NOT_ACTIVE = 1,
    IN_PROGRESS = 2,
    COMPLETE = 3,
    CANCEL = -1,
    REJECT = -2
}

enum OrderOprate {
    CREATE = 1,
    ACTIVE = 2,
    COMPLETE = 3,
    CANCEL = -1,
    REJECT = -2
}

struct OrderInfo {
    1: string orderId,
    2: string orderCode,
    3: string customerId,
    4: string customerNick,
    5: string customerPhone,
    6: i32 storeId,
    7: string storeName,
    8: i32 payAmount,
    9: PayMethod payMethod,
    10: i32 postage,
    11: OrderStatus orderStatus
    12: i16 regionId,
    13: string createdAt,
    14: string lastUpdatedAt
}

struct InviteOrderConvert {
    1: i64 id,
    2: i64 invitedCustomerId,
    3: i64 actorId,
    4: i64 adPlatformId,
    5: i64 advertiserId,
    6: string adOpenId,
    7: i32 validAmount,
    8: string createdAt,
    9: OrderInfo orderInfo,
    10: optional string regionCode
}

struct InviteOrderList {
    1: i64 count,
    2: list<InviteOrderConvert> orders
}

struct ArticleConvert {
    1: i64 id,
    2: string adOpenId,
    3: i64 actorId,
    4: i64 adPlatformId,
    5: i64 advertiserId,
    6: i64 articleId,
    7: string adpArticleId,
    8: string productId,
    9: i32 validAmount,
    10: string createdAt,
    11: OrderInfo orderInfo
}

struct ArticleConvertList {
    1: i64 count,
    2: list<ArticleConvert> orders
}

struct ShareConvert {
    1: i64 id,
    2: string adOpenId,
    3: i64 actorId,
    4: i64 adPlatformId,
    5: i64 advertiserId,
    6: i32 validAmount,
    7: ShareSourceType sourceType,
    8: string sourceId,
    9: string productId,
    10: string createdAt,
    11: OrderInfo orderInfo
}

struct ShareConvertList {
    1: i64 count,
    2: list<ShareConvert> orders
}

enum ConvertType {
    INVITE = 1,
    ARTICLE = 2,
    SHARE = 3
}

struct OrderRelate {
    1: string orderId,
    2: string orderCode,
    3: string customerId,
    4: string customerNick,
    5: i32 storeId,
    6: string storeName,
    7: i32 payAmount,
    8: i32 postage,
    9: string createdAt,
    10: string completedAt,
    11: PayMethod payMethod,
    12: OrderStatus orderStatus,
    13: i16 regionId,
    14: bool isAfterSales
}

struct OrderCommission {
    1: i64 id,
    2: i32 adPlatformId,
    3: i32 validAmountTotal,
    4: i32 commissionTotal,
    5: string orderCompleteTime,
    6: bool isVerifyCancel,
    7: string createTime,
    8: list<ConvertType> contributors,
    9: OrderRelate orderRelate,
    10: optional i32 operatorId,
    11: optional string operationTime
}

struct ActorCommission{
    1: ConvertType convertType,
    2: i64 actorId,
    3: i64 advertiserId,
    4: string adOpenId,
    5: i64 orderCommissionId,
    6: string orderId,
    7: i32 validAmount,
    8: i32 commission,
    9: string createTime
}

struct OrderComRelated {
    1: i32 payAmount,
    2: string consumerNick,
    3: i32 totalCommission,
    4: ActorCommission actorCommission
}

struct OrderCommissionList {
    1: i64 count,
    2: list<OrderCommission> orders
}

struct MonthCommission {
    1: i16 year,
    2: i16 month,
    3: i32 amount
}

struct AdminSubMenu {
    1: required i16 id,
    2: required string name,
    3: required string url
}

struct AdminMenu {
    1: required i16 id,
    2: required string name,
    3: required list<AdminSubMenu> subMenu
}

struct AdminPermission {
    1: required list<i16> menusUsable,
    2: required list<i16> pagesUsable,
    3: required list<i16> elementsUsable
}

struct AdminSignIn {
    1: required i32 userId,
    2: required string userName,
    3: required list<AdminMenu> menus,
    4: required AdminPermission permissions,
    5: optional AdminUserLevel roleLevel
}

struct AdminUser {
    1: required i32 userId,
    2: required string userName,
    3: required string trueName,
    4: required AdminUserState state,
    5: optional string lastLoginIp,
    6: optional string lastLoginTime,
    7: optional AdminUserLevel roleLevel
}

struct AdminUsers {
    1: required i32 total,
    2: required list<AdminUser> users
}

struct Element {
    1: required i16 id,
    2: required string name
}

struct AdminUserPermissions {
    1: required AdminUser userInfo,
    2: required list<AdminMenu> menus,
    3: required list<Element> elements,
    4: required list<i16> pagesUsable,
    5: required list<i16> elementsUsable 
}

struct AdminInterfaceValidation{
    1: required bool accountUsable,
    2: optional bool pageUsable,
    3: optional bool elementUsable,
    4: optional bool permissionChanged
}

// actor article
enum ArticleType {
    ARTICLE = 1
    REVIEW = 2
}

enum ArticleStatus {
    AUDITING = 1
    PASSED = 2
    REFUSED = 3
    OFFLINE = 4
    DISPLAYING = 5
    DELETED = -1
}

enum ArticleSelectiveStatus {
    NO_STATUS = 1
    ACTIVE = 2
    INACTIVE = 3
}

enum ArticleContentType{
    TEXT = 1
    IMAGE = 2
    PRODUCT = 3
    VIDEO = 4
}

enum ProductType {
    BOUGHT = 1
    POOL = 2
}

struct ArticleContentData{
    1: required string name
    2: required string value
}

struct ArticleContent{
    1: required i32 index,
    2: required ArticleContentType type,
    3: required string content,
    4: required list<ArticleContentData> data, # 修正
}

struct Article{
    1: required i64 id,
    2: required i64 actorId,
    3: required string actorName,
    4: required string actorPhone,
    5: required i32 adPlatformId,
    6: required i64 advertiseId,
    7: required string adOpenId,
    8: required ArticleType type,
    9: required string adpArticleId 
    10: required ArticleStatus status,
    11: required ArticleSelectiveStatus selectiveStatus,
    12: required string title,
    13: required string cover, # 命名修改
    14: required ProductType productType,
    15: required i32 productCount,
    16: required list<string> productIds,
    17: required i32 orderCount,
    18: required i32 pv,
    19: required i32 uv,
    20: required string createdTime,
    21: required string postedTime,
    22: required string updatedTime,
    23: required i64 operatorId,
    24: required string operationTime,
    25: optional list<ArticleContent> contentList,
    26: optional string inviteCode
}

struct PagingArticle{
    1: required i32 total,
    2: required list<Article> articles
}


struct WithdrawApplyDetail {
    1: required WithdrawApply withdraw,
    2: optional Actor actor,
    3: optional Balance balance,
    4: optional Advertiser advertiser,
    5: optional PromoteTotal promoteTotal
}

struct PagingWithdrawApplyDetail{
    1: required i64 total=0,
    2: required list<WithdrawApplyDetail> data=[]
}