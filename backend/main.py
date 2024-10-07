from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
# from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from prometheus_client import make_wsgi_app

from auth.service import get_user_by_id
from auth.views import blueprint as blueprint_auth, prefix as prefix_auth
from tasks.views import blueprint as blueprint_tasks, prefix as prefix_tasks
from timer.api_views import blueprint as blueprint_timer, prefix as prefix_timer
from teams.views import blueprint as blueprint_teams, prefix as prefix_teams
from teams.api_views import blueprint as blueprint_teams_api

from config import SECRET_KEY, HOST
import db_session

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = SECRET_KEY
# app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
#     '/metrics': make_wsgi_app()
# })

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


app.register_blueprint(blueprint_auth, url_prefix=prefix_auth)
app.register_blueprint(blueprint_tasks, url_prefix=prefix_tasks)
app.register_blueprint(blueprint_timer, url_prefix=f'/api{prefix_timer}')
app.register_blueprint(blueprint_teams, url_prefix=prefix_teams)
app.register_blueprint(blueprint_teams_api, url_prefix=f'/api{prefix_teams}')


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', title='Homepage')
    return redirect(url_for('auth.login'))


@app.errorhandler(404)
def error404(e):
    return render_template('errors/404.html')


def main():
    """Just a main function.

    :return: no return.
    """

    db_session.global_init()
    print('Запуск сервера')
    app.run(host=HOST)


if __name__ == '__main__':
    main()
