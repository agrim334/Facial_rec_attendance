from .. import db,errors
from . import errrorsbp
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for,session
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user,logout_user,login_required
from ..models import User,Role
from .email import send_password_reset_email
from datetime import datetime,timedelta
import re

fa_role = Role.query.filter_by(role="Faculty").first()
ta_role = Role.query.filter_by(role="TA").first()
admin_role = Role.query.filter_by(role="Admin").first()
stud_role = Role.query.filter_by(role="Student").first()

@errors.before_request
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
	return response

@errors.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@errors.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

@errors.errorhandler(Exception)
def unhandled_exception(e):
    APP.logger.error('Unhandled Exception: %s', (e))
    return render_template('500.html'), 500
