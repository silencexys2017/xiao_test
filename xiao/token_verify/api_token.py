import time
import jwt

OAUTH2_EXPIRE = 100000
TOKEN_KEY = '=DAone%B@gxiP8iz_Nyhi&:w@83BtQe,U^:ay}p:T-G&_XzE@Dg'


def gen_token(payload, exp=None):
    """生成token"""
    if not exp:
        payload['exp'] = int(time.time()) + OAUTH2_EXPIRE
    else:
        payload['exp'] = int(time.time()) + exp
    return jwt.encode(
        payload, TOKEN_KEY, algorithm='HS256').decode()


if __name__ == "__main__":
    payload = {
                    "seller_id": 200000015,
                    "store_id": 200000011,
                    "region_id_of_seller": 2,
                    "region_id_of_store": 6,
                }
    res = gen_token(payload)
    print(res)