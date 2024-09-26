from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateTeamForm(FlaskForm):
    team_name = StringField('Название команды', validators=[DataRequired()])
    submit = SubmitField('Создать')