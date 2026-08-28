from flask import Blueprint

homeworks_bp = Blueprint("homeworks", __name__)

from app.homeworks import routes  # noqa: E402,F401
