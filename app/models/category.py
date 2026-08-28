from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    kind = db.Column(db.String(20), nullable=False)  # "homework" or "bill"
    color = db.Column(db.String(7), default="#6c757d")  # hex color for UI tag

    __table_args__ = (
        db.UniqueConstraint("user_id", "name", "kind", name="uq_category_user_name_kind"),
    )

    def __repr__(self):
        return f"<Category {self.name} ({self.kind})>"
