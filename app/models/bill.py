from datetime import date, timedelta
from app.extensions import db

#Status de pago recibos
STATUS_UNPAID = "unpaid"
STATUS_PAID = "paid"


class Bill(db.Model):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    name = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=STATUS_UNPAID)

    category = db.relationship("Category")

#Si el status de pago es diferente a verdad mostrar la fecha que debio pagar
    @property
    def is_overdue(self):
        return self.status != STATUS_PAID and self.due_date < date.today()
    
#Si el pago todavia no ha sido realizado y la fecha es menor
# o igual a la de pago o menor o igual a 3 días mostrar en dashboard
    def is_due_soon(self, days=3):
        if self.status == STATUS_PAID:
            return False
        today = date.today()
        return today <= self.due_date <= today + timedelta(days=days)

    def __repr__(self):
        return f"<Bill {self.name}>"
