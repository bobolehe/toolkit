import os
import logging
from datetime import datetime


def logg():
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)
    # 获取当前脚本所在的目录
    script_directory = os.path.dirname(script_path)
    # 获取上级目录
    parent_directory = os.path.dirname(script_directory)
    # 要拼接的子目录名
    subdirectory_name = "logs"
    # 使用os.path.join拼接目录
    logs_path = os.path.join(parent_directory, subdirectory_name)
    # 使用os.path.exists检查目录是否存在
    if os.path.exists(logs_path) and os.path.isdir(logs_path):
        pass
    else:
        # 如果目录不存在，创建它
        os.mkdir(logs_path)

    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    # 创建一个文件处理程序，将日志写入到文件
    t = str(datetime.now())
    log_file = f"log{t[0:10]}.log"
    log_file = os.path.join(logs_path, log_file)
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


log_data = logg()

