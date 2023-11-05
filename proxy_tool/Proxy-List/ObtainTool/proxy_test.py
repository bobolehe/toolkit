import requests
import datetime
import concurrent.futures
from loggingtool import logger
from ObtainTool import RedisProxy


class ProxyTest:

    def __init__(self):
        self.success_list = []

    def requests_proxy(self, *args, **kwargs):
        http = args[0]
        try:

            proxies = {
                'http': http,
                'https': http
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
            # response1 = requests.get("https://github.com/", headers=headers, proxies=proxies, timeout=5)
            response2 = requests.get('https://fanyi.baidu.com/v2transapi?from=en&to=zh', headers=headers, proxies=proxies)

            if response2.status_code == 200:
                self.success_list.append(http)
                success_set = set(self.success_list)

                # 写入json文件
                proxy_dict = {
                    "success": list(success_set),
                    "write_time": str(datetime.datetime.now())
                }

                RedisProxy.w(key="success_proxy", data=proxy_dict)

                logger.info(f'Proxy {http} is working')
            else:
                logger.info(f'Proxy {http} is not working')
        except requests.exceptions.RequestException:
            logger.info(f'Proxy {http} is not working')
        except Exception as e:
            logger.error(f"设置代理发送请求出现错误，查看网络状态是否正常")

    def run(self, ):
        self.success_list = []
        try:
            proxy_list = RedisProxy.r(key="proxy_list")

            # 创建线程池
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

            # 提交任务到线程池
            futures = [executor.submit(self.requests_proxy, proxy) for proxy in proxy_list]

            # 关闭线程池，不再接受新的任务
            executor.shutdown()

            # 等待所有任务完成
            concurrent.futures.wait(futures)
        except Exception as e:
            logger.error(f"错误信息{e}")


if __name__ == '__main__':
    proxy = ProxyTest()
    proxy.run()
