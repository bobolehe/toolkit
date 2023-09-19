"""
百度翻译 翻译速度受ip影响
环境python3.10.*
PyExecJS == 1.5.1
playwright == 1.32.1
`pip install playwright`
`playwright install`
"""
import execjs
import time
import requests
from playwright.sync_api import sync_playwright

# 翻译字符加密js代码
js_str = r"""
function e(t, e) {
    (null == e || e > t.length) && (e = t.length);
    for (var n = 0, r = new Array(e); n < e; n++)
        r[n] = t[n];
    return r
};

function n(t, e) {
    for (var n = 0; n < e.length - 2; n += 3) {
        var r = e.charAt(n + 2);
        r = "a" <= r ? r.charCodeAt(0) - 87 : Number(r),
        r = "+" === e.charAt(n + 1) ? t >>> r : t << r,
        t = "+" === e.charAt(n) ? t + r & 4294967295 : t ^ r
    }
    return t
};

function b(t) {
        var o, i = t.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
        if (null === i) {
            var a = t.length;
            a > 30 && (t = "".concat(t.substr(0, 10)).concat(t.substr(Math.floor(a / 2) - 5, 10)).concat(t.substr(-10, 10)))
        } else {
            for (var s = t.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), c = 0, l = s.length, u = []; c < l; c++)
                "" !== s[c] && u.push.apply(u, function(t) {
                    if (Array.isArray(t))
                        return e(t)
                }(o = s[c].split("")) || function(t) {
                    if ("undefined" != typeof Symbol && null != t[Symbol.iterator] || null != t["@@iterator"])
                        return Array.from(t)
                }(o) || function(t, n) {
                    if (t) {
                        if ("string" == typeof t)
                            return e(t, n);
                        var r = Object.prototype.toString.call(t).slice(8, -1);
                        return "Object" === r && t.constructor && (r = t.constructor.name),
                        "Map" === r || "Set" === r ? Array.from(t) : "Arguments" === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? e(t, n) : void 0
                    }
                }(o) || function() {
                    throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
                }()),
                c !== l - 1 && u.push(i[c]);
            var p = u.length;
            p > 30 && (t = u.slice(0, 10).join("") + u.slice(Math.floor(p / 2) - 5, Math.floor(p / 2) + 5).join("") + u.slice(-10).join(""))
        }
        for (var d = "".concat(String.fromCharCode(103)).concat(String.fromCharCode(116)).concat(String.fromCharCode(107)), h = (null !== r ? r : (r = window[d] || "") || "").split("."), f = Number(h[0]) || 0, m = Number(h[1]) || 0, g = [], y = 0, v = 0; v < t.length; v++) {
            var _ = t.charCodeAt(v);
            _ < 128 ? g[y++] = _ : (_ < 2048 ? g[y++] = _ >> 6 | 192 : (55296 == (64512 & _) && v + 1 < t.length && 56320 == (64512 & t.charCodeAt(v + 1)) ? (_ = 65536 + ((1023 & _) << 10) + (1023 & t.charCodeAt(++v)),
            g[y++] = _ >> 18 | 240,
            g[y++] = _ >> 12 & 63 | 128) : g[y++] = _ >> 12 | 224,
            g[y++] = _ >> 6 & 63 | 128),
            g[y++] = 63 & _ | 128)
        }
        for (var b = f, w = "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(97)) + "".concat(String.fromCharCode(94)).concat(String.fromCharCode(43)).concat(String.fromCharCode(54)), k = "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(51)) + "".concat(String.fromCharCode(94)).concat(String.fromCharCode(43)).concat(String.fromCharCode(98)) + "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(102)), x = 0; x < g.length; x++)
            b = n(b += g[x], w);
        return b = n(b, k),
        (b ^= m) < 0 && (b = 2147483648 + (2147483647 & b)),
        "".concat((b %= 1e6).toString(), ".").concat(b ^ f)
    }
var r = "320305.131321201"

function getSign(t) {
   return b(t)
};

function getToken() {
    return (window.common.token)
};

"""


class BaiduTranslate:
    def __init__(self, auto):
        """
        auto: 指定是否需要自动获取cookie、token
        """
        self.proxy_http = self.query_proxy()
        if auto:
            self.cookie, self.token = self.get_token()
        else:
            self.cookie = 'BAIDUID=98EEF90A355645CA9AB89E1E3E0031CA:FG=1; BAIDUID_BFESS=98EEF90A355645CA9AB89E1E3E0031CA:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1694569932; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1694569932; ab_sr=1.0.1_OGM1NjYzMTc3NTgyOGEwYmE2ODIyZDc3YjhjNzQwZjg5MDIyMTE3ZWM3N2E2ZTVlNzk0ZDFmYjRiMDVkZmY2NjJlOTUzYWJiNDE2YzAyZDNlMzNmZTUyNGI1MGE0YzI4OGFmOTc4OWM1OWQxMjM1YjIwOTJiNTAwMjMxMzFjOTRhZGZjMDUzNDc1MmFmNTk1MDhmNjJlMGE0ZmNhNDg2NA=='
            self.token = '5feecf1da271b194f8ee16314e560c6a'
        print("初始化cookie、token成功")
        print(self.cookie)
        print(self.token)

    # 翻译字段方法
    def translate(self, query, fro='en'):
        """
        query: 需要翻译字符串
        proxy: 代理
        fro: 指定翻译语言
        """
        # 执行js生成翻译字符串sign值
        context = execjs.compile(js_str)
        result = context.call("getSign", query)

        url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
        # cookie与请求体中token相关联
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': self.cookie,
        }
        data = {
            'from': fro,
            'to': 'zh',
            'query': query,
            'transtype': 'realtime',
            'simple_means_flag': '3',
            'sign': result,
            'token': self.token,
            'domain': 'common',
            'ts': int(time.time() * 1000),
        }
        proxy = {
            'http': 'http://' + self.proxy_http,
            'https': 'https://' + self.proxy_http,
        }
        response = requests.post(url, headers=headers, data=data).json()
        data = ""
        for k, d in enumerate(response["trans_result"]["data"]):
            if d['dst'] and k == 0:
                data += f"{d['dst']}"
                continue
            if d['dst']:
                data += f"\n{d['dst']}"
        try:
            return {'error': 101, 'data': data}
        except KeyError:
            raise "ip失效"

    # 获取单个代理
    @staticmethod
    def query_proxy():
        i = 5
        while i:
            try:
                # p = requests.get(url='http://127.0.0.1:8888/success/get').json()['message']
                p = requests.get(url='http://192.168.90.12:5010/get/').json()['proxy']
                if p:
                    return p
            except Exception as e:
                print(f'获取代理失败，失败原因{e}')
                i -= 1

    # 自动检测语言
    @staticmethod
    def query_language(query):
        url = 'https://fanyi.baidu.com/langdetect'
        data = {
            'query': query
        }
        return requests.post(url, data=data).json()['lan']

    # 执行方法
    def run(self, p):
        """
        p: 翻译字段
        """
        if not self.proxy_http:
            self.query_proxy()
        # 初始代理池
        i = 10
        s_time = time.time()
        while i:
            try:
                # 判断翻译字符串语种（暂时停用）
                f = self.query_language(p)
                a = self.translate(p, fro=f)
            except Exception as e:
                e = e
                self.proxy_http = self.query_proxy()
                # i -= 1
            else:
                e_time = time.time()
                h_time = e_time - s_time
                if h_time > 2:
                    self.proxy_http = self.query_proxy()
                #     self.cookie, self.token = self.get_token()
                a['consuming'] = h_time
                return a

    # 获取cookies以及token
    @staticmethod
    def get_token():
        # 默认尝试获取5次
        c = ''
        t = ''
        i = 1
        while i < 6:
            with sync_playwright() as p:
                try:
                    # 默认情况下开启无头模式，也就是不显示浏览器窗口
                    # browser = p.chromium.launch(headless=True, channel='msedge')
                    # browser = p.chromium.launch(headless=False, proxy={"server": proxy_http})
                    browser = p.firefox.launch(headless=True)
                    # browser = p.webkit.launch(headless=False)
                    context = browser.new_context()
                    page = context.new_page()
                    page.goto('https://fanyi.baidu.com/#auth/zh/')
                    page.locator("#baidu_translate_input").fill("mange")
                    time.sleep(1)
                    # 发送一次翻译请求,获取cookie
                    for i in context.cookies():
                        c += f"{i['name']}={i['value']}; "
                    # js获取token
                    t = page.evaluate('window.common.token')
                except Exception as e:
                    print(f"第{i}次获取cookie以及token失败，错误原因{e}")
                    i += 1
                else:
                    return c[0:-2], t


if __name__ == "__main__":
    translate = BaiduTranslate(auto=True)
    for i in range(2):
        print(translate.run(p="TypeError: 'NoneType' object is not subscriptable"))
