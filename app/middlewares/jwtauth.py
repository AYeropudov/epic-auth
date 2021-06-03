import jwt
from werkzeug.wrappers import Request, Response, ResponseStream
from config import Config


class middlewareAuth():
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        if request.path in ['/api/users', '/api/login']:
            pass
        else:
            auth = (self.decode_jwt(jwt_str=request.headers['auth']))
            environ['user'] = auth
        return self.app(environ, start_response)
        # these are hardcoded for demonstration
        # verify the username and password from some database or env config variable
        # if userName == self.userName and password == self.password:
        #     environ['user'] = {'name': 'Tony'}
        #     return self.app(environ, start_response)
        #
        # res = Response(u'Authorization failed', mimetype='text/plain', status=401)
        # return res(environ, start_response)

    def decode_jwt(cls, jwt_str):
        try:
            _decoded = jwt.decode(jwt=jwt_str, key=Config.JWT_KEY, algorithms=['HS256'])
            return _decoded
        except jwt.ExpiredSignatureError:
            raise jwt.exceptions.TokenExpired