from flask import Flask, session, g
import config
from exts import db, mail
from blueprints import qa_bp
from blueprints import user_bp
from flask_migrate import Migrate
from models import UserModel

app = Flask(__name__)
# 绑定config
app.config.from_object(config)
# 绑定exts,数据库和邮箱
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)


@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个user的变量   值是user
            g.user = user
        except:
            g.user = None


# 请求  ---》before_request---》视图函数---》视图函数中返回的模板----》context_processor
@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    # https://blog.csdn.net/m0_37997046/article/details/86304398
    app.run(host='0.0.0.0', port=10, debug=True)
