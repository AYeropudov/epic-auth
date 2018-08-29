import datetime
import uuid
from app import db
import jwt
from app import Config
from app import exceptions


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    access = db.Column(db.String(40))
    expired_at = db.Column(db.Integer)
    created_at = db.Column(db.Integer)

    def generate(self, user):
        self.user_id = user.id
        self.access = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()
        self.expired_at = datetime.datetime.utcnow() + datetime.timedelta(days=10)

    def encode(self):
        _dict = {
            "token": self.access,
            "exp": self.expired_at
        }
        return jwt.encode(payload=_dict, key=Config.JWT_KEY, algorithm='HS256')

    @classmethod
    def decode_jwt(cls, jwt_str):
        _decoded = jwt.decode(jwt=jwt_str, key=Config.JWT_KEY, algorithms=['HS256'])
        if _decoded.get('exp', 0) < datetime.datetime.utcnow():
            return _decoded
        else:
            raise exceptions.TokenExpired



