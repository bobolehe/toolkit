import pytz
import sys

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
from urllib.parse import urlparse

config = {
    'redis': 'redis://:123456@127.0.0.1:6379/2',  # redis链接
    'ThreadPoolExecutor': 100,  # 默认线程数
    'ProcessPoolExecutor': 5,  # 默认进程数量
    'max_instances': 200,  # 支持200个实例并发
    'misfire_grace_time': 15,  # 15秒的任务超时容错
}


def create_scheduler(setting):
    """
    生成调度器对象
    :param setting: 配置字典
    :return:
    """
    parsed_url = urlparse(setting['redis'])
    scheme = parsed_url.scheme
    host = parsed_url.hostname
    port = parsed_url.port
    db = parsed_url.path[1:]
    password = parsed_url.password

    jobstores = {
        'redis': RedisJobStore(host=host, port=port, db=db, password=password),
        'default': MemoryJobStore()
    }

    executors = {
        'default': ThreadPoolExecutor(setting['ThreadPoolExecutor']),  # 默认线程数
        'processpool': ProcessPoolExecutor(setting['ProcessPoolExecutor'])  # 默认进程
    }

    job_defaults = {
        "coalesce": True,
        # 积攒的任务只跑一次
        'max_instances': setting['max_instances'],  # 支持200个实例并发
        'misfire_grace_time': setting['misfire_grace_time']  # 15秒的任务超时容错
    }
    scheduler = BackgroundScheduler(daemon=False, job_defaults=job_defaults, executors=executors, jobstores=jobstores, timezone=pytz.utc)
    scheduler.start()
    return scheduler


def scheduled_tasks(scheduler, task, sleep, parameters=None):
    """
    分配定时任务
    :param scheduler: 调度器
    :param task: 执行函数
    :param sleep: 指定延时
    :param parameters: 函数所需参数
    :return: 返回任务名称id
    add_jod:
        func: 执行函数
        trigger: 触发器
            日期触发器 ('date'): 任务在特定日期和时间执行一次。
            间隔触发器 ('interval'): 任务按照指定的时间间隔重复执行，可以按秒、分钟、小时等重复。
            每日触发器 ('daily'): 任务在每天的指定时间执行一次。
            每周触发器 ('weekly'): 任务在每周的指定时间执行一次。
            每月触发器 ('monthly'): 任务在每月的指定日期和时间执行一次。
            每天触发器 ('cron'):
        run_date: 时间类型
        jobstore: 指定任务存储在Redis
        args: 传递给执行函数参数
        id: 命名任务id
    """
    if parameters:
        jobid = scheduler.add_job(func=task, trigger='interval', seconds=sleep, args=parameters)
    else:
        jobid = scheduler.add_job(func=task, trigger='interval', seconds=sleep)
    return jobid


def assignments(scheduler, task, parameters=None):
    """
    安排任务执行
    :param scheduler: 调度器
    :param task: 执行函数
    :param parameters: 函数所需参数
    :return:
    add_jod:
        func: 执行函数
        trigger: 触发器
            日期触发器 ('date'): 任务在特定日期和时间执行一次。
            间隔触发器 ('interval'): 任务按照指定的时间间隔重复执行，可以按秒、分钟、小时等重复。
            每日触发器 ('daily'): 任务在每天的指定时间执行一次。
            每周触发器 ('weekly'): 任务在每周的指定时间执行一次。
            每月触发器 ('monthly'): 任务在每月的指定日期和时间执行一次。
            每天触发器 ('cron'):
        run_date: 时间类型
        jobstore: 指定任务存储在Redis
        args: 传递给执行函数参数
        id: 命名任务id
    """
    if parameters:
        jobid = scheduler.add_job(func=task, trigger='date', run_date=datetime.utcnow(), jobstore='redis', args=parameters)
    else:
        jobid = scheduler.add_job(func=task, trigger='date', run_date=datetime.utcnow(), jobstore='redis')
    return jobid


def close_scheduler(scheduler):
    """
    关闭调度器
    :param scheduler: 调度器
    :return:
    """
    scheduler.shutdown()


def my_job():
    """
    测试定时函数
    :return:
    """
    print("执行定时任务")
    sys.stdout.flush()


if __name__ == '__main__':
    scheduled = create_scheduler(config)
    job_id = assignments(scheduled, my_job)
    # # scheduled_tasks(scheduled, my_job, 1)
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        close_scheduler(scheduled)
