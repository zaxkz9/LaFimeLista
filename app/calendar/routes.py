import calendar as cal
from datetime import date

from flask import render_template, request
from flask_login import current_user, login_required

from app.calendar import calendar_bp
from app.models.bill import Bill
from app.models.homework import Homework

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


@calendar_bp.route("/")
@login_required
def calendar_calendar():
    today = date.today()
    year = request.args.get("year", type=int, default=today.year)
    month = request.args.get("month", type=int, default=today.month)

    # Si el mes se sale de 1-12 (al navegar con las flechas), lo pasamos al año de al lado
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    # Junta, por día del mes que se está mostrando, las tareas y recibos del usuario
    items_by_day = {}
    homeworks = Homework.query.filter_by(user_id=current_user.id).all()
    bills = Bill.query.filter_by(user_id=current_user.id).all()

    for h in homeworks:
        if h.due_date.year == year and h.due_date.month == month:
            items_by_day.setdefault(h.due_date.day, []).append(("tarea", "Tarea", h.title))
    for b in bills:
        if b.due_date.year == year and b.due_date.month == month:
            items_by_day.setdefault(b.due_date.day, []).append(("recibo", "Recibo", b.name))

    cal.setfirstweekday(cal.MONDAY)
    weeks = cal.monthcalendar(year, month)  # lista de semanas; 0 = día fuera del mes

    return render_template(
        "calendar/calendar.html",
        weeks=weeks,
        items_by_day=items_by_day,
        month_name=MESES[month - 1],
        year=year,
        month=month,
        dias_semana=DIAS_SEMANA,
        prev_month=month - 1,
        next_month=month + 1,
        today=today,
    )
