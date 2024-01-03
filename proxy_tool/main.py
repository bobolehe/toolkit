from app import create_app
from app.task_tool.apscheduler_task import scheduler
from app.check_proxy.check_proxy import rds
from app.config import BaseConfig
import signal
import sys


def cleanup_function():
    # 执行清理操作，例如关闭数据库连接、保存状态等
    for i in BaseConfig.VERIFY_URL:
        rds.ret.delete(i)
    scheduler.shutdown()
    # 最后退出应用
    sys.exit(0)


app = create_app()

# 启动
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=False)
    # 注册信号处理程序，捕获Ctrl+C信号(SIGINT)
    signal.signal(signal.SIGINT, cleanup_function)

    # 正常的应用逻辑
    try:
        while True:
            # 应用的主要操作
            cleanup_function()
            break
    except KeyboardInterrupt:
        # 用户按下Ctrl+C时会触发KeyboardInterrupt异常
        pass
