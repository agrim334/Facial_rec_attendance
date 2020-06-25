from flask import Blueprint

role_sysbp = Blueprint('role_sysbp',__name__,template_folder = "templates")

from . import routes