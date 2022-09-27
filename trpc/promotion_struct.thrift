const i32 APPLY_STATUS_UNAUDITED = 1
const i32 APPLY_STATUS_AUDITED = 2
const i32 APPLY_STATUS_AUDIT_FAILED = 3
const i32 APPLY_STATUS_APPLY_CANCEL = 4
const i32 APPLY_STATUS_CANCEL = 5
const i32 APPLY_STATUS_INVALID = 6
const i32 APPLY_STATUS_EXPIRED = 7
const i32 ACTIVITY_SKU_STATUS_ACTIVE = 1
const i32 ACTIVITY_SKU_STATUS_INVALID = 2
const i32 ACTIVITY_TYPE_FLASH_SALE = 1
const i32 ACTIVITY_TYPE_LUCKY_DRAW = 2
const i32 ACTIVITY_TYPE_REDEEM = 3
const i32 ACTIVITY_TYPE_DEAL = 4
const i32 ACTIVITY_TYPE_GROUP_BUYING = 5
const i32 LIMIT_RULE_NORMAL = 1
const i32 LIMIT_RULE_ONECE = 2
const i32 LIMIT_RULE_ACCOUNT_ONECE = 3
const i32 COMPLETION_PERIOD_12_HOUR = 12
const i32 COMPLETION_PERIOD_24_HOUR = 24
const i32 COMPLETION_PERIOD_48_HOUR = 48
const i64 ORDER_PAID_DELAY = 2400000
const i64 ONE_HOUR_TTL = 3600000
const i64 TWELVE_HOUR_TTL = 43200000
const i64 TWENTY_FOUR_HOUR_TTL = 86400000
const i64 FORTY_EIGHT_HOUR_TTL = 172800000
const i32 GROUP_BUYING_OTHERS_TAG_ID = -1

# 奖励级别: 1:特等、2:一等、3:二三等、4:参与
enum AwardLevel {
    SpecialAward = 1
    FirstAward = 2
    SecondAward = 3
    ThirdAward = 4
    ParticipationAward = 5
}

# 奖励类型: 1:sku、2:voucher、3:coins:
enum AwardType {
    Sku = 1
    Voucher = 2
    Coins = 3
}

# 抽奖序列状态
enum DrawBatchStatus {
    Disabled = 1    # 未启用
    Enabled = 2     # 启用
    Finished = 3    # 结束
}

# 抽奖机会类型
enum DrawChanceType {
    DailyFree = 1   # 每日免费次数
    DailyCoins = 2  # 每日coins次数
    Earned = 3      # 其他途径获取的永久次数
}

# 奖品发放状态
enum AwardStatus {
    Unsend = 1   # 未发放
    Sent = 2     # 已发放
}

# 奖品发放类型
enum AwardSendType{
    Order = 1         
    Voucher = 2
    Coins = 3
}

# 抽奖账户抽奖次数流水
enum EarnedFreeTimesLogType{
    Order = 1
    LuckyDraw = 2
}

# 秒杀申请人类型: 1:管理员 2:商家 3:店铺管理员
enum OperatorType {
    ADMIN = 1
    SELLER = 2
    STORE_ADMIN = 3
}

# Activity SKU Type: 1:flash sale 2:lucky draw 3:coins redeem
enum ActivityType {
    FLASH = 1
    LUCKY_DRAW = 2
    REDEEM = 3,
    GROUP_BUYING = 5
}

# Activity SKU Status: 1.active  2.invalid
enum ActivityStatus {
    ACTIVE = 1
    INVALID = 2
}
# Activity SKU Status: 1.active  2.invalid
enum LimitRuleType {
    NORMAL = 1
    EVERY_ORDER = 2
    SKU_OF_ACOUNT = 3
}

enum TodatDealApplyStatus {
    WAITING = 1
    PASSED = 2
    REFUSED = 3
}

enum TodatDealFilterTimeType {
    APPLY_TIME = 1  # 申请时间
    AUDIT_TIME = 2  # 审核时间
}

enum PromotionType {
    PRICE_BREAK_DISCOUNT = 1
}

enum PromotionStatus {
    WAITING = 1
    PASSED = 2
    REFUSED = 3
    CANCELED = 4
}

enum PromoActiveStatus {
    NOT_STARTED = 1
    IN_PROGRESS = 2
    CLOSED = 3
}

enum PromotionProductStatus {
    WAITING = 1
    PASSED = 2
    REFUSED = 3
    CANCELED = 4
}

// 数据库中GroupBuying的state
enum GroupBuyingState {
    PENDING_AUDIT = 1,
    PASSED = 2,
    REJECT = -1,
    CANCELED = -2,
    SHELF_OFF = -3,
}

// 是由数据库中的state结合日期时间计算得出
enum GroupBuyingStatus {
    PENDING_AUDIT = 1,    // 待审核 state = 1 & startOn > now()
    PENDING_START = 2,    // 待开始 state = 2 & startOn > now()
    ONGOING = 3,          // 进行中 state = 2 & startOn <= now() < expiredOn
    INVALID = -1,         // 已失效 state = 1 & startOn <= now()
    REJECT = -2,          // 已拒绝 state = -1
    CANCELED = -3,        // 已取消 state = -2
    EXPIRED = -4,         // 已过期 state = 2 & now() >= expiredOn
    SHELF_OFF = -5        // 已下架 state = -3
}

enum GroupBuyingTeamState {
    PRE_CREATED = 1,               // 预创建团,团长未支付
    CREATED_AND_NOT_FULL = 2,      // 建团成功,团长已支付,未满员
    FULL_BUT_NOT_ALL_PAID = 3,     // 满员,但有团员未支付
    FULL_AND_ALL_PAID = 4,         // 满员,所有有团员已支付,成团
    EXPIRED = -1                   // 过期未成团
    LEADER_CANCEL = -2             // 团长取消
}

enum GroupBuyingTeamStatus {
    PRE_CREATED = 1,    // 预创建团,团长未支付 TeamState = 1
    NOT_FULL = 2,       // 未满员 TeamState = 2
    FULL = 3,           // 满员 TeamState in [3, 4]
    TEAM_INVALID = -1   // 过期未成团或者团长取消 TeamState in [-1, -2]
}

enum GroupBuyingTeamMemberState {
    JOINED_BUT_NOT_PAID = 1,       // 入团, 但尚未支付
    JOINED_AND_PAID = 2,           // 入团, 且已支付
    CANCELED = -1                  // 取消(超时未支付取消,主动取消)
    TEAM_EXPIRED = -2              // 过期未成团
    TEAM_LEADER_CANCEL = -3        // 团长取消
}

enum GroupBuyingTeamMemberStatus {
    NOT_PAID = 1                         // 待支付 MemberState = 1
    PAID_BUT_TEAM_NOT_SUCCESS = 2        // 已支付,拼团中 MemberState = 2 & TeamState in [2, 3]
    TEAM_SUCCESS = 3                     // 拼团成功 MemberState = 2 & TeamState = 4
    CANCELED = -1                        // 取消(超时未支付取消,主动取消) MemberState = -1
    TEAM_INVALID = -2                    // 过期未成团或者团长取消 MemberState in [-2, -3]
}

enum BigDiscountSaleState {
    PENDING_AUDIT = 1,     // 待审核
    PASSED = 2,            // 通过
    REJECT = -1,           // 拒绝
    CANCELED = -2          // 取消或下架
}

enum BigDiscountSaleStatus {
    PENDING_AUDIT = 1,     // 待审核
    PENDING_START = 2,     // 待开始
    ONGOING = 3,           // 进行中
    EXPIRED = 4            // 已过期
    CANCELED = -1          // 取消或下架或拒绝
}

enum BigDiscountSaleProductState {
    ONGOING = 1
    CANCELED = -1
}

enum BigDiscountSaleProductStatus {
    PENDING_START = 1
    ONGOING = 2
    EXPIRED = 3
    CANCELED = -1
}

enum TopicPageStatus {
    EXPIRED = -2,
    DELETED = -1,
    ACTIVITY = 1
}

struct ActivitySkuStockItem {
    1: i32 activityType,
    2: i64 activityId,
    3: i32 count
}

struct TimeInterval {
    1:optional i32 startHour,
    2:optional i32 endHour,
}

struct IntervalRule {
    1:required i32 type,  # 1.every day, 2.all
    2:optional list<TimeInterval> intervals
}

struct LimitRule {
    1:required LimitRuleType type   # 1.normal; 2.one order one sku; 3.one acount one sku
}

struct SessionGen {
    1: required i64 id,
    2: required i32 regionId,
    3: required i32 activityType,  # 1.flash sales
    4: required string startTime,
    5: required string endTime,
    6: required IntervalRule intervalRule,
    7: required i32 status,
    8: required i64 creatorId,
    9: required string createAt,
    10: optional i64 auditorId,
    11: optional string auditTime,
    12: optional i64 operatorId,
    13: optional string operationTime
}

struct Session {
    1: required i64 id,
    2: required i32 regionId,
    3: required i32 genId,
    4: required i32 activityType,  # 1.flash sales
    5: required i32 index,
    6: required string startTime,
    7: required string endTime,
    8: required string date,
    9: optional i32 count,
    10: optional i32 status, # 1.in progress; 2.in coming; 3.waiting; 4.expired    9: optional i32 count,
    11: optional i32 applyCount,
    12: optional string queryTime

}

struct CloneSku {
    1: required i64 storeId,
    2: required i64 listingId,
    3: required string title,
    4: required i64 salePrice,
    5: required i64 listPrice,
    6: required string image,
    7: optional string spec
}

struct BatchActivityApply {
    1: required i64 skuId,
    2: required i64 storeId,
    3: required i64 listingId,
    4: required string title,
    5: required i64 salePrice,
    6: required i64 listPrice,
    7: required string image,
    8: required i64 activityPrice,
    9: required i32 promiseStock,
}

struct ActivityApply {
    1: required i64 id,
    2: required i32 regionId,
    3: required i64 applySessionId,
    4: required i32 activityType,  # 1.flash sales
    5: required i64 skuId,
    6: required i64 activityPrice,
    7: required LimitRule limitRule,
    8: required i32 promiseStock,
    9: required i32 status,  # 1:Unaudited; 2:Audited; 3:Audit Failed; 4:Apply Cancel; 5:Cancel; 6:Invalid; 7:Expired
    10: required OperatorType applicantType,
    11: required i64 applicantId,
    12: required bool isAcceptAdjust,
    13: required string createAt,
    14: required CloneSku cloneSku,
    15: required bool noRemissionPostage,
    16: required bool noRemissionAmount,
    17: required bool noVoucher,
    18: optional i64 operatorId,
    19: optional string operationTime,
    20: optional string rejectReason,
    21: optional string applySessionStart,
    22: optional string applySessionEnd,
    23: optional i64 finalSessionId,
    24: optional string finalSessionStart,
    25: optional string finalSessionEnd,
    26: optional OperatorType operatorType
}

struct SimpleActivitySku {
    1: required i64 id,
    2: required i32 activityType,  # 1.flash sales
    3: required i64 skuId,
}

struct ActivitySku {
    1: required i64 id,
    2: required i32 regionId,
    3: required i64 sessionId,
    4: required i64 applyId,
    6: required i32 activityType,  # 1.flash sales
    7: required i64 skuId,
    8: required i64 activityPrice,
    9: required i32 index,
    10: required CloneSku cloneSku,
    11: required LimitRule limitRule,
    12: required i32 promiseStock,
    13: required i32 status,  #1.active  2.invalid
    14: required string createAt,
    15: required string sessionStartTime,
    16: required string sessionEndTime,
    17: required bool noRemissionPostage,
    18: required bool noRemissionAmount,
    19: required bool noVoucher,
    20: optional i32 stock,
    21: optional i32 lockStock,
    22: optional i32 sold,
}

struct SetParameter{
    1: required i32 regionId,
    2: required string name,
    3: required string value,
    4: required string paramModule,
    5: optional i32 index
}

struct Parameter{
    1: required i64 id,
    2: required i32 regionId,
    3: required string name,
    4: required string value,
    5: required string dataType,
    6: required string paramModule,
    7: optional i32 index
}

struct PagingSessionGen{
    1: required i32 total,
    2: required list<SessionGen> data
}

struct PagingSession{
    1: required i32 total,
    2: required list<Session> data
}

struct PagingActivityApply{
    1: required i32 total,
    2: required list<ActivityApply> data
}

struct PagingActivitySku{
    1: required i32 total,
    2: required list<ActivitySku> data
}

struct CurrentSessionSku{
    1:required Session session,
    2:required list<ActivitySku> skus
}

# 抽奖相关
struct LuckyDrawRules{
    1:required i64 dailyFreeTimes,
    2:required i64 dailyCoinsTimes,
    3:required i64 coinsPerTimes,
    4:required bool addTimesFromOrder,
}

struct NewLuckyDrawAward{
    1:required AwardLevel level, 
    2:required AwardType type,
    3:required string award, # 奖品的skuID, voucher定向发放ID或者coins数量的字符串
    4:required string displayName,
    5:required i64 total,
}

struct LuckyDrawAward{
    1:required i64 id,
    2:required i64 batchId,
    3:required AwardLevel level, 
    4:required AwardType type,
    5:required string award, # 奖品的skuID, voucher定向发放ID或者coins数量的字符串
    6:required string displayName,
    7:required i64 total, # 奖品总数
    8:required i64 drewNumber, # 已经抽中的数量
    9:required i64 leftNumber, # 剩余个数
    10:required i32 awardIndex
}

struct LuckyDrawBatch{
    1:required i64 id,
    2:required i64 regionId,
    3:required DrawBatchStatus status,
    4:required string startAt,
    5:required string endAt,
    6:required list<LuckyDrawAward> awards,
    7:required string updatedAt,
}

struct PagingLuckyDrawBatch{
    1: required i32 total,
    2: required list<LuckyDrawBatch> data
}

struct LuckyDrawLog{
    1:required i64 id,
    2:required i64 accountId,
    3:required DrawChanceType chanceType,
    4:required i64 batchId,
    5:required string batchStartAt,
    6:required string batchEndAt,
    7:required LuckyDrawAward award,
    8:required AwardStatus awardStatus,
    9:required i64 coinsCost,
    10:required AwardSendType sendType,         // 奖品发放类型  1:order  2:voucher 3: coins
    11:optional string sendContent,             // 奖品发放内容  orderId  voucherId优惠券ID  coins数
    12:optional string createdAt
}

struct PagingLuckyDrawLog{
    1: required i32 total,
    2: required list<LuckyDrawLog> data
}

struct LuckyDrawTimes{
    1: i32 leftDailyFreeTimes
    2: i32 leftDailyCoinsTimes
    3: i32 leftEarnedFreeTimes
}

struct LuckyDrawAccount{
    1: i64 id,
    2: i64 accountId,
    3: i32 totalEarnedTimes,
    4: i32 leftEarnedTimes,     /// 剩余次数, 原子性 findoneandupdate
    5: string createdAt,
    6: string updatedAt
}

struct LuckyDrawProbability{
    1: list<i32> indexZero,
    2: list<i32> indexOne,
    3: list<i32> indexTwo,
    4: list<i32> indexThree,
    5: list<i32> indexFour,
    6: list<i32> indexFive,
    7: list<i32> indexSix,
    8: list<i32> indexSeven,
    9: list<list<i32>> awardsPool
}

struct QueryActivity {
    1: i32 activityType,
    2: i64 activityId,
    3: i64 skuId,
    4: optional i64 gourpBuyingTeamId
}

struct GeneralLimitRule {
    1:optional i32 type,   # 1.nomal; 2.one order one sku; 3.one acount one sku
    2:optional i32 coins
}

struct GeneralActivity {
    1: required i64 id,
    2: required i32 regionId,
    3: required ActivityType activityType,
    4: required i64 skuId,
    5: required i64 activityPrice = 0,
    6: required CloneSku cloneSku,
    7: required GeneralLimitRule limitRule,
    8: required i32 promiseStock,
    9: required i32 status,  #1.active  2.invalid
    10: required bool noRemissionPostage,
    11: required bool noRemissionAmount,
    12: required bool noVoucher,
    13: optional i32 stock,
    14: optional i32 lockStock,
    15: optional i32 sold,
    16: optional string sessionStartTime,
    17: optional string sessionEndTime,
    18: optional i32 groupBuyersGoals,
    19: optional i32 groupExpireDays,
    20: optional i32 groupCompletionPeriod
}

struct RedeemSku {
    1: required i64 id,
    2: required i32 regionId,
    3: required ActivityType activityType,
    4: optional i64 activityPrice = 0,
    5: required i64 skuId,
    6: required CloneSku cloneSku,
    7: required string displayTitle,
    8: required i32 coins,
    9: required i32 promiseStock,
    10: required i32 status,  #1.active  2.invalid
    11: required string createTime,
    12: optional i32 stock,
    13: optional i32 lockStock,
    14: optional i32 sold,
}

struct PagingRedeemSku{
    1: required i32 total,
    2: required list<RedeemSku> data
}

struct BatchUpdateApply {
    1: required i64 id,
    2: optional i32 promiseStock=0
}

struct BatchResult {
    1: required i64 resourceId,
    2: optional i32 code=0,
    3: optional string msg
}

struct SimpleTodayDealSku{
    1: required i64 id
    2: required i64 skuId,
    3: optional i64 listingId,
    4: optional i64 dealPrice,
    5: optional i32 dealDays,
    6: optional string startTime,
    7: optional string endTime,
}

struct PagingSimpleTodayDealSku{
    1: required i32 total,
    2: required list<SimpleTodayDealSku> dealSkus
}

struct TodayDealSku{
    1: required i64 id
    2: required i64 skuId,
    3: required i64 listingId,
    4: required i32 storeId,
    5: required string storeName,
    6: required string skuTitle,
    7: required i64 listPrice,
    8: required i64 salePrice
    9: required i64 dealPrice,
    10: required string applyTime,
    11: optional string auditTime,
    12: optional string startTime,
    13: optional string endTime,
    14: required i32 dealDays,
    15: required TodatDealApplyStatus status
}

struct PagingTodayDealSku{
    1: required i32 total,
    2: required list<TodayDealSku> dealSkus
}

struct ApplyTodayDealSku{
    1: required i64 skuId,
    2: optional i64 listingId,
    3: optional i64 dealPrice,
    4: optional i32 dealDays,
    5: optional string skuTitle,
    6: optional i64 listPrice,
    7: optional i64 salePrice,
    8: optional i32 storeId
    9: optional string storeName,
    10: optional i32 source,
    11: optional i32 regionId
}

struct todayDealHandleResult{
    1: optional i64 skuId,
    2: optional i64 todayDealId,
    3: optional i32 code=0,
    4: optional string msg="success."
}

struct SkuSoldRes {
    1: i64 skuId,
    2: i16 reStartMonth,
    3: i16 reStartDay,
    4: bool noSold=true,
    5: string sessionStartTime
}

struct PromotionRule {
    1: optional i64 priceBreak,
    2: optional i64 discount,
    3: optional bool per
}

struct Operator {
    1: optional OperatorType type,
    2: optional i64 id,
    3: optional string name
    4: optional string ip
}

struct Promotion {
    1: required i64 id,
    2: required string title,
    3: required PromotionType type,
    4: required PromotionStatus status,
    5: required PromotionRule rule,
    6: required list<i32> storeIds,
    7: required string startTime,
    8: required string endTime,
    9: required string applyTime,
    10: required string auditTime,
    11: required string canceledTime,
    12: required Operator applyAccount,
    13: required Operator auditAccount,
    14: required bool noStoreVoucher,
    15: required bool noPlatformVoucher,
    16: required bool noCoins,
    17: required i64 productCount,
    18: required i64 regionId,
    19: optional i64 storeProductCount,
    20: optional i32 limitStoreProducts  #0表示不限制，正整数表示所限制的店铺报名商品数量
}

struct PagingPromotion {
    1: required i32 total,
    2: required list<Promotion> promotions
}

struct PromotionProductMsg {
    1: required i64 id,
    2: required string title,
    3: required i64 minPrice,
    4: required i64 maxPrice
}

struct PromotionProduct {
    1: required i64 id,
    2: required i64 promotionId,
    3: required PromotionType promotionType,
    4: required PromotionProductMsg product,
    5: required i64 storeId,
    6: required PromotionProductStatus status,
    7: required Operator applyAccount,
    8: required Operator auditAccount,
    9: required string applyTime,
    10: required string auditTime,
    11: required string canceledTime,
}

struct PagingPromotionProduct {
    1: required i32 total,
    2: required list<PromotionProduct> promotionProducts
}

struct PromotionProductResult {
    1: optional i64 productId,
    2: optional i64 promotionId,
    3: optional i32 code=0,
    4: optional string msg="success."
}

struct PromotionsOfListing {
    1: i64 listingId,
    2: list<Promotion> promotions
}

struct PromotionCartItem {
    1: required i64 itemId,
    2: required i64 listingId,
    3: required i64 itemPrice,
    4: required i64 itemCount,
    5: optional i64 promotionId
}

struct DefaultPromotionOfCartItem {
    1: i64 itemId,
    2: Promotion defaultPromotion
}

struct GroupBuyingSku {
    1: optional i64 skuId,
    2: optional i64 dealPrice
}

struct GroupBuyingListing {
    1: optional i64 listingId,
    2: optional i64 regionId
    3: optional i64 storeId,
    4: optional i64 categoryId,
    5: optional list<GroupBuyingSku> skus
}

struct GroupBuyingTeamMember {
    1: optional i64 id,
    2: optional i64 skuId,
    3: optional i64 accountId,
    4: optional bool isLeader,
    5: optional i64 saleOrderId,
    6: optional GroupBuyingTeamMemberStatus status,
    7: optional string shareCode
    8: optional i64 skuDealPrice
}

struct GroupBuyingTeam {
    1: optional i64 id,
    2: optional i64 regionId,
    3: optional i64 groupBuyingId,
    4: optional i64 buyersGoals,
    5: optional i64 listingId,
    6: optional i64 leaderAccountId,
    7: optional string leaderShareCode
    8: optional list<i64> memberAccountIds,
    9: optional GroupBuyingTeamStatus status,
    10: optional string createdAt,
    11: optional string expiredAt,
    12: optional GroupBuyingTeamMember currentAccountMember
    13: optional GroupBuyingTeamMember shareCodeAccountMember
    14: optional GroupBuyingTeamMember saleOrderAccountMember
    15: optional GroupBuyingTeamState state
}

struct GroupBuying {
    1: optional i64 id,
    2: optional i16 regionId,
    3: optional i64 storeId,
    4: optional i16 tagId,
    5: optional i64 listingId,
    6: optional string startOn,
    7: optional i16 expireDays,
    8: optional GroupBuyingStatus status,
    9: optional i64 buyersGoals,
    10: optional string createdAt,
    11: optional i64 orderCount,
    12: optional string expiredOn,
    13: optional list<GroupBuyingSku> skus
    14: optional bool isHot
    15: optional string isHotAt
    16: optional i64 completionPeriod
}

struct PagingGroupBuying {
    1: optional i32 total,
    2: optional list<GroupBuying> groupBuyings
}

struct PagingGroupBuyingTeam {
    1: optional i32 total,
    2: optional list<GroupBuyingTeam> groupBuyingTeams
}

struct GroupBuyingApplyResult {
    1: optional i64 listingId,
    2: optional i64 groupBuyingId=-1,
    3: optional i32 code=0,
    4: optional string msg="success."
}

struct GroupBuyingTag {
    1:i64 id,
    2:i64 regionId,
    3:i16 index,
    4:string name,
    5:optional list<i64> categoryIds
}

struct RelatedActivitySkus{
    1:required list<SimpleActivitySku> skus
    2:optional ActivitySku activitySku,
    3:optional GeneralActivity generalActivity
}

struct BigDiscountSale{
    1:required i64 id
    2:required i64 regionId
    3:required string title
    4:required string code
    5:required string tag
    6:required string tagImage
    7:required string startAt
    8:required string endAt
    9:required BigDiscountSaleStatus status
    10:required string applyAt,
    11:required string auditAt,
    12:required string canceledAt,
    13:required Operator applyAccount,
    14:required Operator auditAccount,
    15:required i64 productCount
}

struct PagingBigDiscountSale {
    1:required i64 total
    2:required list<BigDiscountSale> bigDiscountSales
}

struct BigDiscountSaleSku {
    1:required i64 skuId
    2:required i64 dealPrice
}

struct BigDiscountSaleProductApply{
    1:required i64 listingId
    2:required string listingTitle
    3:required list<BigDiscountSaleSku> skus
}

struct BigDiscountSaleProductResult {
    1: optional i64 skuId,
    2: optional i64 BigDiscountSaleProduct=-1,
    3: optional i32 code=0,
    4: optional string msg="success."
}

struct BigDiscountSaleSku{
    1:required i64 id
    2:required i64 regionId
    4:required i64 skuId
    5:required i64 listingId
    6:required i64 storeId
    7:required i64 dealPrice
    8:required string startAt
    9:required string endAt
    10:required BigDiscountSale bigDiscountSale
}

struct BigDiscountSaleProduct{
    1:required i64 id
    2:required i64 regionId
    3:required BigDiscountSale bigDiscountSale
    4:required i64 listingId
    5:required i64 storeId
    6:required i64 minDealPrice
    7:required i64 maxDealPrice
    8:optional BigDiscountSaleProductStatus status
    9:optional string startAt
    10:optional string endAt
    11:optional string applyAt
    12:optional string canceledAt
    13:optional list<BigDiscountSaleSku> skus
    14:optional string listingTitle
}

struct PagingBigDiscountSaleProduct {
    1:required i64 total
    2:required list<BigDiscountSaleProduct> bigDiscountSaleProducts
}


struct TopicPage {
    1:i64 id,
    2:i64 regionId,
    3:string code,
    4:string title,
    5:string description,
    6:string backgroundImage,
    7:string backgroundColor,
    8:string htmlContent,
    9:TopicPageStatus status,
    10:string createTime,
    11:string expireTime,
    12:i64 operatorId,
    13:optional i64 updateOperatorId,
    14:optional string updateTime,
    15:optional string backgroundImageUrl
}

struct PagingTopicPages {
    1: required i32 total,
    2: required list<TopicPage> data
}