from app.models import Token
from app import db


def revoke_token(token):
    _token = Token.query.filter_by(access=token).first()
    db.session.remove(_token)
    db.session.commit()

