from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class HomeworkForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(max=150)])
    subject = StringField("Materia", validators=[Optional(), Length(max=100)])
    category_id = SelectField("Categoria", coerce=int, validators=[Optional()])
    due_date = DateField("Fecha de Entrega", validators=[DataRequired()])
    status = SelectField(
        "Status",
        choices=[("pending", "Pendiente"), ("done", "Terminada")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Guardar")
