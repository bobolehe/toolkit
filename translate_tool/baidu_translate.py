"""百度翻译"""
import execjs
import time
import requests


js_str = r"""
function n(t, e) {
    for (var n = 0; n < e.length - 2; n += 3) {
        var r = e.charAt(n + 2);
        r = "a" <= r ? r.charCodeAt(0) - 87 : Number(r),
        r = "+" === e.charAt(n + 1) ? t >>> r : t << r,
        t = "+" === e.charAt(n) ? t + r & 4294967295 : t ^ r
    }
    return t
}

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
cookie = 'BAIDUID=18DF16B54514705624F8E574AA769831:FG=1; BAIDUID_BFESS=18DF16B54514705624F8E574AA769831:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1694141463; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1694141463; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; ab_sr=1.0.1_MDE3NGRjZTJkYzUzOGY1OGZjZGU1Mzg2NGQ0NmQwMGFkNmMyYjg1ZjJjMmUzNjM0Y2U2ODk2ZWFmMTk4N2NhYTRmZjhhYTZkYzI3NWI1Njc1MzgwOWVlNGJlNDY3N2RjNmQwYjA1NjU4OGY2MWMyNjM0OTQyYTA3MjA2Y2RkNmYyN2U0ZWY0NGI4NjUxMDU3NWM5ZWIzMDg2NjZlYzE5NA=='
token = 'd9a3bef87e7e727ddcfdf7925c4e8849'


def translate(query, proxy, fro):
    """
    query: 需要翻译字符串
    proxy: 代理
    fro: 指定翻译语言
    """
    # 执行js生成翻译字符串sign值
    context = execjs.compile(js_str)
    result = context.call("getSign", query)

    url = 'https://fanyi.baidu.com/v2transapi'
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
    response = requests.post(url, headers=headers, data=data, proxies=proxy).json()
    # print(response)
    try:
        return {'error': 101, 'data': response["trans_result"]["data"][0]["dst"]}
    except KeyError:
        raise "ip失效"


# 获取单个代理
def query_proxy():
    return requests.get(url='http://192.168.90.12:5010/get/').json()['proxy']


# 自动检测语言
def query_language(query):
    url = 'https://fanyi.baidu.com/langdetect'
    data = {
        'query': query
    }
    return requests.post(url, data=data).json()['lan']


def run(p):
    # 初始代理池
    proxy = {
        'http': 'http://' + query_proxy()
    }
    i = True
    while i:
        try:
            f = query_language(p)
            a = translate(p, proxy=proxy, fro=f)
        except Exception as e:
            proxy['http'] = 'http://' + query_proxy()
        else:
            return a


if __name__ == "__main__":
    print(run(p='root privileges via buffer overflow in xlock command on SGI IRIX systems.')['data'])
    # query_language('123')
