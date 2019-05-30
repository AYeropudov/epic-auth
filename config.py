import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv((os.path.join(basedir, '.env'))) # создать файл .env со всеми переменными среды


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql+pymysql://epic:nNm7Xs0r@sqldb:3306/epic'
    JWT_KEY = os.environ.get('JWT_KEY') or 's9A1NDxIkPAqEIQHThy5Oh'
    BASE_DIR = basedir
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG') or 1
