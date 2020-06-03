from flask import Blueprint

dept_sysbp = Blueprint('dept_sysbp',__name__,template_folder = "../templates/")

from . import routes