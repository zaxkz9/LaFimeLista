from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    categories = db.relationship("Category", backref="user", lazy=True, cascade="all, delete-orphan")
    homeworks = db.relationship("Homework", backref="user", lazy=True, cascade="all, delete-orphan")
    bills = db.relationship("Bill", backref="user", lazy=True, cascade="all, delete-orphan")

#Definir la generación de contraseñas
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

#Definir el checkeo de contraseñas
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"
