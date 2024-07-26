from flask import Blueprint, redirect, render_template, request, abort, jsonify
from flask_login import login_required, current_user
from sqlalchemy import and_

import db_session
from baskets.forms import CreateBasketForm
from baskets.models import Basket
from tasks.models import Task

blueprint = Blueprint('baskets', __name__)
prefix: str = '/baskets'


@blueprint.route('/')
def all_baskets():
    baskets: list = list()
    if current_user.is_authenticated:
        session = db_session.create_session()
        baskets: list = session.query(Basket).where(current_user.id == Basket.creator_id).all()
    return render_template(prefix + '/tasks.html', baskets=baskets)


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def add_basket():
    form = CreateBasketForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        basket = Basket()
        basket.name = form.name.data
        basket.description = form.description.data
        basket.creator_id = current_user.get_id()
        session.add(basket)
        session.commit()
        return redirect('/baskets')
    return render_template(prefix + '/create.html', form=form, title='Добавить корзину')


@blueprint.route('/<int:basket_id>', methods=['GET', 'POST'])
@login_required
def get_basket(basket_id: int):
    if not current_user.is_authenticated:
        return abort(404)
    with db_session.create_session() as session:
        basket: Basket = session.query(Basket).where(
            and_(current_user.id == Basket.creator_id, Basket.id == basket_id)).first()
        if not basket:
            return abort(404)
        return render_template(prefix + '/show_task.html', basket=basket)


# API
@blueprint.route('/<int:basket_id>', methods=['GET', 'POST'])
@login_required
def get_basket(basket_id: int):
    if not current_user.is_authenticated:
        return abort(404)
    with db_session.create_session() as session:
        basket: Basket = session.query(Basket).where(
            and_(current_user.id == Basket.creator_id, Basket.id == basket_id)).first()
        if not basket:
            return abort(404)
        return render_template(prefix + '/show_task.html', basket=basket)


@blueprint.route('api/get_basket/<int:basket_id>')
@login_required
def get(basket_id: int):
    with db_session.create_session() as session:
        basket: Basket = session.query(Basket).where(
            and_(current_user.id == Basket.creator_id, Basket.id == basket_id)).first()
        tasks: list[Task] = session.query(Task).where(
            and_(current_user.id == Task.creator_id, Task.basket_id == basket_id)).all()
        return jsonify(
            {
                'basket': basket.to_dict(only=('name', 'creator.name', 'description')),
                'tasks': [task.to_dict(only=('name', 'description', 'status')) for task in tasks]
            }
        )


@blueprint.route('/api/add_to_basket/<int:basket_id>/<int:task_id>', methods=['POST'])
@login_required
def add_to_basket(basket_id: int, task_id: int):
    with db_session.create_session() as session:
        basket: Basket = session.query(Basket).where(
            and_(current_user.id == Basket.creator_id, Basket.id == basket_id)).first()
        task: Task = session.query(Basket).where(
            and_(current_user.id == Task.creator_id, Task.id == task_id)).first()
        if not task or not basket:
            return abort(404)
        task.basket_id = basket_id
        session.commit()
