from flask import Blueprint

attd_sysbp = Blueprint('attd_sysbp',__name__,template_folder = "../templates/")

from . import routes