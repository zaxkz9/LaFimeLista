from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.models.bill import BILL_CATEGORIES


class BillForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(max=150)])
    amount = DecimalField("Cantidad", validators=[DataRequired(), NumberRange(min=0)], places=2)
    category = SelectField(
        "Categoria",
        choices=[("", "Sin categoría")] + [(c, c) for c in BILL_CATEGORIES],
        validators=[Optional()],
    )
    due_date = DateField("Fecha de pago", validators=[DataRequired()])
    status = SelectField(
        "Status",
        choices=[("unpaid", "Pendiente"), ("paid", "Pagado")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Guardar")
