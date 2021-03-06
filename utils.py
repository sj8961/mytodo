import time
from datetime import datetime

from jinja2 import Environment, FileSystemLoader


def log(*args, **kwargs):
    # time.time() 返回 unix time
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)
    # a append 追加模式
    with open('log.liu.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


path = 'templates'
# 创建一个加载器, jinja2从目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)


def template(path, **kwargs):
    """
    接受一个路径和一系列参数
    读取模板并渲染返回
    """
    t = env.get_template(path)
    return t.render(**kwargs)


def formatted_time(unixtime):
    dt = time.localtime(unixtime)
    ds = time.strftime('%Y-%m-%d %H:%M:%S', dt)
    return ds
