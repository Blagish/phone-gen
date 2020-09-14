from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, NumberRange


class BaseForm (FlaskForm):
    region_id = SelectField('Выберите регион:', coerce=int)
    provider_id = SelectField('Выберите провайдера связи', coerce=int)
    count = IntegerField('Укажите число запрашиваемых номеров', validators=[DataRequired(), NumberRange(1, 1000000)])
    submit = SubmitField('Запросить')
    region_chosen = BooleanField()

