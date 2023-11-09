from proxy_tool.app.routes.id import register_id_views
from proxy_tool.app.routes.proxy import register_proxy_views


# 注册所有路由，每个路由分支下__init__中，使用app进行注册蓝图
def init_view(app):
    register_id_views(app)
    register_proxy_views(app)


