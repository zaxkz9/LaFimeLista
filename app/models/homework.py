from datetime import date, timedelta

from app.extensions import db

#Declaración status tareas
STATUS_PENDING = "pending"
STATUS_DONE = "done"


class Homework(db.Model):
    __tablename__ = "homeworks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(100), nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=STATUS_PENDING)

    category = db.relationship("Category")

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
