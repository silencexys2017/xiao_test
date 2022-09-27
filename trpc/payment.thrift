struct SslNoticeParams {
    1: required string status,
    2: required string amount,
    3: required string bank_tran_id,
    4: required string base_fair,
    5: required string currency,
    6: required string currency_amount,
    7: required string currency_rate,
    8: required string currency_type,
    9: required string store_id,
    10: required string tran_date,
    11: required string tran_id,
    12: required string value_a,
    13: required string value_b,
    14: required string value_c,
    15: required string value_d,
    16: required string verify_sign,
    17: required string verify_key,
    18: optional string card_brand,
    19: optional string card_issuer,
    20: optional string card_issuer_country,
    21: optional string card_issuer_country_code,
    22: optional string card_no,
    23: optional string card_type,
    24: optional string val_id,
    25: optional string risk_level,
    26: optional string risk_title,
    27: optional string store_amount,
    28: optional string verify_sign_sha2,
    29: optional string error,
    30: optional string card_sub_brand
}

struct SSLTrans {
    1: optional string bankTranId,
    2: optional string baseFair,
    3: optional string cardBrand,
    4: optional string cardIssuer,
    5: optional string cardIssuerCountry,
    6: optional string cardIssuerCountryCode,
    7: optional string cardNo,
    8: optional string cardType,
    9: optional string currencyAmount,
    10: optional string currencyRate,
    11: optional string currencyType,
    12: optional string emiAmount,
    13: optional string emiDescription,
    14: optional string emiInstalment,
    15: optional string emiIssuer,
    16: optional string gwVersion,
    17: optional bool isValidated,
    18: optional string paidAt,
    19: optional string payAmount,
    20: optional string riskLevel,
    21: optional string riskTitle,
    22: optional string settlementCurrency,
    23: optional string storeAmount,
    24: optional string tranDate,
    25: optional string valId,
    26: optional string validatedOn,
    27: optional string tranId
}

struct BkashTrans {
    1: string agreementID,
    2: string payerReference,
    3: string amount,
    4: string currency,
    5: string customerMsisdn,
    6: string paymentID,
    7: string transactionStatus,
    8: string paymentExecuteTime,
    9: string merchantInvoiceNumber,
    10: string intent,
    11: string trxID
}

enum PayTransStatus {
    UNPAID = 1,
    PAID = 2
}

enum Gateway {
    SSL = 1,
    BKASH = 2,
    VIRTUAL = -1,
    KBZ = 3
}

enum TranRefundStatus {
    NO_REFUND = 1,
    PART_REFUNDED = 2,
    ALL_REFUNDED = 3
}

struct RefundTransaction {
    1: string originalTrxID,
    2: string refundTrxID,
    3: i32 refundSlipId,
    4: optional string refundAmount,
    5: optional string bankTranId,
    6: optional string charge
}

struct PayTransactions {
    1: required string tranId,
    2: required PayTransStatus status,
    3: required Gateway gatewayId,
    4: required i64 billId,
    5: required i64 payBillId,
    6: required i32 amount,
    7: required string currency,
    8: required string createdAt,
    9: required string expiredAt,
    10: optional string paidAt,
    11: optional SSLTrans sslData,
    12: optional BkashTrans bkashData,
    13: optional TranRefundStatus refundStatus,
    14: optional list<RefundTransaction> refundTrx
}

enum PaySessionStatus {
    NEW_CREATE = 1,
    PAID = 2,
    FAILED = -1
}

enum RefundState {
    NO_REFUND = 1,
    REFUNDED = 2,
    PROCESSING = 3,
    CANCEL = -1
}

struct KBZSession {
    1: string total_amount,
    2: string merch_order_id,
    3: string trans_currency,
    4: string mm_order_id
}

struct PaySession {
    1: string id,
    2: PaySessionStatus state,
    3: string currency,
    4: i64 amount,
    5: i64 billId,
    6: i64 payBillId,
    7: Gateway gatewayId,
    8: string createdAt,
    9: optional string platform,
    10: optional KBZSession kbzSession
}