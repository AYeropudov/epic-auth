from app import app
from app import db
from app.models import User, Token
import pydevd_pycharm

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Token': Token}


if __name__ == '__main__':
    if app.config.get('FLASK_DEBUG'):
        pydevd_pycharm.settrace('192.168.255.1', port=37259, stdoutToServer=True, stderrToServer=True)
    app.run(host="0.0.0.0", debug=True)
