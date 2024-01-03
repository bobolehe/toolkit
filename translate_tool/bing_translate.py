import json
import random
import time
import requests
import datetime
import re
import settings

from bs4 import BeautifulSoup
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def replace_empty_brackets_with_conditions(text):
    # 正则表达式匹配函数名（由字母组成）后紧跟的空括号（无论是英文还是中文括号）
    # 函数名后不能有空格或非字母字符，括号内必须为空
    pattern = re.compile(r'([a-zA-Z]+)\s*[\(\（]\s*[\)\）]')

    # 函数用于替换匹配项的格式
    def replacer(match):
        return f"{match.group(1)}()"

    # 应用替换
    return pattern.sub(replacer, text)


def remove_spaces_around_chinese_brackets(text):
    # 移除中文括号前的空格
    text = re.sub(r'\s+(（)', r'\1', text)
    # 移除中文括号后的空格
    text = re.sub(r'(）)\s+', r'\1', text)
    return text


def remove_spaces_around_numbers(text):
    # 使用正则表达式替换中文字符和数字之间的空格
    # 中文字符后跟数字
    text = re.sub(r'([\u4e00-\u9fa5])\s+(\d)', r'\1\2', text)
    # 数字后跟中文字符
    text = re.sub(r'(\d)\s+([\u4e00-\u9fa5])', r'\1\2', text)
    return text


def remove_spaces_between_chinese_and_english(text):
    # 正则表达式匹配中文字符和英文字符之间的空格
    pattern = re.compile(r'([\u4e00-\u9fa5])\s+([a-zA-Z])|([a-zA-Z])\s+([\u4e00-\u9fa5])')

    # 替换匹配的空格
    return pattern.sub(r'\1\2\3\4', text)


def replace_chinese_brackets_with_english(text):
    # 替换英文字符后紧跟的中文括号为英文括号
    text = re.sub(r'([a-zA-Z])（', r'\1(', text)
    text = re.sub(r'）([a-zA-Z])', r')\1', text)
    return text


class BingTranslate:
    def __init__(self):
        self.cooike = None
        self.IG = None
        self.IID = None
        self.key = None
        self.Token = None
        self.Expiry = None
        self.ExpirationTime = datetime.datetime.now()
        self.url = "https://www.bing.com/translator?mkt=zh-CN"

    def get_bing_token(self):
        url = "https://www.bing.com/translator?mkt=zh-CN"
        url = "https://cn.bing.com/translator/?h_text=msn_ctxt&setlang=zh-cn"
        headers = {
            "Host": "cn.bing.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }
        response = requests.get(url, headers=headers)
        cookie = '; '.join([c.split(';')[0] for c in response.headers.get('set-cookie', '').split(',')])

        # 从响应正文中提取 IG 和 IID
        body = response.text
        IG = re.search(r'IG:"([^"]+)"', body)
        IID = re.search(r'data-iid="([^"]+)"', body)
        IG = IG.group(1) if IG else None
        IID = IID.group(1) if IID else None

        # 提取 key, token, tokenExpiryInterval
        match = re.search(r'params_AbusePreventionHelper\s?=\s?([^\]]+\])', body)
        if match:
            key, token, tokenExpiryInterval = json.loads(match.group(1))
        else:
            key = token = tokenExpiryInterval = None

        # 打印提取的值（可根据需要处理）
        return {
            "Cookie": cookie,
            "IG": IG,
            "IID": IID,
            "Key": key,
            "Token": token,
            "Token-Expiry-Interval": tokenExpiryInterval
        }

    def bing_translate(self, text):
        if self.ExpirationTime < datetime.datetime.now() or (not self.cooike or not self.IG or not self.IID or not self.key or not self.Token or not self.Expiry):
            self.ExpirationTime = datetime.datetime.now() + datetime.timedelta(minutes=30)
            self.cooike, self.IG, self.IID, self.key, self.Token, self.Expiry = self.get_bing_token().values()
        url = f"https://cn.bing.com/ttranslatev3?isVertical=1&&IG={self.IG}&IID=translator.5027"
        s_time = time.time()
        headers = {
            "Host": "cn.bing.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Referer": "https://cn.bing.com/translator/?h_text=msn_ctxt&setlang=zh-cn",
            "Cooike": self.cooike,
        }
        text = text.strip()
        if len(text) <= 5000:
            data = f"&fromLang=en&text={text}&to=zh-Hans&token={self.Token}&key={self.key}&tryFetchingGenderDebiasedTranslations=true"
            encoded_data = data.encode('utf-8')
            w = 0
            while True:
                try:
                    r = requests.post(url, headers=headers, data=encoded_data)
                    if r.status_code == 200:
                        e_time = time.time()
                        t_r = {'status': True, 'data': r.json()[0]['translations'][0]['text'], "time": e_time - s_time}
                        return t_r
                except Exception as e:
                    w += 1
                    if w == 10:
                        return {'status': False, 'data': str(e)}

        else:
            text_list = text.split('\n')
            t_value = ''
            for t in text_list:
                if t:
                    data = f"&fromLang=en&text={t}&to=zh-Hans&token={self.Token}&key={self.key}&tryFetchingGenderDebiasedTranslations=true"
                    encoded_data = data.encode('utf-8')
                    w = 0
                    while True:
                        try:
                            r = requests.post(url, headers=headers, data=encoded_data)
                            if r.status_code == 200:
                                t_value += r.json()[0]['translations'][0]['text']
                                t_value += '\n'
                                break
                        except Exception as e:
                            w += 1
                            if w == 10:
                                return {'status': False, 'data': str(e)}
                else:
                    t_value += '\n'

            t_value = t_value.strip()
            e_time = time.time()
            return {'status': True, 'data': t_value, 'time': e_time - s_time}


translateRun = BingTranslate()

if __name__ == '__main__':
    t = """OWASP AntiSamy .NET is a library for performing cleansing of HTML coming from untrusted sources. Prior to version 1.2.0, there is a potential for a mutation cross-site scripting (mXSS) vulnerability in AntiSamy caused by flawed parsing of the HTML being sanitized. To be subject to this vulnerability the `preserveComments` directive must be enabled in your policy file and also allow for certain tags at the same time. As a result, certain crafty inputs can result in elements in comment tags being interpreted as executable when using AntiSamy's sanitized output. This is patched in OWASP AntiSamy .NET 1.2.0 and later. See important remediation details in the reference given below. As a workaround, manually edit the AntiSamy policy file (e.g., antisamy.xml) by deleting the `preserveComments` directive or setting its value to `false`,  if present. Also it would be useful to make AntiSamy remove the `noscript` tag by adding a line described in the GitHub Security Advisory to the tag definitions under the `<tagrules>` node, or deleting it entirely if present. As the previously mentioned policy settings are preconditions for the mXSS attack to work, changing them as recommended should be sufficient to protect you against this vulnerability when using a vulnerable version of this library. However, the existing bug would still be present in AntiSamy or its parser dependency (HtmlAgilityPack). The safety of this workaround relies on configurations that may change in the future and don't address the root cause of the vulnerability. As such, it is strongly recommended to upgrade to a fixed version of AntiSamy."""
    r = "WireMock with GUI versions 3.2.0.0 through 3.0.4.0 are vulnerable to stored cross-site scripting (SXSS) through the recording feature. An attacker can host a malicious payload and perform a test mapping pointing to the attacker's file, and the result will render on the Matched page in the Body area, resulting in the execution of the payload. This occurs because the response body is not validated or sanitized."
    t2 = "Update Mattermost Server to versions 8.1.7, 9.3.0 or higher."
    t3 = "Mattermost fails to scope the WebSocket response around notified users to a each user separately resulting in the WebSocket broadcasting the information about who was notified about a post to everyone else in the channel."
    t_list = [t, r, t2, t3]

    pattern = re.compile(r'^<[^>]+>.*<\/[^>]+>$', re.DOTALL)
    cleaned_html_content = re.sub(r'\s+', ' ', t)
    t_value = ""

    i = 0
    while True:
        i += 1
        r = translateRun.bing_translate(random.choice(t_list))
        print(f"第{i}次翻译", r)
