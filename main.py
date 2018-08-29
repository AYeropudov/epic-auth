from app import app
from app import db
from app.models import User, Token


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Token': Token}


if __name__ == '__main__':
    app.run()
