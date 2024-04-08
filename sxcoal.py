import requests
import time
import datetime
import secrets
import json
import hashlib
import base64

class SX_coal_API:
    def __init__(self, proxy, appKey, appKeySecret):
        self.PROXY = proxy
        self.appKey = appKey
        self.appKeySecret = appKeySecret
        self.environmentPRO = "https://openapi.fwenergy.cn/dsapi/"

    def _get_token(self, appKey, appKeySecret):
        self.tokenUrl = self.environmentPRO+f"getToken?appKey={self.appKey}&appKeySecret={self.appKeySecret}"
        response = requests.get(self.tokenUrl, proxies=self.PROXY)
        self.token = response.json()['data']['token']

    def _sign_request(self, header, params):
        StringToSign=header|params
        StringToSign=dict(sorted(StringToSign.items()))
        StringToSign=json.dumps(header).replace(" ", "").replace(",","\n").replace('"',"")
        StringToSign=StringToSign[1:-1]
        self.header['sign'] = base64.b64encode(hashlib.md5(StringToSign.encode()).hexdigest().upper().encode()).decode()

    def get_data(self, dates, templateCode, itemCodes):

        self._get_token(self.appKey, self.appKeySecret)

        self.header={"appKey": self.appKey,
                     'nonce': secrets.token_hex(16),
                     'timestamp': str(int(round(time.time() * 1000))),
                     'token': self.token,
                     'version': '1.0'}
        self.params = {"appKey": self.appKey,
                       "templateCode": templateCode,
                       "date":dates,
                       "itemCodes":itemCodes,
                       'type': "json",
                       'lang': 'en'}
        
        self._sign_request(self.header, self.params)

        #Get data
        self.dataUrl = self.environmentPRO + "standard/getData"
        response = requests.get(self.dataUrl, proxies=self.PROXY, headers=self.header, params=self.params)
        self.response = response.json()