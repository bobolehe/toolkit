import execjs
import time
import requests
import concurrent.futures


js_str = """
function getSign() {
   return 10000 * Math.round(10000 * Math.random())
}
"""
context = execjs.compile(js_str)
result = int(context.call('getSign')) + 2


def translate(p, proxy=None):
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
                    "browserType": 1},
                "timestamp": timestamp},
            "id": result}
    h = {
        # 'Cookie': "INGRESSCOOKIE=473be7f9ed74d2102b967dbabee92b95|a6d4ac311669391fc997a6a267dc91c0; userCountry=CN; dapUid=85093c07-7e5b-4fb2-b4aa-641244692755; releaseGroups=2690.AAEXP-1779.2.1_2700.AAEXP-1789.2.1_1119.B2B-251.2.4_2365.WDW-179.2.2_2366.WDW-189.2.2_2405.DWFA-435.2.2_2464.DM-1175.2.2_2655.DM-994.1.1_2715.AAEXP-1804.1.1_2068.DF-3045.2.3_2357.TACO-19.2.3_2694.AAEXP-1783.1.1_2698.AAEXP-1787.1.1_2703.AAEXP-1792.2.1_2711.AAEXP-1800.1.1_863.DM-601.2.2_866.DM-592.2.2_1577.DM-594.2.3_2459.TC-850.2.1_2496.MLOP-24.2.3_2699.AAEXP-1788.1.1_2349.DWFA-553.2.2_2370.DAL-568.2.1_2394.WDW-217.2.3_2413.DWFA-524.1.1_2656.DM-1177.1.1_2696.AAEXP-1785.2.1_220.DF-1925.1.9_2272.DF-3361.1.2_1444.DWFA-362.2.2_2654.DF-3554.1.1_2708.AAEXP-1797.1.1_2716.AAEXP-1805.1.1_975.DM-609.2.3_2055.DM-814.2.3_2345.DM-1001.2.2_2373.DM-1113.2.4_2395.WDW-151.2.2_2402.DF-3525.1.6_2369.DAL-371.2.1_2499.DWFA-657.1.2_2710.AAEXP-1799.1.1_2712.AAEXP-1801.1.1_2691.AAEXP-1780.2.1_2692.AAEXP-1781.2.1_1327.DWFA-391.2.2_2278.DF-3430.2.5_2372.DM-1004.1.1_2374.DWFA-542.2.4_2396.ACL-384.2.1_2688.AAEXP-1777.1.1_2693.AAEXP-1782.2.1_2704.AAEXP-1793.1.1_2717.AAEXP-1806.1.1_2705.AAEXP-1794.1.1_2713.AAEXP-1802.1.1_2714.AAEXP-1803.1.1_2377.DUI-131.2.2_2706.AAEXP-1795.1.1_2455.DPAY-2828.2.2_2695.AAEXP-1784.1.1_2701.AAEXP-1790.1.1_2697.AAEXP-1786.2.1_2707.AAEXP-1796.1.1_976.DM-667.2.3_1084.TG-1207.2.3_1483.DM-821.2.2_1997.DM-941.2.3_2346.DF-3049.2.3_2689.AAEXP-1778.1.1_2702.AAEXP-1791.1.1_1571.DM-791.2.4_1585.DM-900.2.3_2356.B2B-515.2.2_2383.DF-3505.2.2_2403.DF-3531.1.2_2657.DWFA-656.1.1_1780.DM-872.2.2_2400.WDW-238.2.2_2404.DWFA-525.2.2_2709.AAEXP-1798.1.1_1583.DM-807.2.5_2050.DM-455.2.3_2274.DM-952.2.2_2497.WDW-209.2.1; __cf_bm=WcLwLY4yja_6kruc2qnwgROlP.kvJd5lcR9S5h68BRg-1694680079-0-AfpxhiKvncKhy4touBLriN7B5gZlN5Ru3drEUa0e6fey4ieEI9eBNkBgw1HoOI/7dVqmtUL0m1qgd3YtZy9akX8=; privacySettings=%7B%22v%22%3A%221%22%2C%22t%22%3A1694649600%2C%22m%22%3A%22LAX_AUTO%22%2C%22consent%22%3A%5B%22NECESSARY%22%2C%22PERFORMANCE%22%2C%22COMFORT%22%2C%22MARKETING%22%5D%7D; dapVn=1; LMTBID=v2|7ad5b988-65f5-4fd3-bc76-227538042608|3ef9f20818dbffef7417eb8c7cdd3e1e; dapSid=%7B%22sid%22%3A%227d427423-d7d5-4126-b345-e100fdde06ef%22%2C%22lastUpdate%22%3A1694680094%7D",
        'Content-type': 'application/json',
    }
    return requests.post(url, json=data, headers=h).json()


# 获取单个代理
def query_proxy():
    proxy = {
        'http': 'http://' + requests.get(url='http://127.0.0.1:8888/proxy/get').json()['message']
    }
    return proxy


def run(p):
    # 创建线程池
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    # 提交任务到线程池
    futures = [executor.submit(self.requests_proxy, proxy) for proxy in proxy_list]

    response = translate(p)
    while True:
        try:
            print(response)
            if not response.get('error'):
                return response
        except Exception as e:
            e = e
            pass
        else:
            global result
            result += 1
            response = translate(p)


if __name__ == '__main__':
    run(p="A password for accessing a WWW URL is guessable.")
