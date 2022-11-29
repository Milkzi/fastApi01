import time

from flask import Flask
from setting import SQLALCHEMY_DATABASE_URI
from apps.flask.model import db
from apps.flask.api.api import api_app
from apps.flask.ss.ssapi import ss_login_app
from datetime import timedelta







def create_flask_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    # templates
    app.jinja_env.auto_reload = True

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # redis
    app.config['SECRET_KEY'] = 'hu123456'
    # app.config['SESSION_TYPE'] = 'redis'
    # app.config['SESSION_PERMANENT'] = False
    # app.config['SESSION_USE_SIGNER'] = False
    # app.config['SESSION_KEY_PREFIX '] = 'ff_session:'
    # app.config['SESSION_REDIS'] = redis.Redis(host='192.168.5.1', port=6379)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
    # mysql
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SQLALCHEMY_POOL_SIZE"] = 60
    app.config["SQLALCHEMY_MAX_OVERFLOW"] = 40
    app.config["SQLALCHEMY_POOL_TIMEOUT"] = 10
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 120

    # Session(app)
    db.init_app(app)

    app.register_blueprint(api_app)
    app.register_blueprint(ss_login_app)

    return app



