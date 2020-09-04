from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class BaseForm (FlaskForm):
    region = SelectField('Выберите регион:', coerce=int)
    provider = SelectField('Выберите провайдера связи', coerce=int)
    count = IntegerField('Укажите число запрашиваемых номеров', validators=[DataRequired()])
    submit = SubmitField('Запросить')
