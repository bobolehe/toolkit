import execjs
import time
import requests

js_str = """
function getSign() {
   return 10000 * Math.round(10000 * Math.random())
}
"""


def translate(p, proxy):
    context = execjs.compile(js_str)
    result = int(context.call('getSign'))
    timestamp = int(time.time() * 1000)

    url = 'https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs'
    data = {"jsonrpc": "2.0", "method": "LMT_handle_jobs",
            "params": {
                "jobs": [{"kind": "default",
                          "sentences": [{"text": p,
                                         "id": 1, "prefix": ""}],
                          "raw_en_context_before": [], "raw_en_context_after": [], "preferred_num_beams": 4, "quality": "fast"}],
                "lang": {"target_lang": "ZH",
                         "preference": {
                             "weight": {"DE": 0.21132, "EN": 9.57542, "ES": 0.17399, "FR": 0.18998, "IT": 0.15512, "JA": 0.08295, "NL": 0.11271, "PL": 0.09597, "PT": 0.08225,
                                        "RU": 0.03925,
                                        "ZH": 0.67131, "BG": 0.0327, "CS": 0.07697, "DA": 0.09674, "EL": 0.02845, "ET": 0.07492, "FI": 0.12651, "HU": 0.06874, "LT": 0.05693,
                                        "LV": 0.05231,
                                        "RO": 0.05983, "SK": 0.06445, "SL": 0.05084, "SV": 0.09252, "TR": 0.04818, "ID": 0.0562, "UK": 0.05513, "KO": 0.0353, "NB": 0.15495},
                             "default": "default"},
                         "source_lang_user_selected": "EN"}, "priority": -1, "commonJobParams": {"mode": "translate", "browserType": 5},
                "timestamp": timestamp}, "id": result}
    print(requests.post(url, json=data, proxies=proxy).json())


# 获取单个代理
def query_proxy():
    proxy = {
        'http': 'http://' + requests.get(url='http://127.0.0.1:8888/proxy/get').json()['message']
    }
    return proxy


def run(p):
    proxy = query_proxy()
    translate(p, proxy)


if __name__ == '__main__':
    run(p="A password for accessing a WWW URL is guessable.")
