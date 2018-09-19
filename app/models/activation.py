import secrets
import string

from app import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import uuid
from app.services.activation import ActivationSrvLocal


class Activation(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    code = db.Column(db.String(128))
    is_used = db.Column(db.Boolean, default=False)

    def __init__(self):
        self.is_used = False
        self.id = str(uuid.uuid4())

    def set_code(self, code):
        self.code = generate_password_hash(password=code)

    def check_code(self, _code):
        return check_password_hash(self.code, _code)

    def activate(self):
        self.is_used = True

    @classmethod
    def generate_random_code(cls):
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    def generate_for_user(self, user):
        self.user_id = user.id
        _code = self.generate_random_code()
        self.set_code(_code)
        ActivationSrvLocal.send(code=_code, user=user)

