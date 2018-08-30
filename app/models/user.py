import secrets
import string
from app import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from .models import PaginatedAPIMixin


class User(PaginatedAPIMixin, db.Model):
    FIELDS = ['user_name', 'email']
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "User {}".format(self.user_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict_open(self):
        return {
            "id": self.id,
            "username": self.user_name
        }

    def to_dict_private(self):
        return {
            "id": self.id,
            "username": self.user_name,
            "email": self.email
        }

    def from_dict(self, adict, new_user=False):
        for field in self.FIELDS:
            if field in adict:
                setattr(self, field, adict[field])
        if new_user:
            self.set_password(adict.get('password', self.generate_random_password()))

    @classmethod
    def generate_random_password(cls):
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
