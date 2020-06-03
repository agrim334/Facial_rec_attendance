from flask import Blueprint

log_sysbp = Blueprint('log_sysbp',__name__,template_folder = "templates")

from . import routes,email