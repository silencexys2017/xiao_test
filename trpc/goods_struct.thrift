const map<string, string> HW_SEARCH_GOODS_PRICE_ASC = {"field": "goods_price", "order": "asc"}
const map<string, string> HW_SEARCH_GOODS_PRICE_DESC = {"field": "goods_price", "order": "desc"}
const map<string, string> HW_SEARCH_ORDER_COUNT_ASC = {"field": "order_count", "order": "asc"}
const map<string, string> HW_SEARCH_ORDER_COUNT_DESC = {"field": "order_count", "order": "desc"}

const map<i16, map<string, string>> HW_SEARCH_SORT_BY = {
    1: HW_SEARCH_GOODS_PRICE_ASC,
    2: HW_SEARCH_GOODS_PRICE_DESC,
    3: HW_SEARCH_ORDER_COUNT_ASC,
    4: HW_SEARCH_ORDER_COUNT_DESC
}

const string HW_HOME_RECOMMENDED = "Home_Recommended_for_you"
const string HW_CATEGORY_RECOMMENDED = "Category_Recommended_for_you"
const string HW_PRODUCTSHOP_RECOMMENDED = "ProductShop_Recommended_for_you"
const string HW_PRODUCT_RECOMMENDED = "Product_Recommended_for_you"
const string HW_CART_RECOMMENDED = "Cart_Recommended_for_you"
const string HW_ORDER_RECOMMENDED = "Order_Recommended_for_you"
const string HW_COLLECT_RECOMMENDED = "Collect_Recommended_for_you"

const i64 TOP_SALE_DEFAULT_NUMBER = 60
const string UPDATE_AUTOMATIC_TOP_SALE_PERIODICALLY = "update_automatic_top_sale_periodically"
const string UPDATE_AUTOMATIC_TOP_SALE_IMMEDIATELY = "update_automatic_top_sale_immediately"

const map<i16, string> HW_RECOMMEND_SCENARIO = {
    1: HW_HOME_RECOMMENDED,
    2: HW_CATEGORY_RECOMMENDED,
    3: HW_PRODUCTSHOP_RECOMMENDED,
    4: HW_PRODUCT_RECOMMENDED,
    5: HW_CART_RECOMMENDED,
    6: HW_ORDER_RECOMMENDED,
    7: HW_COLLECT_RECOMMENDED
}

enum HWRecommendScenario {
    HOME_RECOMMENDED = 1
    CATEGORY_RECOMMENDED = 2
    PRODUCTSHOP_RECOMMENDED = 3
    PRODUCT_RECOMMENDED = 4
    CART_RECOMMENDED = 5
    ORDER_RECOMMENDED = 6
    COLLECT_RECOMMENDED = 7
}

enum ReviewType {
    un_review = 1, // 未评价
    reviewed = 2   // 已评价
}

enum IsWithBattery {
    no = 0,
    yes = 1,
    partially = 2
}

enum ExcelTaskcCompleted {
    no = 0,
    yes = 1, 
}

enum ReviewLikeClick {
    like = 1,
    dislike = 2
}

enum ReviewLikeStatus {
    like = 1,
    dislike = 2,
    no_status = 3
}

enum SkuType {
    normal = 1,
    derive = 2
}

enum SkuDeriveType {
    stocking = 1,
    returned = 2
}

enum PriceOperationStatus {
    WAITING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
}

enum HWDataOptType {
    INSERT = 1
    UPDATE = 2
}

enum TopSaleOrderType {
    ALL = 1
    PAID = 2
    COMPELETED =3
}

enum TopSaleFrequencyType {
    DAILY = 1
    WEEKLY = 2
    MONTHLY =3
}

enum TopSaleOrderTimeType {
    ALL = 1
    YESTERDAY = 2
    LAST_SEVEN_DAYS = 3
    LAST_TEN_DAYS = 4
    LAST_FIFTEEN_DAYS = 5
    LAST_THIRTY_DAYS = 6
    LAST_SIXTY_DAYS = 7
    LAST_NINETY_DAYS = 8
}

enum TopSaleProductType {
    MANUAL = 1
    AUTOMATIC = 2
}

enum TopSaleProductStatus {
    ACTIVE = 1
    INACTIVE = -1
}

enum BrandLinkType {
    DEFAULT = 1
    H5 = 2
    ANDROID = 3
}

enum SearchFrom {
    APP = 1
    WAP = 2
    OTHER = 3
}

enum PrepaymentState {
    PLATFORM = 1,
    PRODUCT = 2,
    DISABLE = -1
}

struct PrepaymentSetting {
    1: PrepaymentState state,
    2: double prepaymentRatio,
    3: bool isSupportMergeCommit
}

struct GoodsPrepaymentSetting {
    1: PrepaymentState state,
    2: double prepaymentRatio,
    3: bool isSupportMergeCommit,
    4: optional i64 listingId,
    5: optional i64 skuId
}

struct ExcelTaskProgress {
    1: ExcelTaskcCompleted status,
    2: i64 total,
    3: i64 completed,
}

struct ProductListing {
    1: i64 listingId,
    2: i64 skuCount,
    3: i64 minPrice,
    4: i64 maxPrice,
    5: string image,
    6: string title,
    7: i32 status,
    8: string weight,
    9: string createdAt,
    10: i64 minListPrice,
    11: i64 maxListPrice,
    12: optional i64 categoryId,
    13: optional string categoryName,
    14: optional i64 storeId,
    15: optional list<i64> skuIds
    16: optional i64 brandId
    17: optional string brandName
}

struct ReviewTotal {
    1: required i32 count,
    2: required i32 score,
    3: required i32 oneStarCount,
    4: required i32 twoStarCount,
    5: required i32 threeStarCount,
    6: required i32 fourStarCount,
    7: required i32 fiveStarCount,
}

struct StoreReviewTotal {
    1: required i64 regionId,
    2: required i64 storeId,
    3: required ReviewTotal storeService,
    4: required ReviewTotal deliveryService,
    5: required ReviewTotal riderService,
}

struct ListingReviewTotal {
    1: required i64 regionId,
    2: required i64 listingId,
    3: required i32 imageCount,
    4: required ReviewTotal skuService,
}

struct StoreReview {
    1: required i64 id,
    2: required i64 regionId,
    3: required i32 storeServiceScore,
    4: required i32 deliveryServiceScore,
    5: required i32 riderScore,
    6: required string createAt,
    7: optional i64 accountId,
    8: optional i64 saleOrderId,
    9: optional i64 storeId
}

struct SkuReview {
    1: required i64 id,
    2: required i64 storeReviewId,
    3: required i64 regionId,
    4: required i64 accountId,
    5: required i64 saleOrderId,
    6: required i64 shipOrderDetailId,
    7: required i64 storeId,
    8: required i64 listingId,
    9: required i64 skuId,
    10: required i32 status,  # 1.not audit；2.audited；3.audit failed, 4.deleted
    11: required bool isAnonymous,
    12: required i32 sourceType, # 1.from customer; 2.from admin; 3.from auto
    13: required i32 skuScore,
    14: required string createAt,
    15: optional string content,
    16: optional list<string> attachNames,
    17: optional i32 rewardCoin,
    18: optional bool isTop,
    19: optional i64 auditorId,
    20: optional string auditTime,
    21: optional bool hasSellerReplied,
    22: optional i32 sellerRepliedId,
    23: optional i32 likes,
    24: optional i32 dislikes,
    25: optional i32 replyCount,
    26: optional list<string> attachVideoNames
}


struct PagingSkuReview {
    1: required i32 total,
    2: required list<SkuReview> data,
    3: required double listingStars
}

struct ListingReviewCount{
    1: required double goodRate,
    2: required i32 total,
    3: required i32 good,
    4: required i32 average,
    5: required i32 bad,
    6: required i32 hasImage
}

struct Review {
    1: required SkuReview sku_review,
    2: optional StoreReview store_review
}

struct OrderCompleteSku{
    1: required i64 id,
    2: required i64 regionId,
    3: required i64 accountId,
    4: required i64 saleOrderId,
    5: required i64 shipOrderDetailId,
    6: required i64 storeId,
    7: required i64 listingId,
    8: required i64 skuId,
    9: required i32 status # 1. not review; 2.reviewed
}

struct PagingNotReview {
    1: required i32 total,
    2: required list<OrderCompleteSku> data
}

struct ShipOrderDetail{
    1: required i64 id,
    2: required i64 skuId,
    3: optional i64 listingId
}

struct ShipOrder{
    1: required i64 saleOrderId,
    2: required i64 storeId,
    3: required list<ShipOrderDetail> shipOrderDetails
}

struct OrderCompleteNotice {
    1: required i64 accountId,
    2: required i64 regionId,
    3: required list<ShipOrder> shipOrders,
}

struct StoreStars {
    1: required i64 storeId,
    2: required double stars,
}

struct ReviewReply {
    1: i64 id,
    2: i64 skuReviewId,
    3: string content, 
    4: bool isSeller,
    5: i64 sellerId,
    6: i64 storeId,
    7: i64 accountId,
    8: string accountName,
    9: i64 targetId,
    10: string targetName,
    11: bool isDeleted,
    12: string craetedAt,
    13: string updatedAt,
    14: bool isAnonymous
}

struct PagingReviewReply {
    1: i32 total,
    2: list<ReviewReply> replys,
}

struct ReviewLikesData {
    1: i32 likes,
    2: i32 dislikes,
    3: optional ReviewLikeStatus likeStatus,
    4: optional i16 incLikes,
    5: optional i16 incDislikes,
}

struct SkuReviewLikeStatus {
    1: i64 skuReviewId,
    2: ReviewLikeStatus likeStatus
}

struct FullEditSkuSpecValue {
    1: i64 id,
    2: string value,
}

struct FullEditSkuSpec {
    1: i64 id,
    2: string name,
    3: FullEditSkuSpecValue value
}

struct FullEditSku {
    1: i64 id,
    2: string idByVendor,
    3: i64 listPrice,
    4: i64 salePrice,
    5: i64 stock,
    6: string mainImage
    7: bool isDeleted,
    8: list<FullEditSkuSpec> specs
    9: double pCost
}

struct FullEditListingReturn {
    1: i64 id,
    2: i32 status,
    3: i32 storeCategoryId
}

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

enum PostageStrategyType {
    ALL_AREAS = 1
    ONE_BY_ONE = 2
    SPECIAL = 3
}

struct ArticleContentData{
    1: required string name
    2: required string value
}

struct ArticleContent{
    1: required i32 index,
    2: required ArticleContentType type,
    3: required string content,
    4: required list<ArticleContentData> data,
}

struct Article{
    1: required i64 id,
    2: required i64 regionId,
    3: required i64 accountId,
    4: required string accountName,
    5: required string inviteCode,
    6: required ArticleType type,
    7: required string sourceId,
    9: required string title
    10: required string cover,
    11: required list<ArticleContent> contentList
    12: required ProductType productType,
    13: required i32 productCount,
    14: required list<string> productIds,
    15: required ArticleStatus status,
    16: required ArticleSelectiveStatus selectiveStatus,
    17: required i32 orderCount,
    18: required i32 pv,
    19: required i32 uv,
    20: required i32 likes,
    21: required i32 dislikes,
    22: required i32 replyCount,
    23: required string createdTime,
    24: required string postedTime,
    25: required string updatedTime,
}

struct ArticleReply {
    1: i64 id,
    2: i64 articleId,
    3: string content, 
    4: bool isSeller,
    5: i64 sellerId,
    6: i64 storeId,
    7: i64 accountId,
    8: string accountName,
    9: i64 targetId,
    10: string targetName,
    11: bool isDeleted,
    12: string craetedAt,
    13: string updatedAt,
    14: bool isAnonymous
}

struct PagingArticleReply {
    1: i32 total
    2: list<ArticleReply> replys,
}

struct ArticleLikesData {
    1: i32 likes,
    2: i32 dislikes,
    3: optional ReviewLikeStatus likeStatus
}

struct SimpleDeriveSku {
    1: i64 id,
    2: string title,
    3: string spec,
    4: i64 sourceSkuId,
    5: i64 listingId,
    6: i16 deriveRegionId,
    7: i32 stock,
    8: SkuDeriveType deriveType,
    9: string createdAt
    10: optional i64 storeId
    11: optional string stockLatestUpdatedAt
    12: optional i64 stockChange
}

struct PagingSimpleDeriveSku {
    1: i32 total,
    2: list<SimpleDeriveSku> deriveSkus
}

struct DeriveSkuChecking {
    1: bool isOK,
    2: string reason
}

struct PriceRegion {
    1: i64 regionId ,
    2: string region,
    3: string currencySymbol,
    4: string currency,
    5: double exchangeRateOfCNY,
    6: i64 firstTripShipping
}

struct GrossProfitRateOfPrice {
    1: i64 salePrice
    2: double grossProfitRate
}

struct PriceOperationProgress {
    2: PriceOperationStatus status,
    3: i64 total,
    4: i64 completed,
}

struct Category {
    1: i64 id,
    2: string name,
    3: optional string path,
    4: optional i16 depth
}

struct BrandSetting {
    1: i64 regionId,
    2: bool appShow,
    3: bool webShow,
    4: bool moreShow
}

struct Brand {    
    1: required i64 id,
    2: required string logo,
    3: required string name,
    4: required string nameCN,
    5: optional list<Category> categories,
    6: optional i64 skuCount,
    7: optional string createdAt,
    8: optional string updatedAt
    9: optional bool isHot
    10: optional i64 index
    11: optional BrandLinkType linkType
    12: optional string linkValue
}

struct PagingBrand {
    1: required i64 total,
    2: required list<Brand> brands
}

struct SetParameter {
    1: required string name,
    2: required string value,
    3: required string paramModule,
    4: optional i32 index,
    5: optional i16 regionId
}

struct Parameter {
    1: required i64 id,
    2: required i32 regionId,
    3: required string name,
    4: required string value,
    5: required string dataType,
    6: required string paramModule,
    7: required i16 index
}

struct AreaPostage {
    1: i64 id,
    2: i64 postage
}

struct ProductPostage {
    1: i64 id,
    2: i32 regionId,
    3: i64 storeId,
    4: i64 listingId,
    5: PostageStrategyType postageStrategyType,
    6: string createdAt,
    7: string updatedAt,
    8: i64 operatorId,
    9: optional i64 postage,
    10: optional list<AreaPostage> areaPostage=[]
}

struct StorePostage {
    1: i64 id,
    2: i32 regionId,
    3: i64 storeId,
    4: i64 postage,
    5: PostageStrategyType postageStrategyType,
    6: string createdAt,
    7: string updatedAt,
    8: i64 operatorId,
    9: list<AreaPostage> areaPostage=[],
    10: bool isFreeShip,
    11: i64 freeShipOrderAmount
}

struct ExchangeRate {
    1: required double regionId
    2: required double exchangeRateToUSD
}

struct RecommendedListing {
    1: required i64 listingId
    2: required i64 skuId
    3: required string algId
}

struct RecommendedListings {
    1: required list<RecommendedListing> listings
    2: required string reqId
}

struct HWSearchSetting {
    1: required bool isSearchOpened
    2: required bool isRecommendOpened
}

struct TopSaleAutomaticSettings {
    1: required i64 regionId,
    2: required TopSaleOrderType orderType
    3: required TopSaleFrequencyType frequencyType
    4: required TopSaleOrderTimeType orderTimeType
    5: required i64 number
}

struct TopSaleProduct {
    1: required i64 id,
    2: required i64 regionId,
    3: required i64 listingId
    4: required TopSaleProductType type
    5: required TopSaleProductStatus status
    6: required ProductListing listing
}
