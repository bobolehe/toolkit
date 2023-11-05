import logging
import os
import datetime

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir, "proxy_list_logs")

if not os.path.exists(log_dir):
    os.mkdir(log_dir)


def loggingtool(logger):
    logger.setLevel(logging.INFO)

    # 设置日志文件输出名
    # log_file = os.path.join(log_dir,"{}_log".format(time.strftime("%Y/%m/%d",time.localtime())))
    date = datetime.datetime.now()
    log = f"log{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}.log"
    log_file = os.path.join(log_dir, log)

    # 创建处理器：sh为控制台处理器，fh为文件处理器,log_file为日志存放的文件夹
    sh = logging.StreamHandler()
    fh = logging.FileHandler(log_file, encoding="UTF-8")

    # 创建格式器,并将sh，fh设置对应的格式
    formator = logging.Formatter(fmt="%(asctime)s %(filename)s %(levelname)s %(message)s",
                                 datefmt="%Y/%m/%d %X")
    sh.setFormatter(formator)
    fh.setFormatter(formator)

    # 将处理器，添加至日志器中
    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger = loggingtool(logger)

    logger.info("123456")
