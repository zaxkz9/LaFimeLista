from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.homeworks import homeworks_bp
from app.homeworks.forms import HomeworkForm
from app.models.category import Category
from app.models.homework import Homework


def _category_choices():
    categories = (
        Category.query.filter_by(user_id=current_user.id, kind="homework")
        .order_by(Category.name)
        .all()
    )
    return [(0, "Sin categoría")] + [(c.id, c.name) for c in categories]


@homeworks_bp.route("/")
@login_required
def list_homeworks():
    query = Homework.query.filter_by(user_id=current_user.id)

    status = request.args.get("status")
    if status in ("pending", "done"):
        query = query.filter_by(status=status)

    category_id = request.args.get("category_id", type=int)
    if category_id:
        query = query.filter_by(category_id=category_id)

    homeworks = query.order_by(Homework.due_date.asc()).all()
    categories = (
        Category.query.filter_by(user_id=current_user.id, kind="homework").order_by(Category.name).all()
    )
    return render_template("homeworks/list.html", homeworks=homeworks, categories=categories)


@homeworks_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_homework():
    form = HomeworkForm()
    form.category_id.choices = _category_choices()

    if form.validate_on_submit():
        homework = Homework(
            user_id=current_user.id,
            title=form.title.data,
            subject=form.subject.data,
            category_id=form.category_id.data or None,
            due_date=form.due_date.data,
            status=form.status.data,
        )
        db.session.add(homework)
        db.session.commit()
        flash("Tarea agregada con exito.", "success")
        return redirect(url_for("homeworks.list_homeworks"))

    return render_template("homeworks/form.html", form=form, title="Tarea Nueva")


@homeworks_bp.route("/<int:homework_id>/edit", methods=["GET", "POST"])
@login_required
def edit_homework(homework_id):
    homework = Homework.query.filter_by(id=homework_id, user_id=current_user.id).first_or_404()
    form = HomeworkForm(obj=homework)
    form.category_id.choices = _category_choices()

    if request.method == "GET":
        form.category_id.data = homework.category_id or 0

    if form.validate_on_submit():
        homework.title = form.title.data
        homework.subject = form.subject.data
        homework.category_id = form.category_id.data or None
        homework.due_date = form.due_date.data
        homework.status = form.status.data
        db.session.commit()
        flash("Tarea actualizada.", "success")
        return redirect(url_for("homeworks.list_homeworks"))

    return render_template("homeworks/form.html", form=form, title="Editar tarea")


@homeworks_bp.route("/<int:homework_id>/delete", methods=["POST"])
@login_required
def delete_homework(homework_id):
    homework = Homework.query.filter_by(id=homework_id, user_id=current_user.id).first_or_404()
    db.session.delete(homework)
    db.session.commit()
    flash("Tarea borrada.", "info")
    return redirect(url_for("homeworks.list_homeworks"))
