import time

from models import Model
from utils import formatted_time, log


class Todo(Model):
    """
    Todo.new() 来创建一个 todo
    """

    def __init__(self, form):
        super().__init__(form)
        self.task = form.get('task', '')
        self.completed = False
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        # 默认不关联任何用户
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('created_time')
        self.updated_time = form.get('updated_time')

    @classmethod
    def new(cls, form, **kwargs):
        log('newtodo', form, kwargs)
        m = cls(form)

        # for name in cls.valid_names():
        #     k, t, v = name
        #     if k in form:
        #         setattr(m, k, t(form[k]))
        #     else:
        #         # 设置默认值
        #         setattr(m, k, v)

        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        t = int(time.time())
        m.created_time = t
        m.updated_time = t
        log('newtodo-5', m)
        m.save()
        return m

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            'task',
        ]
        for key in form:
            # form 类型是 dict
            # 这里只应该更新想要更新的东西
            # 使用 setattr()设置属性值：setattr(object, name, value)
            if key in valid_names:
                setattr(t, key, form[key])
        t.updated_time = int(time.time())
        t.save()
        return t

    def is_owner(self, id):
        return self.user_id == id

    def formatted_created_time(self):
        return formatted_time(self.created_time)

    def formatted_updated_time(self):
        return formatted_time(self.updated_time)
