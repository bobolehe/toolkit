from loggingtool import loggingtool
import logging
import sys
import signal


# 定义信号处理函数
def signal_handler(signal, frame):
    print("Ctrl+C pressed. Exiting...")
    # 进行必要的清理工作或其他处理操作
    # ...

    # 退出程序
    sys.exit(0)


# 注册信号处理函数
signal.signal(signal.SIGINT, signal_handler)

# 实例化日志类
logger = logging.getLogger(__name__)
logger = loggingtool.loggingtool(logger)
