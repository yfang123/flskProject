import wtforms
from wtforms.validators import length, email, EqualTo
from models import EmailCaptchaModel, UserModel
from flask import flash


# 创建一个登录的表单
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


# 创建一个注册表单验证，如果都通过就进行数据库校验，否则直接提示报错

class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=6, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=6, max=6)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_password(self, field):
        password = field.data
        password_confirm = self.password_confirm.data
        if password_confirm != password:
            flash("两次密码不相等!")
        if len(password) >= 6 and len(password) <= 20:
            flash("密码长度不匹配!")

    # 验证是否注册
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            flash("您的邮箱已经注册过了!")
            raise wtforms.ValidationError("您的邮箱已经注册过了!")

    # 邮箱验证
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # 在数据库中提取验证码
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        # 如果验证码不存在，或不相等，提示错误
        if not captcha_model or captcha_model.captcha != captcha:
            flash("邮箱验证码错误!")
            raise wtforms.ValidationError("邮箱验证码错误!")
