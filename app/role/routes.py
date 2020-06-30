from . import role_sysbp
from flask import jsonify,current_app
from ..models import Role,Permission
from app.log_sys.routes import token_required

APP = current_app._get_current_object()

@role_sysbp.after_request
def after_request(response):									#security
	response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-XSS-Protection'] = '1; mode=block'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
	response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
	return response

@role_sysbp.route('/check_role_json',methods=['GET','POST'])
@token_required(Permission.READ)
def checkrolejson():
	roles = [role.to_json() for role in Role.query.all()]
	response = { 'records': roles }
	return jsonify(response)