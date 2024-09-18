from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from teams.models import Team
from teams.service import get_user_teams, get_team_by_id, LinkGenerator, add_new_team_members

blueprint = Blueprint('teams', __name__)
prefix: str = '/teams'


@blueprint.route('/all')
@login_required
def user_teams():
    return render_template(prefix + '/teams.html', teams=get_user_teams(current_user.id))


@blueprint.route('<int:team_id>/invite')
@login_required
def invite(team_id: int):
    invite_link = LinkGenerator.generate_link(team_id)
    return render_template(prefix + '/invite.html', invite_link=invite_link)


@blueprint.route('/join_team')
@login_required
def join_team():
    team_id = int(request.args.get('team_id'))
    key = request.args.get('key')
    if LinkGenerator.check_key(team_id, key):
        add_new_team_members(team_id, current_user.id)
    return redirect(url_for('teams.user_teams'))


@blueprint.route('/<int:team_id>')
@login_required
def single_team(team_id: int):
    #team = get_team_by_id(team_id)
    invite_link = LinkGenerator.generate_link(team_id)
    return render_template(prefix + '/single_team.html', invite_link=invite_link)