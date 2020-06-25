from .. import db,errors
from . import log_sysbp
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for,session
from app.forms import LoginForm,RegistrationForm,ResetPasswordRequestForm,ResetPasswordForm,EditProfileForm,ChangePWDForm,ViewUserForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user,logout_user,login_required
from ..models import User,Role,Department
from .email import send_password_reset_email
from datetime import datetime,timedelta
import re
from flask import current_app
from app.tables import UserResults

APP = current_app._get_current_object()

#fa_role = Role.query.filter_by(name="Faculty").first()
#ta_role = Role.query.filter_by(name="TA").first()
#admin_role = Role.query.filter_by(name="Admin").first()
#stud_role = Role.query.filter_by(name="Student").first()

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
	return response

@log_sysbp.route('/check_user_json',methods=['GET'])
def checklogjson():
	logrec = [user.to_json() for user in User.query.all()]
	response = { 'records': logrec }
	return jsonify(response)

@log_sysbp.route('/add_log_json',methods=['POST'])
def addlogjson():
	user = User.from_json(request.json)
	user.set_password(request.json.get('pass'))
	if user is None:
		return jsonify({ 'error' : 'bad info'})

	db.session.add(user)
	db.session.commit()
	return jsonify({ 'status' : 'success'})

@log_sysbp.route('/modify_log_json',methods=['POST'])
def modifylogjson():
	user = User.query.filter_by(username=request.json['old'].get('username')).first_or_404()
	if user is None:
		return jsonify({ 'error' : 'bad info'})

	user.username = request.json['new'].get('username') or user.username
	user.fname = request.json['new'].get('fname') or user.lname 
	user.lname = request.json['new'].get('lname') or user.lname 
	user.email = request.json['new'].get('email') or user.email

	db.session.commit()
	return jsonify({'status' : 'success'})

@log_sysbp.route('/delete_log_json',methods=['POST'])
def dellogjson():
	user = User.query.filter_by(username=request.get_data('username')).first_or_404()
	if user is None:
		return jsonify({ 'error' : 'bad info'})
	db.session.delete(user)
	db.session.commit()
	return jsonify({ 'status' : 'success'})
