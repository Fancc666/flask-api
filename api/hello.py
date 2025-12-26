from flask import Blueprint, jsonify
from api.__Kit import myResponse

bp = Blueprint('hello', __name__, url_prefix='/api')

@bp.route('/')
def hello_api():
    return myResponse(code=0, msg='ok!测试成功\nHello Fancc API!')

# 测试蓝图