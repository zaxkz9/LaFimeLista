from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.bills import bills_bp
from app.bills.forms import BillForm
from app.extensions import db
from app.models.bill import BILL_CATEGORIES, BILL_CATEGORY_COLORS, Bill


@bills_bp.route("/")
@login_required
def list_bills():
    query = Bill.query.filter_by(user_id=current_user.id)

    status = request.args.get("status")
    if status in ("unpaid", "paid"):
        query = query.filter_by(status=status)

    category = request.args.get("category")
    if category:
        query = query.filter_by(category=category)

    bills = query.order_by(Bill.due_date.asc()).all()
    return render_template(
        "bills/list.html",
        bills=bills,
        categories=BILL_CATEGORIES,
        category_colors=BILL_CATEGORY_COLORS,
    )


@bills_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_bill():
    form = BillForm()

    if form.validate_on_submit():
        bill = Bill(
            user_id=current_user.id,
            name=form.name.data,
            amount=form.amount.data,
            category=form.category.data or None,
            due_date=form.due_date.data,
            status=form.status.data,
        )
        db.session.add(bill)
        db.session.commit()
        flash("Recibo añadido.", "success")
        return redirect(url_for("bills.list_bills"))

    return render_template("bills/form.html", form=form, title="Nuevo recibo")


@bills_bp.route("/<int:bill_id>/edit", methods=["GET", "POST"])
@login_required
def edit_bill(bill_id):
    bill = Bill.query.filter_by(id=bill_id, user_id=current_user.id).first_or_404()
    form = BillForm(obj=bill)

    if form.validate_on_submit():
        bill.name = form.name.data
        bill.amount = form.amount.data
        bill.category = form.category.data or None
        bill.due_date = form.due_date.data
        bill.status = form.status.data
        db.session.commit()
        flash("Recibo actualizado.", "success")
        return redirect(url_for("bills.list_bills"))

    return render_template("bills/form.html", form=form, title="Editar recibo")


@bills_bp.route("/<int:bill_id>/delete", methods=["POST"])
@login_required
def delete_bill(bill_id):
    bill = Bill.query.filter_by(id=bill_id, user_id=current_user.id).first_or_404()
    db.session.delete(bill)
    db.session.commit()
    flash("Recibo borrado.", "info")
    return redirect(url_for("bills.list_bills"))
