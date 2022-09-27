

title = "您的店铺%s (店铺ID %s) %s年%s月账单已经生成，请您及时到店铺管理后台查看并对" \
        "账以避免延误您的结算。" % ("xiao", 1, "2020", "08")
link_env = "dev"

link_url = "https://%s.perfee.com/store-login?storeId=%s&fromSource=%s"\
           % ("seller-dev", 1, 1)
msg = """
<!DOCTYPE html>
<html lang="en">
<head></head>

<body>
    <p>%s</p>
        <div class="table-a" style="color:black;">
            <table width="1200" border="1" cellspacing="0" 
            cellpadding="0" style="text-align:center">
                <tr bgcolor="#B3B3B3" style="height:60px">
                    <td>Code</td>
                    <td>Monthly</td>
                    <td>Store ID</td>
                    <td>Store Name</td>
                    <td>Country</td>
                    <td>Self-delivery</td>
                    <td>Settlement date</td>
                    <td>Item Total</td>
                    <td>Discount</td>
                    <td>Postage Total</td>
                    <td>User Paid</td>
                    <td>Commission Basis</td>
                    <td>Delivery charge platform collected</td>
                    <td>Accountable Coins</td>
                    <td>Platform coupon settlement amount</td>
                    <td>Fees of Transaction</td>
                    <td>Commission</td>
                    <td>Operation fee</td>
                    <td>After-sales deduction</td>
                    <td>Rewards and punishments</td>
                    <td>Logistics costs</td>
                    <td>Settlement amount</td>
                    <td>Self-delivery COD payment</td>
                    <td>Self-delivery COD delivery Charge</td>
                </tr>
                <tr style="height:40px">
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                </tr>
            </table>
        </div>
    <p>明细可参考附件中Excel, 更多操作和详情点击：
        <a href=%s>%s</a>
    </p>
</body>
</html>
""" % (
    title, "it.code", "it.monthly", 1, "xiao", "CN",
    'Y', "20200823", 200, 10, 30, 160, 200, 30, 20, 30, 20, 10, 10,
    0, 10, 10, 200, 10, 20,
    link_url, link_url)