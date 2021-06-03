from os import environ

from flask import jsonify, request, url_for

from app.api import bp
from app.models import Activation, User
from .errors import bad_request, error_response
from app import db


@bp.route('/activate', methods=['Post'])
def activate():
    data = request.get_json() or {}
    if data.get('code', None) is None:
        return bad_request('must include code field')
    user = User.query.get_or_404(request.environ.get("user").get('user_id', None))
    activation = Activation.query.filter_by(user_id=user.id, is_used=False).first()
    if activation.is_used:
        return bad_request('must use new code')
    if activation.check_code(data.get('code')):
        activation.activate()
        user = User.query.get(activation.user_id)
        if user.is_active:
            return bad_request('wrong activation')
        user.is_active = True
        db.session.commit()
        response = jsonify({})
        response.status_code = 200
        return response
    return bad_request('must include right code')
