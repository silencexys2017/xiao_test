exception InvalidOperationException {
  1: i32 code
  2: string msg
}

exception InternalException {
  1: i32 code
  2: string msg
}

exception DatabaseException {
  1: i32 code
  2: string msg
}

exception NotFoundException {
  1: i32 code
  2: string msg
}

exception UnauthorizedException {
  1: i32 code
  2: string msg
}

// dnxapi 服务错误码、错误信息
const i32 CODE_INFORMATION_TARGETS_ERROR = 5001
const string MSG_INFORMATION_TARGETS_ERROR = "Targets error."
const i32 CODE_INFORMATION_DIMENTIONS_ERROR = 5002
const string MSG_INFORMATION_DIMENTIONS_ERROR = "Missing dimension metrics."

// System错误码、错误信息
const i32 CODE_SYS_INVALID_PARAM = 1000
const string MSG_SYS_INVALID_PARAM = "Invalid parameter '{name}'."

const i32 CODE_SYS_REQUEST_FAILED = 1002
const string MSG_SYS_REQUEST_FAILED = "Failed to request URL '{url}', reason: {reason}"

const i16 CODE_OFS_EXCEPTION = 2001
// order 服务错误码、错误信息
const i32 CODE_ORDER_PAYTRANSACTION_NOT_EXISTS = 7500
const string MSG_ORDER_PAYTRANSACTION_NOT_EXISTS = "The transaction doesn't exists."

const i32 CODE_REFUND_AMOUNT_ERROR = 7501
const string MSG_REFUND_AMOUNT_ERROR = "The refund amount cannot exceed the payment amount."

const i32 CODE_ORDER_PAYMENT_REQUEST_ERROR = 7502
const string MSG_ORDER_PAYMENT_REQUEST_ERROR = "Request method not recognised or implemented."

const i32 CODE_ORDER_PAYMENT_REQUEST_FAIL = 7503

const i32 CODE_ORDER_DOCUMENT_NOT_FOUND = 7505
const string MSG_ORDER_DOCUMENT_NOT_FOUND = "{name} data not found."