from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from app.models.homework import HOMEWORK_CATEGORIES


REQUERIDO = "Este campo es obligatorio."


class HomeworkForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(REQUERIDO), Length(max=150, message="Máximo %(max)d caracteres.")])
    subject = StringField("Materia", validators=[Optional(), Length(max=100, message="Máximo %(max)d caracteres.")])
    category = SelectField(
        "Categoria",
        choices=[("", "Sin categoría")] + [(c, c) for c in HOMEWORK_CATEGORIES],
        validators=[Optional()],
    )
    due_date = DateField("Fecha de Entrega", validators=[DataRequired(REQUERIDO)])
    status = SelectField(
        "Status",
        choices=[("pending", "Pendiente"), ("done", "Terminada")],
        validators=[DataRequired(REQUERIDO)],
    )
    submit = SubmitField("Guardar")
