import functools

from flask import jsonify, request, url_for
import requests
from app.api import bp
from app.models import User, Token, Activation
from .errors import bad_request, error_response
from app import db


def google_wrapper(*args, **kws):
    print("some action")
    token = request.headers.get('X-RECAPTCHA-TOKEN')
    print(token)
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': '6LdsQawUAAAAABSDsD_DTLegnyU5Iy9ISou3tN_w', 'response': token}
    )
    response = response.json()
    print(response)
    return response.get('success')


@bp.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    return jsonify(User.query.get_or_404(id).to_dict_open())


@bp.route('/users/<string:username>', methods=['GET'])
def get_users_by_username(username):
    return jsonify(
        User.to_collection_dict(
            query=User.query.filter(User.user_name.contains(username), User.is_active.__eq__(True)),
            page=1,
            per_page=10,
            endpoint='api.get_users_by_username',
            username=username
        )
    )


@bp.route('/users', methods=['POST'])
def create_user():
    if google_wrapper(request=request):
        data = request.get_json() or {}
        if 'user_name' not in data or 'email' not in data or 'password' not in data:
            return bad_request('must include username, email and password fields')
        if not check_user_duplicates(user_name=data['user_name']):
            return bad_request('please use a different username')
        if not check_user_duplicates(email=data['email']):
            return bad_request('please use a different email address')
        user = User()
        user.from_dict(data, new_user=True)
        db.session.add(user)
        db.session.commit()
        activation = Activation()
        activation.generate_for_user(user)
        db.session.add(activation)
        db.session.commit()
        body = user.to_dict_private()
        _token = Token()
        _token.generate(user=user)
        db.session.add(_token)
        db.session.commit()
        body["jwt"] = _token.encode().decode('utf-8')
        response = jsonify(body)
        response.status_code = 201
        return response
    else:
        return bad_request('SPAM detected. Protection rule')


@bp.route('/auth', methods=['GET'])
def check():
    response = jsonify({})
    response.status_code = 200
    return response


@bp.route('/me', methods=['GET'])
def me():
    user = User.query.get_or_404(request.environ.get('user').get('user_id'))
    response = jsonify(user.to_dict_private())
    response.status_code = 200
    return response




@bp.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user_to_update = User.query.get_or_404(user_id)
    if not user_to_update.is_active:
        return bad_request('user not found or not activate')
    data = request.get_json() or {}
    if 'user_name' in data and user_to_update.user_name != data['user_name'] and not check_user_duplicates(
            user_name=data['user_name']):
        return bad_request('username already in use')
    if 'email' in data and user_to_update.email != data['email'] and not check_user_duplicates(email=data['email']):
        return bad_request('email already in use')
    user_to_update.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user_to_update.to_dict_private())


def check_user_duplicates(**kwargs):
    return False if User.query.filter_by(**kwargs).first() else True


@bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json() or {}
    if 'email' not in data or 'password' not in data:
        return error_response(status_code=412, message='payload are not full')
    find_user = User.query.filter_by(email=data.get('email', None)).first()
    if find_user is None:
        return bad_request('User not found')
    check = find_user.check_password(password=data.get('password'))
    if check:
        _token = Token.query.filter_by(user_id=find_user.id).first()
        if _token is None:
            _token = Token()
            _token.generate(user=find_user)
            db.session.add(_token)
        else:
            _token.regenerate()

        db.session.commit()
        return jsonify({"jwt": _token.encode().decode('utf-8')})
