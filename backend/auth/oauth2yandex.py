import requests
from flask import request
from flask_login import current_user, login_user

import db_session
from auth.repository import UserRepository
from config import YA_CLIENT_ID, YA_CLIENT_SECRET


def callback(code) -> None:
    token_url = 'https://oauth.yandex.ru/token'
    token_params = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': YA_CLIENT_ID,
        'client_secret': YA_CLIENT_SECRET
    }
    response = requests.post(token_url, data=token_params)
    data = response.json()
    if 'access_token' in data:
        user_info_url = 'https://login.yandex.ru/info'
        headers = {'Authorization': f'OAuth {data['access_token']}'}
        user_info_response = requests.post(user_info_url, headers=headers)
        user_info = user_info_response.json()
        # username = user_info.get('login')
        # email = user_info.get('default_email')
        yandex_uid = str(user_info.get('id'))
        login_by_yandex_uid(yandex_uid)


def login_by_yandex_uid(uid: str) -> None:
    with db_session.create_session() as session:
        repository = UserRepository(session)
        user = repository.get_by_yandex_id(uid)
        if not current_user.is_authenticated:
            login_user(user, remember=True)
            return
        if current_user.oauth_yandex_id is None:
            repository.add_yandex_oauth_id(current_user.id, uid)
