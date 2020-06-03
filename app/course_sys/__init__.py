from flask import Blueprint

course_sysbp = Blueprint('course_sysbp',__name__,template_folder = "../templates/")

from . import routes