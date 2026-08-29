from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

REQUERIDO = "Este campo es obligatorio."

#Formato para el forms de registro de cuenta con sus condiciones
class RegisterForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(REQUERIDO), Length(max=120, message="Máximo %(max)d caracteres.")])
    username = StringField(
        "Usuario",
        validators=[DataRequired(REQUERIDO), Length(min=3, max=80, message="Debe tener entre %(min)d y %(max)d caracteres.")],
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(REQUERIDO), Length(min=8, message="Debe tener al menos %(min)d caracteres.")],
    )
    confirm_password = PasswordField(
        "Confirma tu contraseña",
        validators=[DataRequired(REQUERIDO), EqualTo("password", message="Las contraseñas no coinciden.")],
    )
    submit = SubmitField("Crear cuenta")


class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(REQUERIDO)])
    password = PasswordField("Contraseña", validators=[DataRequired(REQUERIDO)])
    submit = SubmitField("Inicia Sesión")
