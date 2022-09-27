include "exceptions.thrift"
include "constants.thrift"
 

struct AppAuthData {
    1:i64 sellerId,
    2:string appId,
    3:string appSecret
}

struct RefreshToken {
    1:i64 storeId,
    2:string refreshToken,
    3:bool expiredByHand
}

struct Oauth2Client {
    1:string clientId,
    2:string clientSecret,
    3:string clientName,
    4:string clientUri,
    5:string createdAt,
    6:list<string> grantTypes,
    7:list<string> redirectUris,
    8:list<string> responseTypes,
    9:list<string> scopes,
    10:list<string> tokenEndpointAuthMethods
}

struct Oauth2AuthorizationCode {
    1:string code
    2:string clientId,
    3:i64 sellerId,
    4:i64 storeId,
    5:string redirectUri,
    6:string responseType,
    7:string scope,
    8:string createdAt,
    9:i64 expiresIn
}

struct PlatformApp {
    1:i64 deliveryId
    2:string appKey,
    3:string appSecret
}

service CubeService {
    void create_app_id(
        1:i64 seller_id,
    )

    AppAuthData verify_app_auth(
        1:string app_id,
        2:string app_secret
    ) throws (
        1: exceptions.UnauthorizedException ue,
    )

    AppAuthData get_app_auth_by_seller_id(
        1:i64 seller_id
    ) 

    void insert_refresh_token(
        1:i64 store_id,
        2:string refresh_token
    )

    RefreshToken get_refresh_token(
        1:i64 store_id,
        2:string refresh_token
    )

    Oauth2Client get_oauth2_client_by_client_id(
        1:string client_id
    ) throws (
        1: exceptions.NotFoundException nfe
    )

    void insert_oauth2_authorization_code(
        1:string code
        2:string clientId,
        3:i64 sellerId,
        4:i64 storeId,
        5:string redirectUri,
        6:string responseType,
        7:string scope,
        8:string createdAt,
        9:i64 expiresIn
    )

    Oauth2AuthorizationCode get_oauth2_authorization_code_by_code(
        1:string code
    ) throws (
        1: exceptions.NotFoundException nfe
    )

    PlatformApp verify_platform_app(
        1:string app_key,
        2:string app_secret
    ) throws (
        1: exceptions.UnauthorizedException ue,
    )
}