from datetime import timedelta, datetime

from flask import url_for
from sqlalchemy import update, select, and_
from werkzeug.security import generate_password_hash, check_password_hash

import db_session
from config import INVITE_LINK_SALT
from teams.models import InviteLink
from teams.service import add_new_team_members


def generate_link(team_id: int):
    create_datetime = datetime.now()
    primary_key: str = generate_primary_key(team_id, create_datetime)  # отдаем пользователю
    secondary_key: str = generate_secondary_key(primary_key)  # храним у себя
    link_id = add_link_to_db(team_id, create_datetime, secondary_key)
    return f"{url_for('teams.join_team')}?id={id}&key={primary_key}"


def add_link_to_db(team_id: int, create_datetime: datetime, secondary_key: str) -> int:
    new_link = InviteLink(
        team_id=team_id,
        burn_datetime=create_datetime + timedelta(days=2),
        key=secondary_key
    )
    update_stmt = update(InviteLink).where(
        InviteLink.is_active is True
    ).values(is_active=False)
    with db_session.create_session() as session:
        session.add(new_link)
        session.execute(update_stmt)
        session.commit()
    return new_link.id


def generate_primary_key(team_id: int, create_datetime: datetime) -> str:
    return generate_password_hash(f'{INVITE_LINK_SALT}{team_id}{str(create_datetime)}')


def generate_secondary_key(primary_hash: str) -> str:
    return generate_password_hash(primary_hash)


def join_to_team(link_id: int, key: str, user_id: int) -> None:
    stmt = select(InviteLink).where(
        and_(
            InviteLink.id == link_id,
            InviteLink.is_active == True
        )
    )
    with db_session.create_session() as session:
        link_obj = session.scalar(stmt)
        if check_password_hash(link_obj.key, key):
            add_new_team_members(link_obj.team_id, user_id)