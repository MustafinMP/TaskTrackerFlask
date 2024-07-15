from flask import Flask, render_template
from flask_login import LoginManager

from auth.blueprint import blueprint as blueprint_auth, prefix as prefix_auth
from tasks.blueprint import blueprint as blueprint_tasks, prefix as prefix_tasks
from auth.models import User
from config import SECRET_KEY
import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


app.register_blueprint(blueprint_auth, url_prefix=prefix_auth)
app.register_blueprint(blueprint_tasks, url_prefix=prefix_tasks)


@app.route('/')
def index():
    return render_template('index.html', title='Homepage')


def main():
    db_session.global_init()
    app.run()


if __name__ == '__main__':
    main()


