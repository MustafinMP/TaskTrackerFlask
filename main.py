from flask import Flask
from flask_login import LoginManager

from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)


if __name__ == '__main__':
    ...


