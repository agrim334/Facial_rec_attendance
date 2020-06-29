from flask import Blueprint

log_sysbp = Blueprint('log_sysbp',__name__,template_folder = "email")

from . import routes,email