from datetime import datetime
import jwt


# def produce_code(code_type):
#     prefix = code_type + datetime.utcnow().strftime('%m')
#     print(prefix)
#     idx = 1
#     code = "%s%06d" % (prefix, idx)
#     return code
#
#
# def get_year_month_str():
#     now = datetime(2021, 2, 17, 16, 28, 54, 535585)
#     year_month = now.strftime('%Y%m')
#     yea = int(year_month[:4])
#     mon = int(year_month[-2:])
#     if mon - 1 < 1:
#         month = 12
#         year = yea - 1
#     else:
#         month = mon - 1
#         year = yea
#     year_month = str(year) + "0" + str(month) if len(str(month)) < 2 else\
#         str(year) + str(month)
#
#     return year_month
#
#
# def export_result(num):
#     if "." in str(num):
#         num_x, num_y = str(num).split('.')
#         num = float(num_x + '.' + num_y[0:2])
#
#     return num
#
#
# def system_confirm_clearing(year_month):
#     year = int(year_month[:4])
#     month = int(year_month[-2:])
#     print(year, month)
#     return year, month
#
#
# def test_default_param(a=None):
#     if a is None:
#         a = []
#     a.append("hello")
#     return a


def get_next_year_month_str():
    time_now = datetime.utcnow().strftime('%Y%m')
    yea = int(time_now[:4])
    mon = int(time_now[-2:])
    if mon + 1 > 12:
        month = 1
        year = yea + 1
    else:
        month = mon + 1
        year = yea
    year_month = str(year) + "0" + str(month) if len(str(month)) < 2 else \
        str(year) + str(month)

    return year_month


def gen_token(payload):
    """生成账户token"""
    token = jwt.encode(
        payload, 'qF9MS7!fmAd*gT^c4TwCqTVyw3FuA@gsERR8D6m5K*o46DfsLHB',
        algorithm='HS256')
    print(token)
    return token


def token_decode(token, algorithms='HS256'):
    payload = jwt.decode(
        token, 'qF9MS7!fmAd*gT^c4TwCqTVyw3FuA@gsERR8D6m5K*o46DfsLHB',
        # algorithms=['HS256']
        algorithms=['HS256']
    )
    print(payload)


def my_function(a, *args, **kwargs):
    print(a)
    if args:
        print(args)
    print(kwargs, "-------")
    for arg in args:
        print(arg)



if __name__ == "__main__":
    # res = produce_code("xiao")
    # res = get_year_month_str()
    # res = export_result(2.833)
    # res = system_confirm_clearing("202005")
    # res = test_default_param()
    # res = test_json()
    # res = get_next_year_month_str()
    # get_diff_data()
    # with open("./data/gmo.json", "r") as f:
    #     ERROR_CODE_MAP = json.load(f)
    #     f.close()
    token = gen_token({"xiao": 1, "yong": 2, "sheng": 3})
    my_function(a=1, **{"xiao": "yongsheng"})
    # token_decode(token)




