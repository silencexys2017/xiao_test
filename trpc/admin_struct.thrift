const i16 ERROR_ADMIN_ACCOUNT = 2000
const i16 ERROR_PERMISSION_DENIED = 2001

enum AdminUserState {
    ACTIVATED = 1,
    LOCKED = 2
}

enum AdminUserLevel {
    SUPER_ADMIN = 1,
    SENIOR_ADMIN = 2,
    GENERAL_ADMIN = 3
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
    3: required i32 regionId,
    4: required i32 localSubId, // 国家站ID
    5: required bool isRoot,
    6: required list<AdminMenu> menus,
    7: required AdminPermission permissions,
    8: optional AdminUserLevel roleLevel
}

struct AdminUser {
    1: required i32 userId,
    2: required string userName,
    3: required string trueName,
    4: required AdminUserState state,
    5: required i32 regionId,
    6: required i32 localSubId, // 国家站ID
    7: required bool isRoot,
    8: optional string lastLoginIp,
    9: optional string lastLoginTime,
    10: optional AdminUserLevel roleLevel
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

enum AdsChannel {
    OTHER = 1
    GOOGLE = 2
    FACEBOOK = 3
    SMS = 4
}

enum AdsType {
    PULL_NEW = 1
    DOWNLOAD = 2
    PRODUCT_SHOW = 3
    ACTIVATED = 4
    PROMOTION = 5
}

enum AdsTarget {
    PERFEE_APP = 1
    PERFEE_WAP = 2
    PERFEE_WEB = 3
    PERFEE_STAR = 4
}

struct AdsRunning {
    1: required i64 id,
    2: required string feeSpentDate,
    3: required string title,
    4: required AdsChannel channel,
    5: required string channelRemark,
    6: required AdsType type,
    7: required i64 regionId,
    8: required AdsTarget targetProduct,
    9: required string landingPage,
    10: required double fee,
    11: required string feeCurrency,
    12: required double feeUSD,
    13: required string remark,
    14: required string spender,
    15: required i64 creatorId,
    16: required string createdAt,
    17: required string updatedAt,
    18: required bool isDeleted,
    19: required i64 deleterId
    20: required double exchangeRateUSD
}

struct PagingAdsRunning {
    1: required i64 total
    2: required list<AdsRunning> adsRunningList
}