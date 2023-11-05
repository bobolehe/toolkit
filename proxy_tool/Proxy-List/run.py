import sys
from ObtainTool.proxy_crawling import RequestsClass
from ObtainTool.proxy_test import ProxyTest
from ObtainTool.proxy_obtain import ProxyObtain
from loggingtool import logger


def crawling_proxy():
    requests_class = RequestsClass(url="https://www.rapid7.com/db/modules/payload/windows/dllinject/bind_tcp_rc4/")
    while True:
        requests_class.start_test()


def extract_proxy():
    extract = ProxyTest()
    while True:
        extract.run()


def obtain_proxy():
    obtain = ProxyObtain()
    if len(sys.argv) > 2:
        if sys.argv[2] == "get":
            return obtain.get_proxy()
        elif sys.argv[2] == "all":
            return obtain.all_proxy()
    else:
        logger.error("获取需要传递获取数量参数get一个，all获取全部")


if __name__ == '__main__':
    # 获取输入参数
    if len(sys.argv) > 1:
        gpus = sys.argv[1]
        if gpus == "crawling":
            logger.info(crawling_proxy())
        elif gpus == "extract":
            logger.info(extract_proxy())
        elif gpus == "obtain":
            logger.info(obtain_proxy())
        else:
            logger.error("指令错误,crawling爬取代理，extract排查有效代理,obtain获取代理")
    else:
        logger.error("指令错误,crawling爬取代理，extract排查有效代理,obtain获取代理")
