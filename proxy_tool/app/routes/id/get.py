"""
雪花ID生成接口
"""
from flask import Blueprint
from flask import request, jsonify
from ....app.common.rights import authorize
from ....app.tool.id.id_generator import IdGenerator
from ....app.tool.id.id_seq import IdSeq

ID = Blueprint('ID', __name__, url_prefix='/id')


# id获取端口
@ID.get('/get/')
@authorize()
def index():
    num = int(request.args.get('num', 50))
    i = 0
    id_list = []
    worker = IdGenerator(IdSeq.coresecurity.value)
    while i < num:
        id = worker.get_id()
        id_list.append(id)
        i += 1
    err = {
        "id": id_list
    }
    return jsonify(err)


@ID.route('/post/', methods=['GET', 'POST'])
@authorize()
def about():
    if request.method == 'POST':
        # 处理 POST 请求
        # 可以通过 request.form 或 request.json 来获取 POST 请求的数据
        # data = request.form  # 或 request.json，取决于请求的 Content-Type
        # 处理数据并返回响应
        return 'POST 请求成功'

    # 处理其他类型的请求（如 GET 请求）
    return '不支持的请求方法'
