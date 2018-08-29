from flask import jsonify, request, url_for

from app.api import bp
from app.models import User
from .errors import bad_request
from app import db


@bp.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    return jsonify(User.query.get_or_404(id).to_dict_open())


@bp.route('/users/<string:username>', methods=['GET'])
def get_users_by_username(username):
    return jsonify(
        User.to_collection_dict(
            query=User.query.filter(User.user_name.contains(username)),
            page=1,
            per_page=10,
            endpoint='api.get_users_by_username',
            username=username
        )
    )


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'user_name' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(user_name=data['user_name']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict_open())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user_by_id', id=user.id)
    return response


@bp.route('/users', methods=['PATCH'])
def update_user():
    pass

