from task_tool import apscheduler_task

scheduled = apscheduler_task.create_scheduler(apscheduler_task.config)
try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    apscheduler_task.close_scheduler(scheduled)