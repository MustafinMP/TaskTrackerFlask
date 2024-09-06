from flask import Blueprint, render_template
from flask_login import login_required, current_user

from teams.models import Team
from teams.service import get_user_teams

blueprint = Blueprint('teams', __name__)
prefix: str = '/teams'


@blueprint.route('/all')
@login_required
def user_teams():
    return render_template(prefix + '/teams.html', teams=get_user_teams(current_user.id))