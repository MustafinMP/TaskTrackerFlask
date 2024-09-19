from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from teams.invite_link_service import generate_link, join_to_team
from teams.service import get_user_teams

blueprint = Blueprint('teams', __name__)
prefix: str = '/teams'


@blueprint.route('/all')
@login_required
def user_teams():
    return render_template(prefix + '/teams.html', teams=get_user_teams(current_user.id))


@blueprint.route('<int:team_id>/invite')
@login_required
def invite(team_id: int):
    invite_link = generate_link(team_id)
    return render_template(prefix + '/invite.html', invite_link=invite_link)


@blueprint.route('/join_team')
@login_required
def join_team():
    link_id = int(request.args.get('team_id'))
    key = request.args.get('key')
    join_to_team(link_id, key, current_user.id)
    return redirect(url_for('teams.user_teams'))


@blueprint.route('/<int:team_id>')
@login_required
def single_team(team_id: int):
    #team = get_team_by_id(team_id)
    invite_link = generate_link(team_id)
    return render_template(prefix + '/single_team.html', invite_link=invite_link)