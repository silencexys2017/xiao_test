include "exceptions.thrift"

enum SearchType {
    KEYWORD_SEARCH = 1
    IMAGE_SEARCH = 2 
    STORE_KEYWORD_SEARCH = 3
    STORE_IMAGE_SEARCH = 4
    ES_RECOMMEND = 5
    OTHER = 6
}

enum SearchFrom {
    APP = 1
    WAP = 2
    OTHER = 3
}

enum SearchEngine {
    ES = 1
    HW = 2
}

enum SearchFeedbackEvaluation {
    MEET_EXPECTATIONS = 1
    FEWER_RESULTS = 2
    CAN_NOT_UNDERSTAND_WHAT_I_WANT = 3
    SORTING_CONFUSING = 4
    TOO_MANY_RESULTS_AND_MISMATCH = 5
}

enum SearchFeedbackState {
    NOT_PROCESSED = 1
    FOLLOWED_UP = 2
}

struct SpecValue {
    1: i64 valueId
    2: string value
}

struct Spec {
    1: i64 specId
    2: string name
    3: list<SpecValue> values
}

struct ListingResult {
    1: i64 listingId
    2: string title
    4: i64 minPrice
    5: i64 maxPrice
    6: list<Spec> specs
    7: double score
    8: i64 minListPrice
    9: i64 maxListPrice
    10: list<string> locations
    11: optional double reviewStar
}

struct SearchResult {
    1: list<ListingResult> listings
    2: i64 total
    3: list<i64> categoryIds
    4: list<i64> thingIds
    5: list<i64> spuIds
    6: i64 sessionId
}

struct StoreSearchResult {
    1: list<ListingResult> listings
    2: i64 total
    3: i64 sessionId
}

struct SpecFilterPair {
    1: i64 pid
    2: i64 pvid
}

struct Chosen {
    1: i64 position
    2: i64 listingId
}

struct hotKey {
    1: string key
    2: i64 count 
}

struct SearchSession {
    1: required i64 id
    2: required i64 regionId
    3: required i64 userId
    4: required SearchType type
    5: required string keyword
    6: required string image
    7: required i64 categoryTotal
    8: required i64 total
    9: required SearchFrom platform
    10: required string createdAt
    11: required string updatedAt
}

struct PagingSearchSession {
    1: required i64 total
    2: required list<SearchSession> searchSessionList
}

struct SearchSetting {
    1: required i64 regionId
    2: required bool isFeedbackOpened
    3: required bool isHotSearchOpened
    4: required bool isImageSearchOpened
    5: required bool isSearchLogOpened
}

struct SearchFeedback {
    1: required i64 id
    2: required i64 regionId
    3: required i64 userId
    4: required SearchType type
    5: required string keyword
    6: required string image
    7: required i64 categoryTotal
    8: required i64 total
    9: required SearchFrom platform
    10: required SearchFeedbackEvaluation evaluation
    11: required string content
    12: required SearchFeedbackState state
    13: required string createdAt
    14: required string updatedAt
}

struct PagingSearchFeedback {
    1: required i64 total
    2: required list<SearchFeedback> searchFeedbackList
}

service EsService {
    SearchResult search(
        1: i64 skip
        2: i64 size
        3: i64 region
        4: string lang
        5: string appSessionId
        6: optional i64 userId
        7: optional i64 sessionId
        8: optional string keyword
        9: optional list<i64> categoryIds
        10: optional i64 lowPrice
        11: optional i64 highPrice
        12: optional list<SpecFilterPair> specsFilter
        13: optional list<string> locations
        14: optional i64 storeId
        15: optional double minReviewStar
        16: optional double maxReviewStar
        17: optional list<i64> listingIds
        18: optional i64 sortBy
        19: optional list<i64> brandIds
        20: optional SearchFrom platform
    ) throws (
        1: exceptions.InvalidOperationException ioe,
        2: exceptions.InternalException ie
    )

    void record_chosen(
        1: i64 sessionId
        2: list<Chosen> chosen
    )

    list<hotKey> get_hot_search_suggestion(
        1: i64 region=1
        2: string time_start
        3: string time_end
        4: i64 limit
    )

    void update_hot_search(
        1: i64 region=1
        2: list<string> hotSearchKeys
    )

    list<string> get_hot_search(
        1: i64 region=1
    )

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
        14: optional list<string> locations,
        15: optional SearchFrom platform
    )

    void create_hot_search(1: i64 region_id)

    i64 create_session_for_hw_search(
        1: required i64 region,
        2: required string app_session_id,
        3: required i64 user_id,
        4: required string keyword,
        5: required i64 total,
        6: required list<i64> category_ids,
        7: required i64 low_price,
        8: required i64 high_price,
        9: required list<SpecFilterPair> specs_filter,
        10: required list<string> locations,
        11: required i64 store_id
        12: required SearchType search_type
        13: required string image
        14: required i64 category_total
        15: required SearchFrom platform
    )

    PagingSearchSession get_search_sessions (
        1: required i64 region_id
        2: optional i64 skip
        3: optional i64 limit
        4: optional string created_time_start
        5: optional string created_time_end
        6: optional list<i64> user_id_list
        7: optional string keyword
        8: optional SearchType search_type
        9: optional SearchFrom platform,
        10: optional bool is_guest
    )

    SearchSetting get_search_setting(
        1:required i64 regionId
    )

    SearchSetting update_search_setting(
        1:required i64 region_id
        2:optional bool is_feedback_opened
        3:optional bool is_hot_search_opened
        4:optional bool is_image_search_opened
        5:optional bool is_search_log_opened
    )

    SearchFeedback create_search_feedback (
        1: required i64 search_session_id
        2: required SearchFeedbackEvaluation evaluation
        3: required string content
    )

    PagingSearchFeedback get_search_feedbacks (
        1: required i64 region_id
        2: optional i64 skip
        3: optional i64 limit
        4: optional string created_time_start
        5: optional string created_time_end
        6: optional list<i64> user_id_list
        7: optional string keyword
        8: optional string content
        9: optional SearchFeedbackEvaluation evaluation
        10: optional SearchFeedbackState state
        11: optional SearchType search_type
        12: optional SearchFrom platform
    )

    void update_search_feedback(
        1: required i64 search_feedback_id,
        2: optional SearchFeedbackState state
    )
}
