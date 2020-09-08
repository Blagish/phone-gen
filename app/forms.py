from flask_wtf import FlaskForm, Form
from wtforms import SelectField, SubmitField, IntegerField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional


class BaseForm (FlaskForm):
    region = SelectField('Выберите регион:', coerce=int)
    provider = SelectField('Выберите провайдера связи', coerce=int, validate_choice=False)
    count = IntegerField('Укажите число запрашиваемых номеров')#, validators=[DataRequired(), NumberRange(1, 1000000)])
    submit = SubmitField('Запросить')
    set_region = SubmitField('Рассчитать доступные провайдеры на основе выбранного региона')
    region_chosen = BooleanField()

