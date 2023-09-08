# 百度垂直领域翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# 2020.07.28 更新，原url拼接错误，感谢热心网友指正
# coding=utf-8

import http.client
import hashlib
import urllib
import random
import json
from http.client import HTTPConnection

# appid = '20230825001793503'  # 填写你的appid
appid = '20230907001808367'  # 填写你的appid
# secretKey = 'AecMzUovmXTviZVYsBnI'  # 填写你的密钥
secretKey = '9Loiq5hv0Zh3HwBEfmt6'  # 填写你的密钥

httpClient = None
myurl = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

fromLang = 'auto'  # 原文语种
toLang = 'zh'  # 译文语种
salt = random.randint(32768, 65536)
httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')


def translate(q):
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    try:
        httpClient.request('GET', url)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        print(result_all)
        result = json.loads(result_all)
        return result['trans_result'][0]['dst']
    except Exception as e:
        return 104
    finally:
        if httpClient:
            httpClient.close()


if __name__ == '__main__':
    print(translate("""Welcome to the new CVE Beta website! CVE Records have a new and enhanced format. View records in the new format using the CVE ID lookup above or download them on the Downloadspage. CVE List keyword search
will be temporarily hosted on the legacy cve.mitre.org
website until the transitionis complete. """))
