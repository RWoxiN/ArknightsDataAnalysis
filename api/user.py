from ast import Pass
from flask_login import UserMixin
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

from .model import DBUser, Account

def create_user(username, password):
    DBUser.get_or_create(username=username, defaults={'password': password})

def get_user(username):
    user = DBUser.get_or_none(DBUser.username == username)
    return user



class User(UserMixin):
    def __init__(self, user):
        self.dbuser = user
        self.username = user.username
        self.password = user.password
        self.id = user.id
    
    def verify_password(self, password):
        if self.password is None:
            return False
        if self.password == password:
            return True
        return False
    
    def add_acc(self, acc_uid):
        acc = Account.get_or_none(Account.uid == acc_uid)
        if acc is not None:
            acc.owner = self.dbuser
            acc.save()

    def get_accs_token(self):
        accs_token = []
        for ark_acc in self.dbuser.ark_accs:
            accs_token.append(ark_acc.token)
        return accs_token

    def get_id(self):
        return self.id
    
    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        user = DBUser.get_or_none(DBUser.id == user_id)
        return user


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password1 = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired()])