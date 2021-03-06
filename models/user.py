from models import Model
from models.todo import Todo

import hashlib


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @staticmethod
    def salted_password(password, salt='$!@><?>EGI&WaKCs`'):
        """
        加盐哈希处理
        $!@><?>EGI&WaKCs`
        """
        salted = password + salt
        hash = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hash

    def validate_login(self):
        u = User.find_by(username=self.username)
        if u is not None:
            return u.password == self.salted_password(self.password)
        else:
            return False

    def validate_register(self):
        u = User.find_by(username=self.username)
        valid = u is None and len(self.username) > 2 and len(self.password) > 2
        if valid:
            p = self.password
            self.password = self.salted_password(p)
            return True
        else:
            return False
