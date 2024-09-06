from flask import Blueprint, render_template
from flask_login import login_required, current_user

from teams.models import Team

blueprint = Blueprint('teams', __name__)
prefix: str = '/teams'


@blueprint.route('/all')
@login_required
def user_teams():
    return render_template(prefix + '/teams.html')