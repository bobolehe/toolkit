import os
import logging
from datetime import datetime
import settings


def logg():

    # 创建一个名为 "log" 的文件夹（如果不存在）
    if not os.path.exists(f"{settings.script_directory}\\log"):
        os.makedirs(f"{settings.script_directory}\\log")

    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    # 创建一个文件处理程序，将日志写入到文件
    t = str(datetime.now())
    log_file = os.path.join(f"{settings.script_directory}\\log", f"log{t[0:10]}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # 设置文件处理程序的格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 将处理程序添加到日志器中
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    # logger.addHandler(console_handler)
    return logging
