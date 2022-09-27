include "exceptions.thrift"
include "inventory.thrift"
include "goods_struct.thrift"
include "warehouse.thrift"
include "property.thrift"
include "constants.thrift"

struct PackageDetail {
    1: double length,
    2: double width,
    3: double height,
    4: double weight,
    5: string unit
}

struct Sku {
    1: i64 id,
    2: i64 listingId,
    3: i64 vendorId,
    4: i64 storeId,
    5: string title,
    6: string desc,
    7: i32 priceRevision,
    8: i64 listPrice,
    9: i64 salePrice,
    10: string key,
    11: string spec,
    12: list<string> images,
    13: i32 status,
    14: list<constants.SupportedPaymentMethods> paymentMethodsMask,
    15: optional string idByVendor,
    16: optional goods_struct.IsWithBattery withBattery,
    17: optional bool withMagneto,
    18: optional bool isPowder,
    19: optional bool isCompressed,
    20: optional i64 storeCategoryId,
    21: optional string createdAt,
    22: optional string updatedAt
    23: optional i64 warehouseId
    24: optional i64 stock
    25: optional goods_struct.SkuType skuType,
    26: optional goods_struct.SkuDeriveType deriveType,
    27: optional i64 sourceSkuId,
    28: optional i64 deriveRegion
    29: optional double pCost
    30: optional string foreignName
    31: optional string chineseName
    32: optional bool liquid,
    33: optional goods_struct.PrepaymentSetting prepayment
}

struct SkuSpec {
    1: i64 pid,
    2: i64 pvid,
    3: string value,
}

struct DetailItem {
    1: string type,
    2: string content
}

struct NewSku {
    1: string title,
    2: string desc,
    3: i64 priceRegion,
    4: i64 listPrice,
    5: i64 salePrice,
    6: list<SkuSpec> specs,
    7: list<string> images,
    8: i64 inventory,
    9: i64 warehouseId,
    10: list<DetailItem> detailContent,
    11: optional list<constants.SupportedPaymentMethods> paymentMethodsMask,
    12: optional string idByVendor,
    13: required double pCost
}

struct NewSkuWithSpecsString {
    1: string title,
    2: string desc,
    3: i64 priceRegion,
    4: double listPrice,
    5: double salePrice,
    6: list<string> specs,
    7: list<string> images,
    8: i64 inventory,
    9: i64 warehouseId,
    10: list<DetailItem> detailContent,
    11: optional list<constants.SupportedPaymentMethods> paymentMethodsMask,
    12: optional string idByVendor
    13: optional double pCost
}

struct NewListing {
    1: string title,
    2: string desc,
    3: list<property.Property> props,
    4: list<property.SpecProperty> specs,
    5: i64 sellerId,
    6: i64 categoryId,
    7: i64 vendorId,
    8: i64 storeId,
    9: list<i64> regions,
    10: string lang,
    11: bool online,
    12: list<NewSkuWithSpecsString> skus,
    13: optional i64 thingId,
    14: optional i64 spuId,
    15: optional PackageDetail package,
    16: optional string idByVendor,
    17: optional goods_struct.IsWithBattery withBattery,
    18: optional bool withMagneto,
    19: optional bool isPowder,
    20: optional bool isCompressed,
    21: optional i64 storeCategoryId,
    22: optional list<string> images,
    23: optional bool liquid
    24: optional i64 brandId
}

struct Listing {
    1: i64 id,
    2: list<string> imageUrls,
    3: string title,
    4: string desc,
    5: string detailUrl,
    6: list<property.Property> props,
    7: list<property.SpecProperty> specs,
    8: list<Sku> skus,
    9: string unit,
    10: i32 status,
    11: i64 categoryId,
    12: i64 vendor,
    13: i64 storeId,
    14: list<constants.SupportedPaymentMethods> paymentMethodsMask,
    15: optional goods_struct.IsWithBattery withBattery,
    16: optional bool withMagneto,
    17: optional bool isPowder,
    18: optional bool isCompressed,
    19: optional i64 storeCategoryId,
    20: optional double stars,
    21: optional string videoUrl,
    22: optional string videoCoverUrl,
    23: optional string categoryName,
    24: optional PackageDetail package,
    25: optional string idByVendor,
    26: optional list<DetailItem> detailContent,
    27: optional i64 brandId,
    28: optional string brandName,
    29: optional bool liquid,
    30: optional goods_struct.PrepaymentSetting prepayment
}

struct SimpleListing {
    1: i64 id,
    2: i64 minPrice,
    3: i64 maxPrice,
    4: i64 minListPrice,
    5: i64 maxListPrice,
    6: string title,
    7: string imageUrl,
    8: list<string> locations,
    9: optional double reviewStar,
    10: optional i64 storeId,
    11: optional i64 categoryId
}

struct SimpleSku {
    1: i64 id,
    2: string title,
    3: string spec,
    4: string imageUrl,
    5: optional i64 listingId,
    6: optional string desc,
    7: optional string chineseName,
    8: optional string foreignName,
}

struct CartItem {
    1: i64 id,
    2: i64 listingId,
    3: i64 skuId,
    4: string title,
    5: string spec,
    6: string image,
    7: i64 listPrice,
    8: i64 salePrice,
    9: i64 dealPrice,
    10: i64 count,
    11: string timeCreated,
    12: optional string latestUpdate,
    13: bool checked,
    14: i64 storeId,
    15: i64 revisionId,
    16: i64 skuStatus,
    17: i32 activityType,
    18: i64 activityId
    19: optional string referCode
    20: optional string authorCode
    21: optional string referSource
    22: optional i64 referSourceId
    23: optional i64 promotionId
    24: optional string tempUserKey
}

struct CartSku {
    1: i64 skuId,
    2: i32 activityType,
    3: i64 activityId
}

struct Reviews {
    1: i32 id,
    2: string nick,
    3: double ratings,
    4: optional string avatar,
    5: string content,
    6: optional list<string> images,
    7: string createdAt
}

struct Feedback {
    1: i32 count,
    2: double overallRating,
    3: list<Reviews> reviews
}

struct PaymentMethod {
    1: i32 id,
    2: string name,
    3: i16 available,
    4: optional list<i64> ids,
    5: optional string reason
}

struct SpecFilterPair {
    1: i64 pid,
    2: i64 pvid
}

struct SearchFilter {
    1: list<i64> catetoryIds,
    2: list<SpecFilterPair> specsFilter
}

struct SimpleCategory {
    1: i64 id,
    2: string name
}

//后台
struct Image{
    1: string imageName,
    2: string imageUrl
}

struct SubCategory {
    1: i64 id,
    2: string name,
    3: optional bool isDisplay,
    4: string chineseName,
    5: string foreignName,
}

struct Category {
    1: string name,
    2: i64 id,
    3: optional list<SubCategory> subCategories
    4: optional i64 depth
    5: optional i64 parent
}
struct SubCategoryName {
    1: i64 id,
    2: string chineseName,
    3: string foreignName,
}

struct CategoryName {
    1: optional list<SubCategoryName> category_name_data
}
struct RelatedTing {
    1: i64 id,
    2: string name
}

struct Thing {
    1: string alphabetName,
    2: list<RelatedTing> relatedThings
}

struct RelatedSpu {
    1: i64 id,
    2: string name
}

struct Spu {
    1: string alphabetName,
    2: list<RelatedSpu> relatedSpus
}

struct Prop {
    1: i64 id,
    2: string name
}

struct Spec {
    1: i64 id,
    2: string name
}

struct ProAndSpec {
    1: list<Prop> props,
    2: list<Spec> specs
}

struct AttributeValue {
    1: i64 id,
    2: string value
}

struct SKU {
    1: string title,
    2: string desc,
    3: string specAggregation,
    4: i32 quantity,
    5: list<string> images,
    6: i64 salePrice,
    7: i64 listPrice,
    8: list<AttributeValue> extendSpecValue
}

struct Attribute {
    1: i64 id,
    2: string name,
    3: list<AttributeValue> values
    4: optional list<string> extendValues
}

struct ListingInfo {
    1: string dependentType,
    2: string name,
    3: i64 id,
    4: string title,
    5: string desc,
    6: string detailContent,
    7: list<Attribute> props,
    8: list<Attribute> specs,
    9: list<SKU> skus
}

struct ListingSummary {
    1: i64 id,
    2: i64 category_id,
    3: list<property.Property> props,
    4: list<property.SpecProperty> specs,
    5: string detail_url,
    6: list<Sku> skus,
    7: optional double stars,
    8: optional string videoUrl,
    9: optional string videoCoverUrl,
}

struct SkuNormalModel {
    1: Sku sku,
    2: ListingSummary listing,
    3: PackageDetail package,
    4: list<inventory.SkuInventoryItem> inventories
}

struct SkuStockDetail {
    1: Sku sku,
    2: PackageDetail package,
    3: list<inventory.SkuInventoryItem> inventories
}

struct NaviTagWithCat {
    1: i64 id,
    2: i64 region,
    3: i64 priority,
    4: string name,
    5: list<SimpleCategory> categories,
    6: optional string status,
    7: optional i64 revision_id,
    8: optional i64 listing_count
}

struct NaviTagNoCat {
    1: i64 id,
    2: i64 priority,
    3: string name
}

struct ListingOfNaviTag {
    1: i64 index,
    2: i64 listingId,
    3: i64 minPrice,
    4: i64 maxPrice,
    5: i64 minListPrice,
    6: i64 maxListPrice,
    7: string image,
    8: string title,
}

struct NaviTagListings {
    1: i64 id,
    2: i64 priority,
    3: string name,
    4: i64 count,
    5: list<ListingOfNaviTag> listings
}

struct RevisionTagResult {
    1: i64 tagId,
    2: string name,
    3: i64 revisionId,
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
    18: optional i64 storeCategoryId
}

struct FilterListingsResult {
    1: i64 total,
    2: list<ProductListing> listings
}

struct SkuPreviewInfo {
    1: i64 id,
    2: i64 listingId,
    3: i64 storeId,
    4: i64 vendorId,
    5: string previewUrl
}

struct ListingPreviewInfo {
    1: i64 id,
    2: i64 storeId,
    3: i64 vendorId,
    4: string previewUrl
}

struct CategoryDetail {
    1: i64 id,
    2: string name,
    3: string path,
    4: i64 depth,
    5: i64 parent,
    6: double weight,
    7: bool via_air,
    8: i64 with_battery,
    9: bool is_leaf,
    10: string icon_small,
    11: string icon_large,
    12: i64 latest_update,
    13: map<i64, string> props,
    14: map<i64, string> specs,
    15: i64 listing_count,
    16: i64 avl_listing_count,
    17: i64 sku_count,
    18: i64 avl_sku_count,
    19: optional list<CategoryDetail> children,
    20: optional bool isDisplay,
    21: optional string chineseName,
    22: optional string foreignName,
}

struct SkuInventory {
    1: i64 skuId,
    2: string skuCode,
    3: warehouse.Warehouse warehouse,
    4: i64 vendorId,
    5: i64 inventory
}

struct SkuVendorInfo {
    1: i64 sku_id,
    2: i64 vendor,
    3: optional string id_by_vendor
}

struct SkuSearchingResult {
    1: i64 total,
    2: i64 limit,
    3: optional list<i64> sku_ids
}

struct Chosen {
    1: i64 position
    2: i64 listingId
}

struct OrderCount {
    1: i64 sku_id,
    2: i64 count
}

struct BasicSelective {
    1: i64 id
    2: string name
    3: string type
    4: string status
    5: i64 SOId
    6: i64 listingCount
    7: i64 listingId
    8: string source
    9: string createdAt
    10: string updatedAt
}

struct FilterSelectiveResult {
   1: i64 total
   2: list<BasicSelective> selectives
}

struct SelectiveListing {
    1: i64 listingId
    2: string title
    3: string image
    4: i64 status
    5: i64 minPrice
    6: i64 maxPrice
    7: optional i64 minListPrice
    8: optional i64 maxListPrice
    9: optional i64 skuCount
    10: optional string desc
    11: optional string createdAt

}

struct SelectiveSceneThing {
    1: string name
    2: i64 index
    3: SelectiveListing mainListing
    4: list<SelectiveListing> alterListings
}

struct BasicSelectiveSceneThing {
    1: string name
    2: i64 index
    3: i64 mainListing
    4: list<i64> alterListings
}

struct GeneralSelective {
    1: i64 id
    2: string name
    3: string status
    4: string type
    5: optional string source
    6: optional string image
    7: optional bool imageVisible
    8: optional list<SelectiveSceneThing> things
    9: optional list<SelectiveListing> listings
    10: optional SelectiveListing listing
    11: optional i64 articleId
    12: optional i64 SOId
    13: optional string createdAt
}

struct FilterFullListingsResult {
    1: i64 total,
    2: list<Listing> listings
}

struct NormalAndDeriveSkus {
    1: list<Sku> skus       // 根据入参sku_ids返回的所有sku
    2: list<Sku> normalSkus // skus中的派生sku的源sku
    3: list<Sku> deriveSkus // skus中的原生sku的派生sku
}

struct ListingWeight {
    1: i64 listingId
    2: double weight
}

struct SellerSiteQuery {
    1: optional i64 baseStoreRegionId
    2: optional bool isExpanded
}

struct SearchResultListing {
    1: i64 id,
    2: i64 minPrice,
    3: i64 maxPrice,
    4: i64 minListPrice,
    5: i64 maxListPrice,
    6: string title,
    7: string imageUrl,
    8: list<string> locations,
    9: optional double reviewStar,
    10: optional i64 storeId,
    11: optional i64 categoryId
    12: optional string reqId
}

struct SearchResult {
    1: list<Category> categoryFilters,
    2: list<property.Property> specsFilters,
    3: list<SearchResultListing> listings,
    4: list<string> locationFilters,
    5: i64 total,
    6: i64 sessionId
    7: optional string reqId
}

struct storeCategoryAgg {
    1: required i64 storeCategoryId
    2: required i64 listingCount
}

struct StoreSearchResult {
    1: list<SearchResultListing> listings
    2: i64 total
    3: i64 sessionId
    4: list<storeCategoryAgg> storeCategoryAggs
    5: optional string reqId
}

service GoodsService {
    Listing getListing(
        1:i64 id,
        2:i64 region,
        3:string lang,
        4:optional bool isStars,
    ) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InternalException ie
    ),

    list<DetailItem> getDetail(
        1:i64 listingId,
        2:i64 skuId,
        3:string lang
    ) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InternalException ie
    ),

    Listing getListingUnlimit(
        1:i64 id,
        2:i64 region,
        3:string lang
        4:optional i64 base_region
    ) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InternalException ie
    ),

    list<SimpleListing> getSimpleListingsByCategoryId(
        1:i64 categoryId,
        2:i64 lastId,
        3:i32 limit,
        4:i64 region,
        5:string lang
    ) throws (
        1:exceptions.InternalException ie
    ),

    list<ProductListing> getProductListingsByIds(
        1:list<i64> ids,
        2:i64 region,
        3:string lang,
        4:optional i64 storeId,
        5:optional bool is_return_sku_ids,
        6:optional bool is_including_offline
    ) throws (
        1:exceptions.InternalException ie
    ),

    list<SimpleListing> getSimpleListingsByIds(
        1:list<i64> ids,
        2:i64 region,
        3:string lang,
        4:optional bool is_stars
        5:optional bool is_including_offline
    ) throws (
        1:exceptions.InternalException ie
    ),

    list<SimpleSku> getSimpleSkusByIds(
        1:list<i64> ids,
        2:i64 region,
        3:string lang
    ) throws (
        1:exceptions.InternalException ie
    ),

    SearchResult search(
        1:i32 skip,
        2:i32 size,
        3:i64 region,
        4:string lang,
        5:string appSessionId,
        6:optional i64 userId,
        7:optional i64 sessionId,
        8:optional string keywords,
        9:optional i64 lowPrice,
        10:optional i64 highPrice,
        11:optional list<i64> catetoryIds,
        12:optional list<SpecFilterPair> specsFilter,
        13:optional list<string> locations,
        14:optional string delivery,
        15:optional i64 storeId,
        16: optional double minReviewStar,
        17: optional double maxReviewStar
        18: optional list<i64> listingIds
        19: required string countrySite
        20: optional i64 sortBy
        21: optional list<i64> excludingStoreIds
        22: optional string imageQuery
        23: optional list<i64> brandIds
        24: optional bool isRecommended
        25: optional goods_struct.SearchFrom platform
        26: optional string imageQueryFileName
    ) throws (
        1:exceptions.InternalException ie
    ),

    StoreSearchResult storeSearch(
        1: i64 skip
        2: i64 size
        3: i64 region
        4: string lang
        5: string appSessionId
        6: i64 storeId
        7: optional i64 userId
        8: optional i64 sessionId
        9: optional string keyword
        10: optional list<i64> storeCategoryIds
        11: optional i64 lowPrice
        12: optional i64 highPrice
        13: optional list<SpecFilterPair> specsFilter
        14: optional list<string> locations
        15: required string countrySite
        16: optional goods_struct.SearchFrom platform
    ) throws (
        1:exceptions.InternalException ie
    ),

    void record_chosen(
        1: i64 sessionId
        2: list<Chosen> chosen
    )

    void deleteAllOwnedCartItems(
        1:i64 accountId,
        2:i64 region
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie
    ),

    void delete_owned_cart_items_by_skuids(
        1: i64 account_id,
        2: i64 region,
        3: list<CartSku> skus
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie
    ),

    i32 addToCart(
        1:i64 accountId,
        2:i64 skuId,
        3:i32 count,
        4:i64 region,
        5:i32 activityType,
        6:i64 activityId
        7: optional string referCode
        8: optional string authorCode
        9: optional string referSource
        10: optional i64 referSourceId
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie,
        3:exceptions.NotFoundException ne
    ),

    i32 add_temp_cart(
        1:string temp_user_key,
        2:i64 sku_id,
        3:i32 count,
        4:i64 region_id,
        5:i32 activity_type,
        6:i64 activity_id
        7: optional string refer_code
        8: optional string author_code
        9: optional string refer_source
        10: optional i64 refer_source_id
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie,
        3:exceptions.NotFoundException ne
    ),

    list<CartItem> getCartList(
        1:i64 accountId,
        2:i64 region,
        3:string lang,
        4:i64 lastId,
        5:optional i32 limit
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie
    ),

    list<CartItem> get_temp_cart_list(
        1:string temp_user_key,
        2:i64 region_id,
        3:string language,
        4:i64 last_id,
        5:optional i32 limit
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie
    ),

    i32 getCartNum(
        1:i64 accountId,
        2:i32 region
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie
    ),

    i32 get_temp_cart_total(
        1:i32 region_id,
        2:string temp_user_key
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie
    ),

    list<CartItem> getCartItems(
        1:list<i64> ids,
        2:string lang
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie
    ),

    CartItem get_cart_item(
        1:i64 item_id,
        2:string language,
        3:i64 account_id
    ) throws (
        1:exceptions.NotFoundException ne
    ),

    CartItem get_temp_cart_item(
        1:i64 item_id,
        2:string language,
        3:string temp_user_key
    ) throws (
        1:exceptions.NotFoundException ne
    ),

    CartItem editCartItem(
        1:i64 id,
        2:string lang
        3:optional i32 count,
        4:optional bool checked,
        5:optional i64 promotion_id
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie,
        3:exceptions.NotFoundException ne
    ),

    CartItem edit_temp_cart_item(
        1:i64 item_id,
        2:string language
        3:optional i32 count,
        4:optional bool checked,
        5:optional i64 promotion_id
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie,
        3:exceptions.NotFoundException ne
    ),

    void deleteCartItems(
        1:list<i64> ids,
        2:i64 account_id
    ) throws (
        1:exceptions.InvalidOperationException ioe
    ),

    void delete_temp_items(
        1:list<i64> ids,
        2:string temp_user_key
    ) throws (
        1:exceptions.InvalidOperationException ioe
    ),

    void change_to_formal_cart(
        1:string temp_user_key,
        2:i64 account_id
    )

    i64 get_cart_item_count(
        1:i64 account_id,
        2:i32 region_id,
        3:i64 sku_id,
        4:i32 activity_type,
        5:i64 activity_id
    ),

    i64 get_temp_cart_item_count(
        1:string temp_user_key,
        2:i32 region_id,
        3:i64 sku_id,
        4:i32 activity_type,
        5:i64 activity_id
    ),

    list<string> getHotSearchKeys() throws (
        1:exceptions.InternalException ie
    ),

    void updateHistorySearchKeys(
        1: i64 accountId,
        2: string key
    ) throws (
        1:exceptions.InternalException ie
    ),

    list<string> getHistorySearchKeys(1: i64 accountId) throws (
        1:exceptions.InternalException ie
    ),

    i16 clearHistorySearchKeys(1: i64 accountId) throws (
        1:exceptions.InternalException ie
    )

    list<Feedback> getRecentReviews(
        1: i64 listingId,
        2: i32 limit
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<PaymentMethod> getPaymentMethod(1: list<i32> itemIds) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    // 后台
    void display_category_list(
        1:i64 region_id,
        2:list<i64> category_ids
    ),

    list<Category> getCategoryTree() throws (
        1: exceptions.InvalidOperationException ioe
    ),

    void update_category_name(
        1: list<SubCategoryName> sub_category_names,
    ),

    list<Category> getCategoriesByDepth(
        1: i64 depth,
        2: optional i64 parent
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<Category> getCategoriesByIds(
        1: list<i64> category_ids,
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<Category> getLeafCategories() throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<Thing> getThings() throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<Spu> getSpus() throws (
        1: exceptions.InvalidOperationException ioe
    ),

    ProAndSpec getCatSpecsAndPros(1: i64 id) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    ProAndSpec getThingSpecsAndPros(1: i64 id) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    ProAndSpec getSpuSpecsAndPros(1: i64 id) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    i64 releaseProducts(
        1: ListingInfo listingInfo,
        2: i16 status
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<SkuStockDetail> get_sku_stock_details(
        1: list<i64> ids,
        2: i64 region,
        3: string lang
    ) throws (
        1: exceptions.InternalException ie,
        2: exceptions.NotFoundException nfe
    ),

    SkuStockDetail get_sku_stock_detail(
        1: i64 id,
        2: i64 region,
        3: string lang
    ) throws (
        1: exceptions.InternalException ie
    ),

    SkuNormalModel get_sku_normal_model(
        1: i64 id,
        2: i64 region,
        3: string lang,
        4: optional bool isStars,
    ) throws (
        1: exceptions.InternalException ie,
        2: exceptions.NotFoundException nfe
    ),

    list<SimpleCategory> getTopSBPCategories(1: i64 region) throws (
        1: exceptions.InternalException ie
    ),

    // Navi Tag management
    NaviTagWithCat getNaviTagDetail(
        1: i64 tagId
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<NaviTagWithCat> get_navitags_detail(
        1: i64 region
    )

    string get_navitag_status(
        1: i64 tag_id
    )

    NaviTagWithCat createNaviTag(
        1: i64 region
        2: i64 priority
        3: string name
        4: list<i64> categories
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    NaviTagWithCat updateNaviTag(
        1: i64 tagId
        2: i64 region
        3: i64 priority
        4: string name
        5: list<i64> categories
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    i32 removeNaviTag(
        1: i64 tagId
        2: i64 region
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<NaviTagNoCat> getNaviTagsNoCat(
        1: i64 region
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<NaviTagWithCat> getNaviTagsWithCat(
        1: i64 region
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    NaviTagListings getNaviTagListings(
        1: i64 id
        2: i64 lastIndex
        3: i64 limit
        4: i64 region
        5: optional i64 skip
        6: optional bool isTop
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.NotFoundException nfe
    ),

    list<RevisionTagResult> revisionListingsOfNaviTags() throws (
        1: exceptions.InvalidOperationException ioe
    ),

    NaviTagWithCat enqueue_revision_navitag(
        1: i64 tag_id
    )

    i64 updateListingVisible(
        1: i64 listingId
        2: i32 visible
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<ProductListing> updateTopListingsOfNaviTag(
        1: i64 tagId
        2: i64 region
        3: list<i64> topListings
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    list<ProductListing> getTopListingsOfNaviTag(
        1: i64 tagId
        2: i64 region
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    // product list
    FilterListingsResult filterListings(
        1: i64 regionId
        2: optional i64 skip
        3: optional i64 limit
        4: optional i64 categoryId
        5: optional i64 listingId
        6: optional i64 skuId
        7: optional string title
        8: optional string createTimeStart
        9: optional string createTimeEnd
        10: optional i64 vendorId
        11: optional i64 storeId
        12: optional bool deleted
        13: optional string updatedTimeStart
        14: optional string updatedTimeEnd
        15: optional bool online
        16: optional bool ascending
        17: optional i32 storeCategoryId
        18: optional list<i64> excludedSkuIds
        19: optional list<i64> excludedListingIds
        20: optional bool isReturningSkuIds
        21: optional i64 brandId
        22: optional SellerSiteQuery sellerSiteQuery
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    string export_goods(
        1: i64 regionId
        2: i64 storeId
        3: optional i64 categoryId
        4: optional i64 listingId
        5: optional i64 skuId
        6: optional string title
        7: optional string createTimeStart
        8: optional string createTimeEnd
        9: optional i32 storeCategoryId
        10: optional string export
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    )

    Sku updateSkuStatus(
        1: i64 skuId,
        2: i32 status,
        3: i64 region
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    Sku updateSkuPrice(
        1: i64 listingId,
        2: i64 skuId,
        3: i64 listPrice,
        4: i64 salePrice,
        5: i64 region
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    void openapi_update_sku_price(
        2: i64 sku_id,
        5: i64 region_id,
        3: optional i64 list_price,
        4: optional i64 sale_price
    ),

    i32 getListingStatus(1: i64 listingId, 2:i64 regionId) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    SkuPreviewInfo getPreviewInfoBySkuId(1:i64 skuId, 2:i64 regionId) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InternalException ie
    ),

    ListingPreviewInfo getPreviewInfoByListingId(
        1:i64 listingId, 2:i64 regionId
    ) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InternalException ie
    ),

    i16 getVendorIdBySkuId(1:i64 skuId) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InternalException ie
    ),

    CategoryDetail get_category_by_id(
        1: i64 id,
        2: string lang
    ) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InternalException ie
    ),

    list<CategoryDetail> get_categories(
        1: i64 region,
        2: string lang
        3: optional i64 parent_id,
        4: optional bool recursive,
        5: optional bool is_filter_region
    ) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InternalException ie
    ),

    list<Sku> getSkusByIds(
        1:list<i64> ids,
        2:i64 region,
        3:string lang
    ) throws (
        1:exceptions.InternalException ie
        2:exceptions.NotFoundException nfe
    ),

    SkuInventory getSkuInventory(
        1: i64 skuId,
        2: i64 region,
        3: optional i64 cityId
    ) throws (
        1: exceptions.InternalException ie
        2: exceptions.NotFoundException nfe
    ),

    list<SkuInventory> getSkuInventories(
        1: list<i64> skuIds,
        2: i64 region,
        3: optional i64 cityId
    ) throws (
        1: exceptions.InternalException ie
        2: exceptions.NotFoundException nfe
    ),

    SkuInventory update_sku_inventory(
        1: i64 sku_id,
        2: i64 warehouse_id,
        3: i64 inventory
    ) throws (
        1: exceptions.InternalException ie
    ),

    void openapi_update_sku_inventory(
        1: i64 sku_id,
        2: i64 inventory,
        3: i64 region_id
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    void bulk_update_sku_warehouse(
        1: i64 listing_id,
        2: i64 warehouse_id
    ) throws (
        1: exceptions.InternalException ie,
        2: exceptions.InvalidOperationException ioe
    ),

    list<warehouse.Warehouse> getWarehouseByVendor(
        1: i64 vendorId
    ) throws (
        1: exceptions.InternalException ie
    ),

    i64 get_warehouse_by_listing(
        1: i64 listing_id
    ),

    property.Property get_property_values(
        1: i64 property_id
        2: bool private_only,       // 仅获取Seller或Store自有属性值
        3: i64 seller_id,
        4: i64 store_id,
        5: string lang
    ) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InvalidOperationException ioe,
        3:exceptions.InternalException ie
    ),

    property.PropertyValue append_property_value(
        1: i64 property_id,
        2: string value,
        3: string lang,
        4: property.PropertyValueSource source,
        5: optional i64 seller_id,
        6: optional i64 store_id
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    ),

    Listing create_listing(
        1: string title,
        2: string desc,
        3: list<property.Property> props,
        4: list<property.SpecProperty> specs,
        6: i64 categoryId,
        7: i64 vendorId,
        8: i64 storeId,
        9: list<i64> regions,
        10: string lang,
        11: bool online,
        12: list<NewSku> skus,
        13: optional i64 thingId,
        14: optional i64 spuId,
        15: optional PackageDetail package,
        16: optional string idByVendor,
        17: optional goods_struct.IsWithBattery withBattery,
        18: optional bool withMagneto,
        19: optional bool isPowder,
        20: optional bool isCompressed,
        21: optional i64 storeCategoryId,
        22: optional list<string> images,
        23: optional string video,
        24: optional bool isFromVendor
        25: optional i64 brandId
        26: optional bool liquid
    ),

    goods_struct.ExcelTaskProgress get_progress_for_excel_import(
        1: i64 seller_id,
        2: i64 store_id
    )

    string bulk_create_listing(
        1: list<NewListing> listings
    )

    Sku get_sku_info(
        1: i64 sku_id,
        2: i64 region,
        3: optional string lang
    ) throws (
        1:exceptions.NotFoundException nfe
        2:exceptions.InternalException ie
    ),

    Sku get_sku_info_unlimit(
        1: i64 sku_id,
        2: i64 region,
        3: optional string lang,
        4: optional i64 base_region
    ) throws (
        1:exceptions.NotFoundException nfe
        2:exceptions.InternalException ie
    ),

    Listing update_listing(
        1: i64 listing_id,
        2: string title,
        3: string desc,
        4: string lang,
        5: i64 region,
        6: list<constants.SupportedPaymentMethods> paymentMethodsMask,
        7: optional list<DetailItem> details,
        8: optional PackageDetail package,
        9: optional goods_struct.IsWithBattery withBattery,
        10: optional bool withMagneto,
        11: optional bool isPowder,
        12: optional bool isCompressed,
        13: optional i64 storeCategoryId,
        14: optional i64 categoryId
        15: optional i64 brandId
        16: optional bool isFromVendor
        17: optional bool liquid
    ),

    void update_listings_order_count(
        1: list<OrderCount> order_count,
    ),

    void update_listings_real_sales(
        1: list<OrderCount> order_count,
    ),

    Sku update_sku(
        1: i64 skuId,
        3: string title,
        4: string desc,
        5: list<string> imageUrls,
        6: string lang,
        7: i64 region,
        8: optional list<constants.SupportedPaymentMethods> paymentMethodsMask,
        9: optional list<DetailItem> details,
        10: optional string idByVendor
        11: optional bool isFromVendor
    ),

    void set_store_category_to_default(
        1: i64 default_id,
        2: i64 deleted_id
    )

    Sku appendSku(
        1: i64 listingId,
        2: list<property.PropertyId> props,
        3: string title,
        4: string desc,
        5: i64 listPrice,
        6: i64 salePrice,
        7: list<string> imageUrls,
        8: string lang,
        9: i64 region,
        10: i64 inventory,
        11: bool online,
        12: list<constants.SupportedPaymentMethods> paymentMethodsMask,
        13: optional list<DetailItem> details,
        14: optional string idByVendor
    ),

    list<SimpleListing> get_most_recent_listings(
        1: i32 limit,
        2: i64 region,
        3: string lang
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    ),

    void update_shoppo_price(
        1: string shoppo_sku_id,
        2: optional double price,
        3: optional double msrp,
        4: optional string weight
    ),

    void update_shoppo_status(
        1: string shoppo_sku_id,
        2: optional bool enabled,
        3: optional i64 inventory
    ),

    list<SkuVendorInfo> get_sku_vendor_info(
        1: list<i64> sku_ids
    ),

    void record_vendor_notification(
        1: string vendor,
        2: string content
    ),

    list<SimpleListing> get_similar_price_listings(
        1: i64 listing_id,
        2: i64 limit,
        3: i64 region,
        4: string lang
    ) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InternalException ie
    ),

    void vvic_product_modify(
        1: string item_vid,
        2: string update_type,
        3: list<string> changed_fields
    ),

    map<i64,i64> get_categories_by_listing_ids(
        1: list<i64> listing_ids
    ),

    string get_faq_by_listing_id(
        1: i64 listing_id
    ),

    bool update_stocks(
        1: string source_type,
        2: string source,
        3: list<inventory.SkuStockItem> items
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    bool add_reservations(
        1: string source_type,
        2: string source,
        3: list<inventory.SkuStockItem> items
    ),

    bool clean_reservations(
        1: string source_type,
        2: string source,
        3: list<inventory.SkuStockItem> items
    ),

    bool decrease_reservations_and_stocks(
        1: string source_type,
        2: string source,
        3: list<inventory.SkuStockItem> items
    ),

    bool increase_stocks(
        1: string source_type,
        2: string source,
        3: list<inventory.SkuStockItem> items
        4: inventory.SkuInventoryLogType inventory_log_type
    ),

    inventory.SkuInventories get_inventories_by_sku(
        1: i64 sku_id,
        2: i64 region,
        3: optional i64 city_id
    ),

    oneway void revision_navitag(
        1: i64 tag_id
    ),

    SkuSearchingResult search_skus_with_title(
        1: string keywords,
        2: i64 limit,
        3: i64 region,
        4: string lang
    ) throws (
        1:exceptions.InternalException ie
    ),

    list<CategoryDetail> walk_category_tree(
        1: i64 region,
        2: string lang,
        3: optional i64 depth
    ) throws (
        1:exceptions.InternalException ie
    ),

    goods_struct.PagingSkuReview get_sku_reviews(
        1: optional i64 region_id,
        2: optional i64 account_id,
        3: optional i64 sku_id,
        4: optional i64 listing_id,
        5: optional list<i32> status,
        6: optional list<i32> source_type,
        7: optional i32 score_min,
        8: optional i32 score_max,
        9: optional string start_time,
        10: optional string end_time,
        11: optional i32 skip,
        12: optional i32 limit,
        13: optional bool istop_first,
        14: optional list<i32> score_filter,
        15: optional bool has_picture,
        16: optional bool has_content,
        17: optional i64 store_id,
        18: optional bool has_seller_replied,
        19: optional bool sort_by_is_empty
        20: optional bool sort_by_score
    ),

    goods_struct.ListingReviewCount get_listing_review_count(
        1: required i32 region_id,
        2: required i64 listing_id
    )

    goods_struct.Review get_review(
        1: optional i64 sku_review_id,
        2: optional i64 account_id,
        3: optional i64 ship_order_detail_id
    ) throws (
        1: exceptions.NotFoundException nfe
    ),

    void audit_review(
        1: i64 sku_review_id,
        2: i64 auditor_id,
        3: bool is_top,
        4: optional i32 status,
        5: optional i32 reward_coin
    ) throws (
        1: exceptions.NotFoundException nfe,
        2: exceptions.InvalidOperationException ioe
    ),

    goods_struct.ListingReviewTotal get_listing_review_total(
        1: i64 region_id,
        2: i64 listing_id,
    ) throws (
        1: exceptions.NotFoundException nfe
    ),

    goods_struct.Review admin_add_review(
        1: i64 region_id,
        2: i64 store_id,
        3: i64 sku_id,
        4: i64 listing_id,
        5: bool is_top,
        6: i64 auditor_id
        7: optional string content,
        8: optional list<string> attach_names,
        9: optional i64 sku_score,
        10: optional string create_at
    ),

    goods_struct.Review add_review(
        1: i64 region_id,
        2: i64 account_id,
        3: i64 ship_order_detail_id,
        4: i64 sku_score,
        5: bool is_anonymous,
        6: optional string content,
        7: optional list<string> attach_names,
        8: optional i32 delivery_service_score,
        9: optional i32 store_service_score,
        10: optional i32 rider_score,
        11: optional list<string> attach_video_names
    ) throws (
        1: exceptions.NotFoundException nfe,
        2: exceptions.InvalidOperationException ioe
    ),

    void order_complete_notice(
        1: goods_struct.OrderCompleteNotice notice
    ),

    void check_order_review(
        1: goods_struct.OrderCompleteNotice notice
    ),

    goods_struct.PagingNotReview get_not_reviews(
        1: i64 region_id,
        2: i64 account_id,
        3: optional i32 skip,
        4: optional i32 limit
    ),

    goods_struct.OrderCompleteSku get_not_review(
        1: i64 region_id,
        2: i64 account_id,
        3: i64 ship_order_detail_id
    ) throws (
        1: exceptions.NotFoundException nfe,
        2: exceptions.InvalidOperationException ioe
    )

    goods_struct.StoreReview get_store_review(
        1: i64 region_id,
        2: i64 account_id,
        3: i64 sale_order_id
    ) throws (
        1: exceptions.NotFoundException nfe
    ),

    goods_struct.ReviewReply get_review_reply(
        1: i64 review_reply_id,
    )

    goods_struct.ReviewReply create_review_reply(
        1: i64 sku_review_id,
        2: string content,
        3: optional bool is_seller,
        4: optional i64 seller_id,
        5: optional i64 store_id,
        6: optional i64 account_id,
        7: optional string account_name,
        8: optional i64 target_id,
        9: optional string target_name,
        10: optional bool is_anonymous
    ) throws (
        1: exceptions.NotFoundException nfe
    )

    goods_struct.PagingReviewReply get_replys_of_review(
        1: i64 review_id,
        2: i64 skip,
        3: i64 limit
    )

    void delete_review_reply(
        1: i64 review_reply_id
    )

    goods_struct.ReviewLikesData update_sku_review_likes (
        1: i64 account_id,
        2: i64 review_id,
        3: goods_struct.ReviewLikeClick like
    ) throws (
        1: exceptions.NotFoundException nfe
    )

    goods_struct.ReviewLikesData get_sku_review_likes (
        1: i64 sku_review_id,
        2: optional i64 account_id
    )

    list<goods_struct.SkuReviewLikeStatus> get_sku_reviews_like_status (
        1: list<i64> sku_review_ids,
        2: optional i64 account_id
    )

    double get_store_stars(
        1: i64 storeId
    )

    list<goods_struct.StoreStars> get_store_stars_by_stroe_ids(
        1: list<i64> store_ids
    )

    i64 get_account_review_count(
    1: i64 region_id, 2: i64 account_id, 3: goods_struct.ReviewType review_type)

    list<warehouse.Warehouse> get_warehouses() throws (
        1: exceptions.InternalException ie
    ),

    warehouse.Warehouse get_warehouse_by_id(1: i64 id) throws (
        1:exceptions.NotFoundException nfe,
        2: exceptions.InternalException ie
    ),

    list<warehouse.Warehouse> get_warehouses_by_ids(
        1: list<i64> ids
    ) throws (
        1:exceptions.NotFoundException nfe,
        2: exceptions.InternalException ie
    ),

    // 获取可用的备货仓列表
    list<warehouse.Warehouse> get_storage_warehouses(
        1: i64 region_id
    ) throws (
        1: exceptions.InternalException ie
    ),

    // 获取店铺可以使用的仓库列表
    list<warehouse.Warehouse> get_usable_warehouses_for_store(
        1: i64 region_id,
        2: i64 seller_id,
        3: i64 store_id
    ) throws (
        1: exceptions.InternalException ie
    ),

    list<warehouse.Warehouse> get_warehouses_for_store(
        1: optional i16 region_id, 2: optional i32 seller_id,
        3: optional i32 store_id, 4: optional bool enabled,
        5: optional warehouse.WarehouseRole role),
    // region_id: 表示仓库所在

    // 获取所有店铺自有虚拟仓创建申请
    list<warehouse.WarehouseApplication> get_dummy_applications(
        1: optional warehouse.WarehouseApplicationState state,
    ) throws (
        1: exceptions.InternalException ie
    )

    // 获取指定店铺自有虚拟仓申请（含共享）
    list<warehouse.WarehouseApplication> get_dummy_applications_of_store(
        1: i64 region_id,
        2: i64 seller_id,
        3: i64 store_id
        4: optional warehouse.WarehouseApplicationState state
    ) throws (
        1: exceptions.InternalException ie
    )

    // 清除所有卖家自有虚拟仓创建申请（仅代测试用例使用）
    void clear_dummy_applications_of_seller(1: i64 seller_id) throws (
        1: exceptions.InternalException ie
    )

    // 申请创建卖家自有虚拟仓
    warehouse.WarehouseApplication apply_dummy_warehouse(
        1: i64 region_id,
        2: i64 seller_id,
        3: i64 store_id,
        4: string warehouse_name,
        5: string location,
        6: bool seller_sharing
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    )

    // 接受卖家自有虚拟仓申请
    void approve_dummy_application(
        1: i64 application_id,
        2: i64 operator_id
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    )

    // 拒绝卖家自有虚拟仓申请
    void reject_dummy_appliation(
        1: i64 application_id,
        2: i64 operator_id,
        3: string reason
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    )

    // 获取所有备货仓使用申请
    list<warehouse.StorageWarehouseApplication> get_storage_applications() throws (
        1: exceptions.InternalException ie
    )

    // 清除所有卖家备货仓创建申请（仅代测试用例使用）
    void clear_storage_applications_of_seller(1: i64 seller_id) throws (
        1: exceptions.InternalException ie
    )

    // 申请使用备货仓
    list<warehouse.StorageWarehouseApplication> apply_storage_warehouse(
        1: i64 region_id,
        2: i64 seller_id,
        3: i64 store_id,
        4: list<i64> warehouse_id_list
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    )

    // 接受备货仓使用申请
    void approve_storage_application(
        1: i64 application_id,
        2: i64 operator_id
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    )

    // 拒绝备货仓使用申请
    void reject_storage_application(
        1: i64 application_id,
        2: i64 operator_id,
        3: string reason
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    )

    // 设置仓库支持的支付方式
    void set_warehouse_payment_methods(
        1: i64 warehouse_id,
        2: list<constants.SupportedPaymentMethods> payment_methods,
        3: i64 operator_id
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    )

    // 申请使用平台公用仓
    warehouse.Warehouse apply_public_warehouse(
        1: i64 region_id,
        2: i64 seller_id,
        3: i64 store_id,
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    )

    bool batch_delete_listings(
        1: list<i64> listing_ids,
        2: i64 region_id
        3: optional i64 store_id
    ) throws (
        1: exceptions.InvalidOperationException ioe
    )

    bool batch_offline_listings(
        1: list<i64> listing_ids,
        2: i64 region_id
        3: optional i64 store_id
    )

    FilterSelectiveResult filter_selectives(
        1: i64 regionId
        2: i64 skip
        3: i64 limit
        8: optional string createTimeStart
        9: optional string createTimeEnd
        10: optional string selective_type
    )

    GeneralSelective get_selective(
        1: i64 selective_id
        2: string selective_type
        3: i64 region
    ) throws (
        1: exceptions.NotFoundException nfe
        2: exceptions.InvalidOperationException e
    )

    void create_selective_scene(
        1: string name
        2: bool imageVisible
        3: string source
        4: list<BasicSelectiveSceneThing> things
        5: optional string image
        6: i64 region_id
    ) throws (
        1: exceptions.InternalException e
    )

    void create_selective_thing(
        1: string name
        2: bool imageVisible
        3: string source
        4: list<i64> listings
        5: optional string image
        6: i64 region_id
    ) throws (
        1: exceptions.InternalException e
    )

    void create_selective_brand(
        1: string name
        2: bool imageVisible
        3: string source
        4: list<i64> listings
        5: optional string image
        6: i64 region_id
    ) throws (
        1: exceptions.InternalException e
    )

    void create_selective_product(
        1: string name
        2: string source
        3: i64 listingId
        4: i64 region_id
    ) throws (
        1: exceptions.InternalException e
    )

    void create_selective_single_from_review(
        1: string name
        2: string account_name,
        3: string invite_code,
        4: i64 review_id,
        5: i64 so_id,
        6: i64 listing_id,
        7: string source
    ) throws (
        1: exceptions.InternalException e,
        2: exceptions.NotFoundException nfe
    )

    void update_selective_scene(
        1: i64 scene_id
        2: i64 region
        3: optional string name
        4: optional string status
        5: optional string image
        6: optional bool imageVisible
        7: optional list<BasicSelectiveSceneThing> things
        8: optional string source
    ) throws (
        1: exceptions.InternalException e
    )

    void update_selective_thing(
        1: i64 thing_id
        2: i64 region
        3: optional string name
        4: optional string status
        5: optional string image
        6: optional bool imageVisible
        7: optional list<i64> listings
        8: optional string source
    ) throws (
        1: exceptions.InternalException e
    )

    void update_selective_brand(
        1: i64 brand_id
        2: i64 region
        3: optional string name
        4: optional string status
        5: optional string image
        6: optional bool imageVisible
        7: optional list<i64> listings
        8: optional string source
    ) throws (
        1: exceptions.InternalException e
    )

    void update_selective_product(
        1: i64 product_id
        2: i64 region
        3: optional string name
        4: optional string status
        5: optional i64 listingId
        6: optional string source
    ) throws (
        1: exceptions.InternalException e
    )

    void update_selective_single (
        1: i64 single_id
        2: optional string name
        3: optional string status
    ) throws (
        1: exceptions.InternalException e
    )

    void update_selective_multi (
        1: i64 multi_id
        2: optional string status
    ) throws (
        1: exceptions.InternalException e
    )

    list<GeneralSelective> get_selective_scene_thing_brand(
        1: i64 limit
        2: i64 skip
        3: i32 region
    )

    list<GeneralSelective> get_selective_product_single_multi(
        1: i64 limit
        2: i64 skip
        3: list<string> type_lsit
        4: i32 region
    )

    bool check_selective_single_by_review_id(
        1: i64 review_id
    )

    goods_struct.FullEditListingReturn edit_full_listing(
        1: i64 region,
        2: i64 listing_id,
        3: string title,
        4: string desc,
        5: string video,
        6: list<string> images,
        7: i32 warehouse_id,
        8: i32 store_category_id,
        9: double weight,
        10: goods_struct.IsWithBattery with_battery,
        11: bool with_magneto,
        12: bool is_powder,
        13: bool is_compressed,
        14: list<i32> payment_methods,
        15: list<goods_struct.FullEditSku> skus
        16: list<DetailItem> detail_content
        17: optional bool online,
        18: optional string lang,
        19: optional i64 brand_id
        20: optional bool liquid
    ) throws (
        1: exceptions.InvalidOperationException ioe
    )

    FilterFullListingsResult filter_full_listings(
        1: i64 region_id
        2: i64 skip
        3: i64 limit
        4: optional string title
        5: optional string create_time_start
        6: optional string create_time_end
        7: optional i64 store_id
        8: optional bool deleted
        9: optional bool online
        10: optional bool ascending
        11: optional i32 store_category_id
        12: optional bool detail
    ) throws (
        1: exceptions.InvalidOperationException ioe
    ),

    goods_struct.Article create_perfee_article(
        1: i32 region_id,
        2: i64 account_id,
        3: string account_name,
        4: string invite_code,
        5: goods_struct.ArticleType article_type
        6: string title,
        7: string cover,
        8: goods_struct.ProductType product_type,
        9: list<goods_struct.ArticleContent> content_list,
        10: i32 product_count,
        11: list<string> product_ids,
        12: string source_id
    )

    goods_struct.Article update_perfee_article(
        1: i64 id,
        2: optional string title,
        3: optional string cover,
        4: optional goods_struct.ProductType product_type,
        5: optional i32 product_count,
        6: optional list<string> product_ids,
        7: optional list<goods_struct.ArticleContent> content_list,
    )

    goods_struct.Article update_perfee_article_status(
        1: i64 id,
        2: goods_struct.ArticleStatus status,
        3: goods_struct.ArticleSelectiveStatus selective_status,
        4: i64 region_id=1
    )

    goods_struct.Article get_perfee_article_by_id(
        1: i64 id
    ) throws (
        1: exceptions.NotFoundException nfe
    )

    goods_struct.ArticleReply create_article_reply(
        1: i64 article_id,
        2: string content,
        3: optional bool is_seller,
        4: optional i64 seller_id,
        5: optional i64 store_id,
        6: optional i64 account_id,
        7: optional string account_name,
        8: optional i64 target_id,
        9: optional string target_name,
        10: optional bool is_anonymous
    ) throws (
        1: exceptions.NotFoundException nfe
    )

    goods_struct.PagingArticleReply get_replys_of_article(
        1: i64 article_id,
        2: i64 skip,
        3: i64 limit
    )

    goods_struct.ArticleLikesData update_article_likes (
        1: i64 account_id,
        2: i64 article_id,
        3: goods_struct.ReviewLikeClick like
    ) throws (
        1: exceptions.NotFoundException nfe
    )

    goods_struct.ArticleLikesData get_article_likes (
        1: i64 article_id,
        2: optional i64 account_id
    )

    void inc_reply_order_likes_of_article(
        1: i64 article_id,
        2: optional i16 likes,
        3: optional i16 dislikes,
        4: optional i16 reply_count,
        5: optional i16 order_count,
    )

    void inc_pv_uv_of_article(
        1: i64 article_id,
        2: optional i64 account_id
    )

    void batch_update_payment_method(
        1: list<i64> listing_ids,
        2: list<constants.SupportedPaymentMethods> payment_methods,
        3: optional i64 store_id
    )

    goods_struct.DeriveSkuChecking check_derive_sku (
        1: i64 sku_id,
        2: i16 derive_region
    ) throws (
        1: exceptions.NotFoundException nfe
    )

    Sku create_derive_sku(
        1: i64 sku_id,
        2: goods_struct.SkuDeriveType derive_type,
        3: i32 derive_region,
        4: i64 stock
        5: i32 warehouse_id
    ) throws (
        1: exceptions.InvalidOperationException ioe
        2: exceptions.NotFoundException nfe
    )

    goods_struct.PagingSimpleDeriveSku get_simple_derive_skus(
        1: i32 derive_region,
        2: i32 skip,
        3: i32 limit,
        4: optional i64 listing_id,
        5: optional i64 sku_id,
        6: optional i64 derive_sku_id,
        7: optional goods_struct.SkuDeriveType derive_type,
        8: optional string title,
        9: optional string created_time_start
        10: optional string created_time_end
        11: optional i64 store_id
        12: optional i64 stock_gte
        13: optional i64 stock_lte
        14: optional string stock_latest_updated_at_start
        15: optional string stock_latest_updated_at_end
        16: optional bool is_including_stock_logs
    )

    # 返回值为 派生SKU 的列表
    list<Sku> get_derive_skus(
        1: list<i64> normal_sku_ids, # 原生SKU的id列表
        2: i16 derive_region # 派生SKU的所在区域
        3: optional bool is_return_prepayment
    ) throws (
        1:exceptions.InternalException ie
    ),

    Sku get_derive_sku(
        1: i64 normal_sku_id,
        2: i16 derive_region
    ) throws (
        1:exceptions.InternalException ie
        2: exceptions.NotFoundException nfe
    ),

    NormalAndDeriveSkus get_normal_and_derive_skus(
        1: list<i64> sku_ids, # SKU的id列表
        2: i16 derive_region # SKU的所在区域
    ) throws (
        1:exceptions.InternalException ie,
        2:exceptions.NotFoundException nfe
    ),

    warehouse.Warehouse get_returned_warehouse_by_region(
        1: i16 region_id
    ) throws (
        1: exceptions.NotFoundException nfe
    )

    list<ListingWeight> get_weight_of_listings(
        1: list<i64> listing_ids
    )

    goods_struct.PriceOperationProgress price_expand(
        1: required i64 store_id
        2: required i64 base_region_id
        3: required i64 target_region_id
        4: required double exchange_rate_of_cny
        5: required double first_trip_shipping
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    goods_struct.PriceOperationProgress get_price_expand_progress(
        1: i64 store_id
    )

    void price_expand_for_listing(
        1: required i64 listing_id
        2: required i64 progress_id
        3: required i64 base_region_id
        4: required i64 target_region_id
        5: required double exchange_rate_of_cny
        6: required double first_trip_shipping
        7: required double exchange_rate_usd_to_cny
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    goods_struct.PriceOperationProgress price_clearing(
        1: required i64 base_region_id
        2: required i64 target_region_id
        3: required i64 store_id
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    goods_struct.PriceOperationProgress get_price_clearing_progress(
        1: i64 store_id
    )

    void price_clearing_for_listing(
        1: required i64 listing_id
        2: required i64 progress_id
        3: required i64 region_id
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )


    void update_aex_skus_price_in_queue(
        1: i64 region_id,
        2: i64 store_id,
        3: i64 category_id,
        4: double margin,
        5: double exchange,
        6: double global_shipping_postage_rate,
        7: double local_delivery_postage
    )

    i64 update_skus_price_in_queue(
        1: required i64 region_id,
        2: required i64 store_id,
        3: list<i64> listing_ids,
        4: list<i64> sku_ids,
        5: i64 category_id,
        6: bool online,
        7: string title
        8: i64 list_price
        9: i64 sale_price
        10: double percentage
    )

    void update_progress_for_price_update(
        1: i64 progress_id,
        2: bool is_completed
    )

    # brand
    goods_struct.BrandSetting get_brand_settings (
        1:required i64 region_id
    )

    goods_struct.BrandSetting update_brand_settings (
        1:required i64 region_id
        2:required bool app_show
        3:required bool web_show
        4:required bool more_show
    )

    goods_struct.PagingBrand get_brands (
        1: optional i64 skip,
        2: optional i64 limit,
        3: optional string name,
        4: optional i64 category_id
        5: optional bool is_hot
        6: optional bool is_shown
        7: optional i64 region_id
    )
    
    void create_brand (
        1: required string logo,
        2: required string name,
        3: required string name_cn,
        4: required list<i64> category_ids,
    )

    void update_brand (
        1: required i64 id
        2: optional list<i64> category_ids
        3: optional bool is_deleted,
        4: optional bool is_hot,
        5: optional i64 index,
        6: optional goods_struct.BrandLinkType link_type,
        7: optional string link_value,
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    list<goods_struct.Parameter> get_parameter_list(1: i32 region_id, 2: string param_module)

    goods_struct.Parameter get_parameter(
        1: i32 region_id, 2: string param_module, 3: string name)
    throws (1:exceptions.NotFoundException nfe)

    void set_parameters(1: list<goods_struct.SetParameter> parameters)

    void set_parameter(1: goods_struct.SetParameter parameter, 2: i64 region_id)

    goods_struct.ProductPostage get_product_postage(
        1: i32 region_id, 2: i64 listing_id)

    void set_product_postage(
        1: i32 region_id, 2: i64 store_id, 3: i64 listing_id,
        4: goods_struct.PostageStrategyType postage_strategy_type, 
        5: i32 operator_id, 6: optional i64 postage=0, 
        7: optional list<goods_struct.AreaPostage> area_postage=[])

    goods_struct.StorePostage get_store_postage(
        1: i32 region_id, 2: i64 store_id)

    void set_store_postage(
        1: i32 region_id, 2: i64 store_id, 3: i64 postage,
        4: list<goods_struct.AreaPostage> area_postage=[], 5: bool is_free_ship,
        6: i64 free_ship_order_amount, 7: i32 operator_id)

    oneway void delete_listings_of_store (
        1: required i64 store_id
        2: required list<i64> region_ids
    )

    goods_struct.ExchangeRate get_exchange_rate (
        1: required i64 region_id
    ) throws (1:exceptions.NotFoundException nfe)

    goods_struct.RecommendedListings get_recommended_listings (
        1: required i64 region_id, 
        2: required string country_site,
        3: optional i64 sub_scenario, 
        4: optional string device_id, 
        5: optional string os_platform, 
        6: optional i64 account_id,
        7: optional i64 skip, 
        8: optional i64 limit, 
        9: optional list<i64> listing_ids,
        10: optional list<i64> sku_ids, 
        11: optional list<i64> third_category_ids
        12: optional string temp_user_key
    ) throws (
        1:exceptions.InternalException ie
    )

    goods_struct.HWSearchSetting get_hw_search_setting ()

    void batch_update_listing_store_category(
        1: required list<i64> listing_ids
        2: required i64 store_category_id
    )
    
    goods_struct.TopSaleAutomaticSettings get_top_sale_automatic_settings(
        1: required i64 region_id
    )

    goods_struct.TopSaleAutomaticSettings update_top_sale_automatic_settings(
        1: required i64 region_id
        2: optional goods_struct.TopSaleOrderType order_type
        3: optional goods_struct.TopSaleFrequencyType frequency_type
        4: optional goods_struct.TopSaleOrderTimeType order_time_type
        5: optional i64 number
        6: optional bool update_top_sale_now
        7: optional i64 operator_id
    )

    list<goods_struct.TopSaleProduct> get_top_sale_products (
        1: required i64 region_id
        2: optional i64 skip
        3: optional i64 limit
        4: optional goods_struct.TopSaleProductStatus status
        5: optional goods_struct.TopSaleProductType type
    )

    list<goods_struct.TopSaleProduct> add_new_top_sale_products (
        1: required i64 region_id
        2: required list<i64> listing_ids
        3: required goods_struct.TopSaleProductType type
        4: optional i64 operator_id
    )

    void create_sku_inventory_log(
        1: required i64 sku_id
        2: required inventory.SkuInventoryLogType log_type
        3: required i64 stock_change
        4: required i64 current_stock
    )

    list<inventory.SkuInventoryLog> get_sku_inventory_logs(
        1: required i64 sku_id
        2: optional string created_time_gte
        3: optional string created_time_lt
    )

    list<warehouse.Warehouse> get_new_warehouses(
        1: optional string start_time, 2: optional string end_time,
        3: optional i32 last_warehouse_id
    )

    list<goods_struct.Category> get_new_categories(
        1: optional string start_time, 2: optional string end_time,
        3: optional i32 last_category_id
    )

    void update_goods_brands(
        1: list<i64> listing_ids,
        2: i32 brand_id,
    )

    goods_struct.PrepaymentSetting update_listing_repayment(
        1: i64 listing_id,
        2: i16 region_id,
        3: goods_struct.PrepaymentSetting prepayment
    )

    list<goods_struct.GoodsPrepaymentSetting> get_skus_prepayment_setting(
        1: list<i64> sku_ids,
        2: i16 region_id
    )

    void update_warehouse_config(
        1: required i64 warehouse_id
        2: optional list<constants.SupportedPaymentMethods> payment_methods
    )
 
    list<constants.SupportedPaymentMethods> get_warehouse_payment_methods (
        1: required i64 warehouse_id
    ) throws (
        1:exceptions.NotFoundException nfe
    )
}
