from utils import log
from routes import json_response, current_user
from models.todo import Todo


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
def all(request):
    u = current_user(request)
    todos = Todo.find_all(user_id=u.id)
    ts = [t.json() for t in todos]
    return json_response(ts)


def add(request):
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json()
    u = current_user(request)
    log('form, request', form, u.id)
    # 创建一个 todo
    t = Todo.new(form, user_id=u.id)
    # 把创建好的 todo 返回给浏览器
    return json_response(t.json())


def delete(request):
    todo_id = int(request.query.get('id'))
    t = Todo.delete(todo_id)
    return json_response(t.json())


def update(request):
    form = request.json()
    # log('api todo update', form)
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return json_response(t.json())


def route_dict():
    d = {
        '/api/todo/all': all,
        '/api/todo/add': add,
        '/api/todo/delete': delete,
        '/api/todo/update': update,
    }
    return d
