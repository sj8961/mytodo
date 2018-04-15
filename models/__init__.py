import json

from utils import log


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        return json.loads(s)


class Model(object):
    """
    Model 是所有 model 的基类
    """

    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def _new_from_dict(cls, d):
        # 因为子元素的 __init__ 需要一个 form 参数
        # 所以给一个空字典
        m = cls({})
        for k, v in d.items():
            # setattr 是一个特殊的函数
            # 假设 k v 分别是 'name'  'liu'
            # 它相当于 m.name = 'liu'
            setattr(m, k, v)
        return m


    @classmethod
    def all(cls):
        """
        all 方法使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def new(cls, form, **kwargs):
        m = cls(form, **kwargs)
        return m

    @classmethod
    def find_by(cls, **kwargs):
        # log('kwargs, ', kwargs, type(kwargs))
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def find_all(cls, **kwargs):
        # log('kwargs, ', kwargs, type(kwargs))
        models = []
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                models.append(m)
        return models


    # @classmethod
    # def valid_names(cls):
    #     names = [
    #         # (字段名, 类型, 默认值)
    #         ('deleted', bool, False),
    #         ('created_time', int, 0),
    #         ('updated_time', int, 0),
    #     ]
    #     return names

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        models = self.all()

        first_index = 0
        if self.id is None:
            # log('id is None')
            if len(models) > 0:
                # 末尾加1
                self.id = models[-1].id + 1
            else:
                log('first index', first_index)
                self.id = first_index
            models.append(self)
        else:
            # log('id is not None')
            # 有 id 说明已经是存在于数据文件中的数据
            # 那么就找到这条数据并替换
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        # 保存
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # 判断是否找到了这个 id 的数据
        if index != -1:
            o = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            # 返回被删除的元素
            return o

    def json(self):
        """
        返回当前 model 的字典表示
        """
        d = self.__dict__
        return d

    @classmethod
    def all_json(cls):
        ms = cls.all()
        # 要转换为 dict 格式
        js = [t.json() for t in ms]
        return js
