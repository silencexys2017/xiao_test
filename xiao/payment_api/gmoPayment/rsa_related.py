# -*- coding:utf-8 -*-
import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

PUBLIC_KEY = '''
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlhKDXlWw4tu2JrbFITYUDT82BH2W8rLZ9OMFifrYIjO8fz12EsP+Xo+I/xUeh1ctTjGOIQYzZHYacWQ+xjNE5NSF5Beilcn2It0ST8EuQEb0NpRcm7BnYgVP7vYROXUFHiyrOUlPopSW4o+31IKwmO7VtTmq4iHZspMF/25YahIbOJfFF0uMAdIJYRxpYwIS5LWQB0zMT1G70tIGU6yIe3ciN7Le7phljZFidnM+EVSaauela9U8uL00WxTFudpybEwpDTX4zYoE5Cd1DWhZt4pSeKpqEiBMzK/siF1tkPBFifU+VH0e8L8+3n6/v52NwMnhPkoeHdDyLgl1tJnWJwIDAQAB
    '''


class RSACipher():
    '''
    RSA加密、解密、签名、验签工具类
    '''

    def encrypt(self, key, text):
        '''
        加密方法
        :param key: 公钥
        :param text: 需要加密的明文
        :return: 加密后的密文
        '''
        public_key = RSA.importKey(base64.b64decode(key))
        cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
        return base64.b64encode(cipher.encrypt(text.encode())).decode()

    def decrypt(self, key, text):
        '''
        解密方法
        :param key: 私钥
        :param text: 加密后的密文
        :return: 解密后的明文
        '''
        private_key = RSA.importKey(base64.b64decode(key))
        cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        return cipher.decrypt(base64.b64decode(text)).decode()

    def sign(self, key, text):
        '''
        签名方法
        :param key: 私钥
        :param text: 需要签名的文本
        :return: 签名信息
        '''
        private_key = RSA.importKey(base64.b64decode(key))
        hash_value = SHA256.new(bytes(text, encoding="utf-8"))
        signer = PKCS1_v1_5.new(private_key)
        signature = signer.sign(hash_value)
        return base64.b64encode(signature).decode()

    def verify(self, key, text, signature):
        '''
        验签方法
        :param key: 公钥
        :param text: 需要验签的文本
        :param signature: 签名信息
        :return: 验签结果
        '''
        public_key = RSA.importKey(base64.b64decode(key))
        hash_value = SHA256.new(bytes(text, encoding="utf-8"))
        verifier = PKCS1_v1_5.new(public_key)
        return verifier.verify(hash_value, base64.b64decode(signature))


if __name__ == '__main__':
    text = '{"cardNo": "4123450131003312", "tokenNumber": 1, "expire": "2212"}'
    cipher = RSACipher()
    encrypt_text = cipher.encrypt(PUBLIC_KEY, text)
    print(encrypt_text)
