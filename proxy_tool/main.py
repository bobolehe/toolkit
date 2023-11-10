from app import create_app
from task_tool.apscheduler_task import scheduler
import atexit

app = create_app()


def cleanup_function():
    scheduler.shutdown()


atexit.register(cleanup_function)

# 启动
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=False)
