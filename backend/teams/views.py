from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from teams.forms import CreateTeamForm
from teams.invite_link_service import generate_link, join_to_team
import teams.service as srv

blueprint = Blueprint('teams', __name__)
prefix: str = '/teams'


@blueprint.route('/all')
@login_required
def user_teams():
    return render_template(prefix + '/teams.html', teams=srv.get_user_teams_by_id(current_user.id))


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_team():
    create_form = CreateTeamForm()
    if create_form.validate_on_submit():
        srv.add_team(current_user.id, create_form.team_name.data)
        return redirect('/teams/all')
    return render_template(prefix + '/create_team.html', form=create_form, title='Создать команду')


@blueprint.route('<int:team_id>/invite')
@login_required
def invite(team_id: int):
    invite_link = generate_link(team_id)
    return render_template(prefix + '/invite.html', invite_link=invite_link)


@blueprint.route('/join')
@login_required
def join_team():
    link_id = int(request.args.get('id'))
    key = request.args.get('key')
    join_to_team(link_id, key, current_user.id)
    return redirect(url_for('teams.user_teams'))


@blueprint.route('/<int:team_id>')
@login_required
def single_team(team_id: int):
    team = srv.get_team_by_id(team_id)
    invite_link = generate_link(team_id)
    return render_template(prefix + '/single_team.html', invite_link=invite_link, team=team)