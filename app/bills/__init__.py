from flask import Blueprint

bills_bp = Blueprint("bills", __name__)

from app.bills import routes  # noqa: E402,F401
