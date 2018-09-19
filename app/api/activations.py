from flask import jsonify, request, url_for

from app.api import bp
from app.models import Activation, User
from .errors import bad_request, error_response
from app import db


@bp.route('/activate/<string:hash_code>', methods=['Post'])
def activate(hash_code):
    data = request.get_json() or {}
    if data.get('code', None) is None:
        return bad_request('must include code field')
    activation = Activation.query.get_or_404(hash_code)
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
