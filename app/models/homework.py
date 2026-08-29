from datetime import date, timedelta

from app.extensions import db

#Declaración status tareas
STATUS_PENDING = "pending"
STATUS_DONE = "done"

#Categorías predeterminadas para tareas (menú fijo, no editable por el usuario)
HOMEWORK_CATEGORIES = ["Tarea", "PIA", "Examen", "Otro"]
HOMEWORK_CATEGORY_COLORS = {
    "Tarea": "#4f46e5",
    "PIA": "#16a34a",
    "Examen": "#dc2626",
    "Otro": "#6b7280",
}


class Homework(db.Model):
    __tablename__ = "homeworks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(100), nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=STATUS_PENDING)

#Si la tarea no es entregada y la fecha limite es menor a la fecha de hoy, mostrar aviso
    @property
    def is_overdue(self):
        return self.status != STATUS_DONE and self.due_date < date.today()

#Si la tarea no ha sido entregada y la fecha es menor o igual a la de entrega o menor 
# o igual a la de hoy más el tiempo delta, avisar
    def is_due_soon(self, days=3):
        if self.status == STATUS_DONE:
            return False
        today = date.today()
        return today <= self.due_date <= today + timedelta(days=days)

    def __repr__(self):
        return f"<Homework {self.title}>"
