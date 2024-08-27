from flask import Blueprint, abort, jsonify
from flask_login import login_required, current_user
import tasks.service as tasks_srv
from timer.timer import TimerManager

blueprint = Blueprint('timers', __name__)
prefix: str = '/timers'


timer_manager = TimerManager()


@blueprint.route('/create/<int:task_id>', methods=['GET'])
@login_required
def create_timer(task_id: int):
    if (task := tasks_srv.select_task_by_id(task_id)) is None:
        return jsonify({'status': 404, 'message': "Task doesn't exist"})
    if task.creator_id != current_user.id:
        return jsonify({'status': 403, 'message': "Forbidden"})

    timer_manager.add_timer(current_user.id, task_id)
    return jsonify({'status': 200, 'message': None})


@blueprint.route('/check', methods=['GET'])
@login_required
def get_time():
    if not timer_manager.has_timer(current_user.id):
        return jsonify({'status': 404, 'message': "Timer doesn't exist"})

    return jsonify({'status': 200, 'message': None, 'data': str(timer_manager.get_time(current_user.id))})


@blueprint.route('/pause', methods=['GET'])
@login_required
def pause():
    if not timer_manager.has_timer(current_user.id):
        return jsonify({'status': 404, 'message': "Timer doesn't exist"})

    timer_manager.pause(current_user.id)
    return jsonify({'status': 200, 'message': None, 'data': str(timer_manager.get_time(current_user.id))})


@blueprint.route('/continue', methods=['GET'])
@login_required
def cont():
    if not timer_manager.has_timer(current_user.id):
        return jsonify({'status': 404, 'message': "Timer doesn't exist"})

    timer_manager.cont(current_user.id)
    return jsonify({'status': 200, 'message': None, 'data': str(timer_manager.get_time(current_user.id))})


@blueprint.route('/terminate', methods=['POST'])
@login_required
def terminate():
    if not timer_manager.has_timer(current_user.id):
        return jsonify({'status': 404, 'message': "Timer doesn't exist"})

    data = timer_manager.save_and_terminate(current_user.id)

    return jsonify({'status': 200, 'message': None, 'data': str(data)})
