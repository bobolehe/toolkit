import datetime
import requests
import concurrent.futures
import setting
from loggingtool import logger
from ObtainTool import json_rw


class RequestsClass:
    def __init__(self, url):
        self.t_or_p = setting.T_OR_P
        self.success_list = []
        self.http_list = setting.HTTP_LIST
        self.target = url

    def requests_proxy(self, *args, **kwargs):
        try:
            proxies = {
                'http': args[0],
                'https': args[0]
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
            response = requests.get(self.target, headers=headers, proxies=proxies)

            if response.status_code == 200:
                self.success_list.append(args[0])
                success_set = set(self.success_list)
                # 写入json文件
                proxy_dict = {
                    "success": list(success_set),
                    "write_time": str(datetime.datetime.now())
                }
                json_rw.w(data=proxy_dict, redis_key="proxy_list")
                logger.info(f'Proxy {args[0]} is working')
            else:
                logger.info(f'Proxy {args[0]} is not working')
        except requests.exceptions.RequestException:
            logger.info(f'Proxy {args[0]} is not working')
        except Exception as e:
            logger.error(f"设置代理发送请求出现错误，查看网络状态是否正常")

    def start_test(self):
        self.success_list = []
        proxy_list = []
        logger.info(f"请求代理网站获取代理地址")
        try:
            for i in self.http_list:
                proxy_data = requests.get(url=i)
                proxy_list += proxy_data.text.split(' ')[0].split('\n')
                # proxy_list = http_text.split(' ')[0].split('\n')
        except Exception as e:
            logger.error(f"获取代理网站发生异常，异常信息{e}")
        else:
            logger.info(f"当前获取到代理数量{len(proxy_list)}")

            if self.t_or_p:
                # 创建线程池
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=setting.NUM_THREADS)
            else:
                # 创建进程池
                executor = concurrent.futures.ProcessPoolExecutor(max_workers=setting.NUM_PROCESSES)

            # 提交任务到线程池or进程池
            futures = [executor.submit(self.requests_proxy, proxy) for proxy in proxy_list]

            # 关闭线程池or进程池，不再接受新的任务
            executor.shutdown()

            # 等待所有任务完成
            concurrent.futures.wait(futures)

            # 返回测试成功代理
            return self.success_list


if __name__ == '__main__':
    requests_class = RequestsClass(url='https://www.rapid7.com/db/modules/payload/windows/dllinject/bind_tcp_rc4/')
    requests_class.start_test()
# pytest.main([__file__])
