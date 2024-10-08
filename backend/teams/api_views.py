from flask import Blueprint, jsonify
from flask_login import login_required

from teams.invite_link_service import generate_link
import teams.service as srv

blueprint = Blueprint('teams_api', __name__)


# @blueprint.route('/<int:team_id>', methods=['GET'])
# @login_required
# def team_info(team_id: int):
#     team_data: dict = srv.get_team_data_by_id(team_id)
#     return jsonify(
#         {
#             'status': 200,
#             'data': {
#                 'team': team_data
#             }
#         }
#     )


@blueprint.route('invite/<int:team_id>')
@login_required
def invite(team_id: int):
    invite_link = generate_link(team_id)
    return jsonify(
        {
            'status': 200,
            'data': {
                'invite_link': invite_link
            }
        }
    )
