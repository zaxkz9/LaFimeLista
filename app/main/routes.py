from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.main import main_bp
from app.models.bill import Bill
from app.models.homework import Homework


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    homeworks = Homework.query.filter_by(user_id=current_user.id).order_by(Homework.due_date.asc()).all()
    bills = Bill.query.filter_by(user_id=current_user.id).order_by(Bill.due_date.asc()).all()

    overdue_homeworks = [h for h in homeworks if h.is_overdue]
    due_soon_homeworks = [h for h in homeworks if h.is_due_soon()]
    overdue_bills = [b for b in bills if b.is_overdue]
    due_soon_bills = [b for b in bills if b.is_due_soon()]
    pending_homeworks = [h for h in homeworks if h.status == "pending"]
    pending_bills = [b for b in bills if b.status == "unpaid"]

    return render_template(
        "main/dashboard.html",
        overdue_homeworks=overdue_homeworks,
        due_soon_homeworks=due_soon_homeworks,
        overdue_bills=overdue_bills,
        due_soon_bills=due_soon_bills,
        pending_homeworks=pending_homeworks,
        pending_bills=pending_bills,
        pending_count=sum(1 for h in homeworks if h.status == "pending"),
        unpaid_count=sum(1 for b in bills if b.status == "unpaid"),
    )
