import thriftpy2
import thrift_connector.connection_pool as connection_pool
import thriftpy2.protocol.json as proto

DEF = thriftpy2.load("./thrift_app/order_struct.thrift")

class VoucherObj:
    def __init__(self, voucher_id, sku_ids, amount, owner_type):
        self.voucherId = voucher_id
        self.skuIds = sku_ids
        self.amount = amount
        self.ownerType = owner_type

voucher_1 = DEF.Voucher(100000549, [10000100108], 100, 2)
voucher_2 = DEF.Voucher(100000542, [10000100060, 10000100108], 100, 1)

vouchers = [voucher_1, voucher_2]

vouchers = sorted(vouchers, key=lambda x: len(x.skuIds), reverse=True)
print(vouchers)