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
    print(result, timestamp)
    url = 'https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs'
    data = {"jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                "jobs": [{"kind": "default",
                          "sentences": [{"text": p,
                                         "id": 1,
                                         "prefix": ""}],
                          "raw_en_context_before": [],
                          "raw_en_context_after": [],
                          "preferred_num_beams": 4
                          }],
                "lang": {"target_lang": "ZH",
                         "preference": {
                             "weight": {},
                             "default": "default"},
                         "source_lang_user_selected": "EN"},
                "priority": 1,
                "commonJobParams": {
                    "mode": "translate",
                    "browserType": 5},
                "timestamp": timestamp},
            "id": result}
    # h = {
    #     'Cookie': 'INGRESSCOOKIE=d757f79cb1c8ae121613a6528f2cabd7|a6d4ac311669391fc997a6a267dc91c0; userCountry=SG; releaseGroups=2706.AAEXP-1795.1.1_2345.DM-1001.2.2_2374.DWFA-542.2.4_2655.DM-994.2.1_2373.DM-1113.2.4_2689.AAEXP-1778.1.1_2696.AAEXP-1785.2.1_2714.AAEXP-1803.1.1_2715.AAEXP-1804.1.1_2274.DM-952.2.2_2357.TACO-19.2.3_2365.WDW-179.2.2_2405.DWFA-435.2.2_2464.DM-1175.1.1_2497.WDW-209.1.1_2693.AAEXP-1782.2.1_2708.AAEXP-1797.1.1_1327.DWFA-391.2.2_2050.DM-455.1.3_2346.DF-3049.2.3_2709.AAEXP-1798.1.1_2394.WDW-217.2.3_2496.MLOP-24.1.3_2656.DM-1177.1.1_2690.AAEXP-1779.1.1_2707.AAEXP-1796.1.1_2068.DF-3045.2.3_2272.DF-3361.2.2_2278.DF-3430.2.5_2695.AAEXP-1784.2.1_2703.AAEXP-1792.1.1_2704.AAEXP-1793.1.1_2404.DWFA-525.2.2_2455.DPAY-2828.2.2_2498.WDW-219.2.1_2459.TC-850.2.1_2697.AAEXP-1786.1.1_2700.AAEXP-1789.2.1_2705.AAEXP-1794.1.1_1119.B2B-251.2.4_1583.DM-807.2.5_2413.DWFA-524.1.1_1997.DM-941.2.3_2396.ACL-384.1.1_2710.AAEXP-1799.1.1_220.DF-1925.1.9_1577.DM-594.2.3_1780.DM-872.2.2_2402.DF-3525.1.5_2699.AAEXP-1788.1.1_2403.DF-3531.1.2_2711.AAEXP-1800.1.1_1585.DM-900.2.3_2349.DWFA-553.2.2_2369.DAL-371.1.1_2691.AAEXP-1780.2.1_2694.AAEXP-1783.1.1_2698.AAEXP-1787.1.1_2713.AAEXP-1802.1.1_863.DM-601.2.2_866.DM-592.2.2_975.DM-609.2.3_2692.AAEXP-1781.2.1_976.DM-667.2.3_2395.WDW-151.2.2_2654.DF-3554.1.1_2383.DF-3505.2.1_2712.AAEXP-1801.1.1_1444.DWFA-362.2.2_1571.DM-791.2.4_2366.WDW-189.2.2_2377.DUI-131.2.2_2382.WDW-165.2.2_2657.DWFA-656.1.1_2702.AAEXP-1791.1.1_1483.DM-821.2.2_2055.DM-814.2.3_2356.B2B-515.2.2_2701.AAEXP-1790.1.1_2400.WDW-238.2.2_2688.AAEXP-1777.1.1_2716.AAEXP-1805.1.1_2717.AAEXP-1806.1.1_1084.TG-1207.2.3_2359.WDW-155.2.3_2372.DM-1004.1.1; dapUid=26aa6186-3b30-40da-84f5-13096b85429f; __cf_bm=N73xx5q_fh3hVHt5I31pq0IChRQM5KiZoXtXYxdcBTI-1694166330-0-Acem8u77vZzx3VovW4o+mwYW/bra7pacJNIfQnOmpaFWxYBtGGO8IXFkdObijzvnJVr0KXfUzK0nllp/Vdi9aYI=; dapSid=%7B%22sid%22%3A%2204a89cd9-9258-47b0-be5f-5fb3313b2723%22%2C%22lastUpdate%22%3A1694166446%7D; privacySettings=%7B%22v%22%3A%221%22%2C%22t%22%3A1694131200%2C%22m%22%3A%22LAX_AUTO%22%2C%22consent%22%3A%5B%22NECESSARY%22%2C%22PERFORMANCE%22%2C%22COMFORT%22%2C%22MARKETING%22%5D%7D; dapVn=1; LMTBID=v2|98a3e2b5-7765-47f2-a55a-7ff1ea69a4a1|e1f27ce7a4179036f54a5e46c8d5fd39',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
    #     'Content-type': 'application/json',
    #     'TE': 'trailers',
    #     'Sec-Fetch-Site': 'same-site',
    #     'Sec-Fetch-Mode': 'cors',
    #     'Sec-Fetch-Dest': 'empty',
    # }
    # print(requests.post(url, json=data, proxies=proxy, headers=h).json())
    print(requests.post(url, json=data).json())


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
