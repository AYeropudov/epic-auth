from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.middlewares import middlewareAuth

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
from app import models
from app import exceptions

from app.api import bp as api_bp

app.wsgi_app = middlewareAuth(app.wsgi_app)

app.register_blueprint(blueprint=api_bp, url_prefix='/api')




