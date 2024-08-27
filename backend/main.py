from flask import Flask, render_template
from flask_login import LoginManager

from auth.views import blueprint as blueprint_auth, prefix as prefix_auth
from tasks.views import blueprint as blueprint_tasks, prefix as prefix_tasks
from timer.api_views import blueprint as blueprint_timer, prefix as prefix_timer
from auth.models import User
from config import SECRET_KEY
import db_session
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)

LOCAL = False
HOST = 'localhost' if LOCAL else '192.168.0.14'


@login_manager.user_loader
def load_user(user_id):
    with db_session.create_session() as db_sess:
        return db_sess.get(User, user_id)


app.register_blueprint(blueprint_auth, url_prefix=prefix_auth)
app.register_blueprint(blueprint_tasks, url_prefix=prefix_tasks)
app.register_blueprint(blueprint_timer, url_prefix=f'/api{prefix_timer}')


@app.route('/')
def index():
    return render_template('index.html', title='Homepage')


def main():
    db_session.global_init()
    print('Запуск сервера')
    app.run(host=HOST)


if __name__ == '__main__':
    main()
