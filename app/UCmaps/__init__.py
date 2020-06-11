from flask import Blueprint

mapbp = Blueprint('mapbp',__name__,template_folder = "../templates/")

from . import routes