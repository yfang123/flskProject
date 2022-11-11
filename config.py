"""文件配置"""

USER = 'root'
PASSWORD = '123456'
DATABASE = 'zf_flask'  # 数据库名字
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@127.0.0.1:3306/%s' % (USER, PASSWORD, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 设置session加盐
SECRET_KEY = "jfwojdfw_afop++_+646fas?>>467"


#设置邮箱

MAIL_SERVER="smtp.qq.com"
MAIL_PORT=25
MAIL_USE_TLS=False
MAIL_USE_SSL=False
MAIL_DEBUG=True
MAIL_USERNAME="1140895906@qq.com"
MAIL_PASSWORD="abmmxaobwmeifhhc"
MAIL_DEFAULT_SENDER="1140895906@qq.com"

