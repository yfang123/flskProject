from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from exts import mail, db
from flask_mail import Message  # 导入邮箱的信息
from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
# from forms import RegisterForm
# 哈希加密 generate_password_hash 对密码进行加密    check_password_hash(加密之后的密码，加密之前的密码)  对密码进行解密
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user", __name__, url_prefix="/user")


# 退出登录
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("user.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = request.form
        print(form)
        # email = form.email.data
        # password = form.password.data

        # user = UserModel.query.filter_by(email=email).first()
        # if not user:
        #     flash("该邮箱还未注册,请先去注册!")
        #     return redirect(url_for("user.login"))
        #
        # # 进行密码校验
        # if user and check_password_hash(user.password, password):
        #     session["user_id"] = user.id
        #     return redirect("/")
        # else:
        #     flash("邮箱和密码不匹配!")
        #     return redirect(url_for("user.login"))
    # else:
    # flash("邮箱和密码格式错误!")
    # return redirect(url_for("user.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        form = request.form
        print(form)
        # email = form.email.data
        # username = form.username.data
        # password = form.password.data
        # # 对密码进行加密
        # hash_password = generate_password_hash(password)
        # # 添加进数据库
        # user = UserModel(username=username, email=email, password=hash_password)
        # db.session.add(user)
        # db.session.commit()
        # return redirect(url_for("user.login"))
        # else:
        #     return render_template("register.html")


@bp.route("/captcha", methods=["POST"])
def get_captcha():
    email = request.form.get("email")
    # 生成随机6为验证码
    letters = string.digits
    captcha = "".join(random.sample(letters, 6))
    print("验证码", captcha)
    if email:
        message = Message(
            subject="XX问答：",
            recipients=[email],
            body=f"【XX问答】您的注册验证码是:{captcha},5分钟内有效。任意索要验证码的都是骗子，千万别给!"
        )
        mail.send(message)
        # 判断数据库中是否有这个邮箱或者验证码
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        # 如果存在了就更新验证码，时间
        if captcha_model:
            captcha_model.captcah = captcha
            captcha_model.captcha_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        return jsonify({"code": 200, "massage": "success"})

    else:
        return jsonify({"code": 400, "massage": "请先输入邮箱!"})
