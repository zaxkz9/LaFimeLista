from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.models.bill import BILL_CATEGORIES


REQUERIDO = "Este campo es obligatorio."


class BillForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(REQUERIDO), Length(max=150, message="Máximo %(max)d caracteres.")])
    amount = DecimalField(
        "Cantidad",
        validators=[DataRequired(REQUERIDO), NumberRange(min=0, message="Debe ser mayor o igual a %(min)s.")],
        places=2,
    )
    category = SelectField(
        "Categoria",
        choices=[("", "Sin categoría")] + [(c, c) for c in BILL_CATEGORIES],
        validators=[Optional()],
    )
    due_date = DateField("Fecha de pago", validators=[DataRequired(REQUERIDO)])
    status = SelectField(
        "Status",
        choices=[("unpaid", "Pendiente"), ("paid", "Pagado")],
        validators=[DataRequired(REQUERIDO)],
    )
    submit = SubmitField("Guardar")
