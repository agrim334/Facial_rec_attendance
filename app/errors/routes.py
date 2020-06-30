from . import errorsbp
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for,session
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user,logout_user,login_required

@log_sysbp.before_request
def make_session_permanent():
	session.permanent = True
	log_sysbp.permanent_session_lifetime = timedelta(minutes=10)		#idle timeout for user session

@log_sysbp.after_request
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

@errorsbp.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@errorsbp.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

@errorsbp.errorhandler(Exception)
def unhandled_exception(e):
	db.session.rollback()
    APP.logger.error('Unhandled Exception: %s', (e))
    return render_template('500.html'), 500

@errorsbp.app_errorhandler(404)
def page_not_found(e):
	if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'not found'})
		response.status_code = 404
		return response
	return render_template('404.html'), 404

def forbidden(message):
	response = jsonify({'error': 'forbidden', 'message': message})
	response.status_code = 403
	return response