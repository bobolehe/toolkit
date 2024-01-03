"""百度翻译"""
import datetime

import execjs
import time
import requests
from playwright.sync_api import sync_playwright

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
}

"""
# 推荐使用Edge取请求cookie和token
cookie = 'BAIDUID=62D29763475FF8C6DA6A1BC670904C8C:FG=1; BIDUPSID=62D29763475FF8C6B138D5D8D88710E3; PSTM=1680753405; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1694139138; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; ZFY=QPcrF53sxH:A:AV6cv7mQEQ3OjZRlEOS4LYHTMGs:B:BqgY:C; H_PS_PSSID=36556_39109_38831_39114_39116_39039_38917_38829_26350_39138_39132_39137_39100; delPer=0; PSINO=7; BDRCVFR[Fc9oatPmwxn]=aeXf-1x8UdYcs; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1694689845; APPGUIDE_10_6_2=1; ab_sr=1.0.1_YjgwM2MyNWQwODI1NWVmZWM0NmU5MGU3NDQ4NzdjNDJkMWY1NmUyYjViOWY5NDk4ZTgyODQyOGQyMTc1N2U5OWE4YmI4Y2U5MmMzM2Q2Y2M3OGI1MDk5YjQwY2E2ZmVmYjkwNTdiNWE5ZWRmZWY5MjRmNTY5YTZjYzlmYzVmM2NmMWIwMDBjZmNhNjg3MTE1MjliYjYxOWM1NDgxYTM3YQ=='
token = 'b0b9f11bbe2017c88df5ba89a8015f9c'
global proxy_http
proxy_http = ''


def translate(query, fro):
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
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie,
    }
    data = {
        'from': fro,
        'to': 'zh',
        'query': query,
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'sign': result,
        'token': token,
        'domain': 'common',
        'ts': int(time.time() * 1000),
    }

    proxy = {
        'http': 'http://' + proxy_http,
        # 'https': 'https://' + '103.207.1.82:8080'
    }
    response = requests.post(url, headers=headers, data=data, proxies=proxy).json()
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
def query_proxy():
    while True:
        p = requests.get(url='http://192.168.90.12:5010/get/').json()['proxy']
        if p:
            global proxy_http
            proxy_http = p
            return


# 自动检测语言
def query_language(query):
    url = 'https://fanyi.baidu.com/langdetect'
    data = {
        'query': query
    }
    return requests.post(url, data=data).json()['lan']


def run(p):
    # if not proxy_http:
    #     query_proxy()
    # 初始代理池
    i = True
    while i:
        try:
            # f = query_language(p)
            a = translate(p, fro='en')
        except Exception as e:
            pass
            # query_proxy()
        else:
            return a


def get_token():
    c = ''
    t = ''
    # if not proxy_http:
    #     query_proxy()
    while True:
        with sync_playwright() as p:
            try:
                # 默认情况下开启无头模式，也就是不显示浏览器窗口
                # browser = p.chromium.launch(headless=True, channel='msedge')
                browser = p.firefox.launch(headless=True)
                # browser = p.chromium.launch(headless=False, proxy={"server": proxy_http})
                context = browser.new_context()
                page = context.new_page()
                page.set_default_timeout(10000)
                page.goto('https://fanyi.baidu.com/#auth/zh/')
                page.locator("#baidu_translate_input").fill("mange")
                for i in context.cookies():
                    c += f"{i['name']}={i['value']}; "
                t = page.evaluate('window.common.token')
            except Exception as e:
                pass
                # query_proxy()
            else:
                return c[0:-2], t


if __name__ == "__main__":
    # 获取代理
    # print(query_proxy())
    # 获取cookie和token
    # cookie, token = get_token()
    # print(f"{cookie}", token)
    # 测试翻译功能
    for i in range(1):
        s_time = time.time()
        r = """Please upgrade to FortiOS version 7.4.0 or above
Please upgrade to FortiOS version 7.2.4 or above
Please upgrade to FortiOS version 7.0.11 or above
Please upgrade to FortiOS version 6.4.12 or above
Please upgrade to FortiOS version 6.2.14 or above
Please upgrade to FortiProxy version 7.2.2 or above
Please upgrade to FortiProxy version 7.0.8 or above
 
Workaround:
 
Disable "Host Check", "Restrict to Specific OS Versions" and "MAC address host checking" in sslvpn portal configuration. For example for "full-access" sslvpn portal:
 
config vpn ssl web portal
edit "full-access"
set os-check disable
set host-check none
set mac-addr-check disable
end"""
        print(run(p=r)['data'])
        e_time = time.time()
        h_time = e_time - s_time
        print(h_time)
    import json
    with open('../zip/deltaCves/CVE-2023-6093.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        tt = data['containers']['cna']['workarounds'][0]['value']
        print(run(p=tt))
    # 执行js生成翻译字符串sign值
    # context = execjs.compile(js_str)
    # result = context.call("getSign", "Cross-Site Request Forgery (CSRF) vulnerability in QuantumCloud ChatBot 🚀 plugin <=\xa04.2.8 versions.")
    # print(result)
