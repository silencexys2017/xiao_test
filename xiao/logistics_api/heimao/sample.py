# -*- coding: utf-8 -*-

"""
APIデータ取得のサンプル

コーディングはPython3.xで記述しています
requestsモジュールを使用しています

実行引数[1]:ログインID
実行引数[2]:パスワード
実行引数[3]:取得データ種別

"""
import sys
import requests
import json

USER_ID = "apitest001"
PASS_WORD = "001apitest"
# USER_ID = "0368031391"
# PASS_WORD = "huang520"
EXECUTE_URL = "http://demo-asp.ysdasp-service.ne.jp/gance/API/download/" \
              "DownloadService"
PRE_CREATE_URL = "https://demo-asp.ysdasp-service.ne.jp/yamato_asp/search.jsp"
PROXY_HOST = "http://proxy.nekonet.co.jp"
PROXY_PORT = "8080"


class Sample:
    def __init__(self, data_type):
        self.user_id = USER_ID
        self.passwd = PASS_WORD
        self.data_type = data_type

    def execute(self):
        self.url = EXECUTE_URL
        self.proxy_host = 'http://proxy.nekonet.co.jp'
        self.proxy_port = '8080'
        
        # 問合せ実行
        response = self.inquiry()
        if response.status_code != 200:
            raise Exception('HTTP通信失敗')
            
        # 取得データの出力
        self.output(response.json())
        
    """
    問合せ
    """
    def inquiry(self):
        param = {
            'download_ID': self.user_id,
            'pass_code': self.passwd,
            'data_type': self.data_type
        }
        # プロキシ認証が必要ない場合はいりません
        proxy = {'http': '{0}:{1}'.format(self.proxy_host, self.proxy_port)}
        # 問合せを実行します
        res = requests.post(
            self.url,
            data=json.dumps(param),
            headers={'Content-Type': 'application/json'},
            verify=False
            # proxies=proxy
        )
        # レスポンスを返却
        return res
        
    """
    取得データの出力処理
    """
    def output(self, json_data):
        print(json_data)
        
        if json_data == None:
            raise Exception('問合せ失敗')

        print('終了コード [ {0} ]\n'.format(json_data['response_code']))
        
        if 'download_data' in json_data:
            print('===========================================')
            print('                 問合せ結果                 ')
            print('===========================================\n')
            for data in json_data['download_data']:
                print(data)


def pre_place_order(files):
    headers = {
        # "Content-Type": "multipart/form-data",
        # "Content-Length": "1024"
        # "Content-Type": "text/html",
        # "charset": "Windows-31J"
    }
    param = {
        "uji.verbs": "fileUpload",
        "uji.id": "body",
        "uji.bean": "yamato.file.upload.bean.FileUploadBean",
        "uji.encoding": "Windows-31J",
        # "uji.encoding": "utf-8",
        "userId": USER_ID,
        "password": PASS_WORD
    }

    # プロキシ認証が必要ない場合はいりません
    proxy = {'http': '{0}:{1}'.format(PROXY_HOST, PROXY_PORT)}
    # 問合せを実行します
    res = requests.post(
        url=PRE_CREATE_URL,
        headers=headers,
        data=param,
        files=files,
        # proxies=proxy,
        verify=False
    )
    res.encoding = 'Windows-31J'
    with open("response.html", "w", encoding="utf-8") as f:
        f.write(res.text)
    print(res.text)
    # print(res.content)
    

if __name__ == '__main__':
    # args = sys.argv

    # if len(args) != 4:
    #     raise Exception('引数は [1]:ログインID, [2]:パスワード, [3]:データ種別 です')
    # sample = Sample(args[1], args[2], args[3])

    # sample = Sample(data_type="101")
    # sample.execute()

    files = {'file': open("test.csv", 'rb')}
    pre_place_order(files)


