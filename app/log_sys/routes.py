from .. import db,errors
from . import log_sysbp
from flask import Flask,jsonify,request,redirect,url_for,session,current_app
from app.forms import LoginForm,RegistrationForm,ResetPasswordRequestForm,ResetPasswordForm,EditProfileForm,ChangePWDForm,ViewUserForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user,logout_user,login_required
from ..models import User,Role,Department
from .email import send_password_reset_email
from datetime import datetime,timedelta
import jwt
import re

APP = current_app._get_current_object()

#fa_role = Role.query.filter_by(name="Faculty").first()
#ta_role = Role.query.filter_by(name="TA").first()
admin_role = Role.query.filter_by(name="Admin").first()
#stud_role = Role.query.filter_by(name="Student").first()

def check(email):
	regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	if(re.search(regex,email)):  
		return True		  
	return False

@log_sysbp.before_request
def make_session_permanent():
	session.permanent = True
	log_sysbp.permanent_session_lifetime = timedelta(minutes=20)		#idle timeout for user session

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
	jsdat = request.json
	check_user = User.query.filter_by(username = jsdat.get_data('username')).all()

	if check_user and check_user.count() != 0:
		return jsonify({ 'error' : 'User already in database'})

	if jsdat.get_data('username') == '' or jsdat.get_data('username') is None:
		return jsonify({ 'error' : 'bad info'})
	
	if jsdat.get_data('fname') == '' or jsdat.get_data('fname') is None:
		return jsonify({ 'error' : 'bad info'})

	if jsdat.get_data('lname') == '' or jsdat.get_data('lname') is None:
		return jsonify({ 'error' : 'bad info'})

	if jsdat.get_data('email') == '' or jsdat.get_data('email') is None or check(jsdat.get_data('email')) is False:
		return jsonify({ 'error' : 'bad info'})

	if jsdat.get_data('rolec') == '' or jsdat.get_data('rolec') is None:
		return jsonify({ 'error' : 'bad info'})

	if jsdat.get_data('rolec') != admin_role.ID and (jsdat.get_data('deptc') == '' or jsdat.get_data('deptc') is None):
		return jsonify({ 'error' : 'bad info'})

	if jsdat.get_data('pass') !=  jsdat.get_data('confirmpass') or ( jsdat.get_data('pass') ==  jsdat.get_data('confirmpass') and (jsdat.get_data('pass') == '' or jsdat.get_data('pass') is None )):
		return jsonify({ 'error' : 'bad info'})

	user = User.from_json(request.json)
	user.set_password(request.json.get('pass'))
	if user is None:
		return jsonify({ 'error' : 'bad info'})

	try:
		db.session.add(user)
		db.session.commit()
		return jsonify({ 'status' : 'User deletion success'})
	except:
		return jsonify({ 'status' : 'User deletion failed'})

@log_sysbp.route('/modify_log_json',methods=['POST'])
def modifylogjson():
	oldjs = request.json['old']
	newjs = request.json['new']
	user = User.query.filter_by(username=oldjs.get('username')).first_or_404()
	if user is None:
		return jsonify({ 'error' : 'bad info'})

	if newjs.get('username') == '' or newjs.get('username') is None:
		return jsonify({ 'error' : 'bad info'})

	check_user = User.query.filter_by(username=newjs.get('username')).first_or_404()

	if check_user:
		return jsonify({ 'error' : 'User already in database'})
	
	if newjs.get('fname') == '' or newjs.get('fname') is None:
		return jsonify({ 'error' : 'bad info'})

	if newjs.get('lname') == '' or newjs.get('lname') is None:
		return jsonify({ 'error' : 'bad info'})

	if newjs.get('email') == '' or newjs.get('email') is None or check(newjs.get('email')) is False:
		return jsonify({ 'error' : 'bad info'})

	check_user = User.query.filter_by(email=newjs.get('email')).first_or_404()

	if check_user:
		return jsonify({ 'error' : 'User already in database'})

	if newjs.get('rolec') == '' or newjs.get('rolec') is None:
		return jsonify({ 'error' : 'bad info'})

	if newjs.get('rolec') != admin_role.ID and (newjs.get('deptc') == '' or newjs.get('deptc') is None):
		return jsonify({ 'error' : 'bad info'})

	try:
		user.username = newjs.get('username') or user.username
		user.fname = newjs.get('fname') or user.lname 
		user.lname = newjs.get('lname') or user.lname 
		user.email = newjs.get('email') or user.email
		user.role_id = newjs.get('rolec') or user.email
		user.dept = newjs.get('deptc') or user.email

		db.session.commit()
		return jsonify({'status' : 'success'})
	except:
		return jsonify({'status' : 'fail'})

@log_sysbp.route('/delete_log_json',methods=['POST'])
def dellogjson():
	user = User.query.filter_by(username=request.get_data('username')).first_or_404()
	if user is None:
		return jsonify({ 'error' : 'No such user in first place'})
	try:
		db.session.delete(user)
		db.session.commit()
		return jsonify({ 'status' : 'User deletion success'})
	except:
		return jsonify({ 'status' : 'User deletion failed'})