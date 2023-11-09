from flask import Flask

from .init_redis import init_redis, redis_store

from task_tool import apscheduler_task


def init_plugs(app: Flask) -> None:
    init_redis(app)


scheduled = apscheduler_task.create_scheduler(apscheduler_task.config)

# try:
#     while True:
#         pass
# except (KeyboardInterrupt, SystemExit):
#     apscheduler_task.close_scheduler(scheduled)
