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
'''
def token_required(f):
	@wraps(f)
	def _verify(*args, **kwargs):
		auth_headers = request.headers.get('Authorization', '').split()

		invalid_msg = {
			'message': 'Invalid token. Registeration and / or authentication required',
			'authenticated': False
		}
		expired_msg = {
			'message': 'Expired token. Reauthentication required.',
			'authenticated': False
		}

		if len(auth_headers) != 2:
			return jsonify(invalid_msg), 401

		try:
			token = auth_headers[1]
			data = jwt.decode(token, current_app.config['SECRET_KEY'])
			user = User.query.filter_by(username=data['sub']).first()
			if not user:
				raise RuntimeError('User not found')
			return f(user, *args, **kwargs)
		except jwt.ExpiredSignatureError:
			return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
		except (jwt.InvalidTokenError, Exception) as e:
			print(e)
			return jsonify(invalid_msg), 401

	return _verify

@log_sysbp.route('/login/', methods=('POST',))
def login():
	data = request.json
	user = User.authenticate(data.get('username'),data.get('email'),data.get('password'))

	if not user:
		return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

	token = jwt.encode({
		'sub': user.username,
		'iat':datetime.utcnow(),
		'exp': datetime.utcnow() + timedelta(minutes=30)},
		current_app.config['SECRET_KEY'])
	return jsonify({ 'token': token.decode('UTF-8') })
'''
@log_sysbp.before_request
def make_session_permanent():
	session.permanent = True
	log_sysbp.permanent_session_lifetime = timedelta(minutes=30)		#idle timeout for user session

@log_sysbp.after_request
def after_request(response):									#security
	response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-XSS-Protection'] = '1; mode=block'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response

@log_sysbp.route('/check_user_json',methods=['GET'])
#@token_required
def checklogjson():
	logrec = [user.to_json() for user in User.query.all()]
	response = { 'records': logrec }
	return jsonify(response)

@log_sysbp.route('/add_log_json',methods=['POST'])
#@token_required
def addlogjson():
	if not request.json:
		return jsonify({ 'status' : 'bad info'})

	jsdat = request.json
	check_user = User.query.filter_by(username = jsdat.get('username')).all()

	if check_user:
		return jsonify({ 'status' : 'User already in database'})

	if jsdat.get('username') == '' or jsdat.get('username') is None:
		return jsonify({ 'status' : 'empty userid'})
	
	if jsdat.get('fname') == '' or jsdat.get('fname') is None:
		return jsonify({ 'status' : 'empty first name'})

	if jsdat.get('lname') == '' or jsdat.get('lname') is None:
		return jsonify({ 'status' : 'empty last name'})

	if jsdat.get('email') == '' or jsdat.get('email') is None or check(jsdat.get('email')) is False:
		return jsonify({ 'status' : 'email empty or bad email format'})

	if jsdat.get('rolec') == '' or jsdat.get('rolec') is None:
		return jsonify({ 'status' : 'role info not given'})

	check_role = Role.query.filter_by(ID=jsdat.get('rolec')).first()
	if not check_role:
		return jsonify({ 'status' : 'not valid role'})

	if jsdat.get('rolec') != admin_role.ID:
		if jsdat.get('deptc') == '' or jsdat.get('deptc') is None:
			return jsonify({ 'status' : 'need to assign department to a non-admin'})

		check_dept = Department.query.filter_by(ID=jsdat.get('deptc')).first()
		if not check_dept:
			return jsonify({ 'status' : 'invalid department'})

	if jsdat.get('pass') !=  jsdat.get('confirmpass') or ( jsdat.get('pass') ==  jsdat.get('confirmpass') and (jsdat.get('pass') == '' or jsdat.get('pass') is None )):
		return jsonify({ 'status' : 'password not match'})

	user = User.from_json(jsdat)
	user.set_password(jsdat.get('pass'))
	if user is None:
		return jsonify({ 'status' : 'can\'t create user'})

	try:
		db.session.add(user)
		db.session.commit()
		return jsonify({ 'status' : 'User add success'})
	except:
		return jsonify({ 'status' : 'User add fail'})

@log_sysbp.route('/modify_log_json',methods=['POST'])
#@token_required
def modifylogjson():
	oldjs = request.json['old']
	newjs = request.json['new']
	user = User.query.filter_by(username=oldjs.get('username')).first_or_404()

	if not user:
		return jsonify({ 'status' : 'bad info'})

	if newjs.get('username') == '' or newjs.get('username') is None:
		return jsonify({ 'status' : 'bad info'})

	check_user = User.query.filter_by(username=newjs.get('username')).first_or_404()

	if check_user:
		return jsonify({ 'status' : 'User already in database'})
	
	if newjs.get('fname') == '' or newjs.get('fname') is None:
		return jsonify({ 'status' : 'bad info'})

	if newjs.get('lname') == '' or newjs.get('lname') is None:
		return jsonify({ 'status' : 'bad info'})

	if newjs.get('email') == '' or newjs.get('email') is None or check(newjs.get('email')) is False:
		return jsonify({ 'status' : 'bad info'})

	check_user = User.query.filter_by(email=newjs.get('email')).first_or_404()

	if check_user:
		return jsonify({ 'status' : 'User already in database'})

	if newjs.get('rolec') == '' or newjs.get('rolec') is None:
		return jsonify({ 'status' : 'bad info'})

	check_role = Role.query.filter_by(ID=newjs.get('rolec')).first()
	if not check_role:
		return jsonify({ 'status' : 'bad info'})

	if newjs.get('rolec') != admin_role.ID:
		if newjs.get('deptc') == '' or newjs.get('deptc') is None:
			return jsonify({ 'status' : 'bad info'})

		check_dept = Department.query.filter_by(ID=newjs.get('deptc')).first()
		if not check_dept:
			return jsonify({ 'status' : 'bad info'})

	try:
		user.username = newjs.get('username') or user.username
		user.fname = newjs.get('fname') or user.lname 
		user.lname = newjs.get('lname') or user.lname 
		user.email = newjs.get('email') or user.email
		user.role_id = newjs.get('rolec') or user.email
		user.dept = newjs.get('deptc') or user.email

		db.session.commit()
		return jsonify({'status' : 'modify success'})
	except:
		return jsonify({'status' : 'modify fail'})

@log_sysbp.route('/delete_log_json',methods=['POST'])
#@token_required
def dellogjson():
	user = User.query.filter_by(username=request.get_data('username')).first_or_404()
	if not user:
		return jsonify({ 'status' : 'No such user in first place'})
	try:
		db.session.delete(user)
		db.session.commit()
		return jsonify({ 'status' : 'User deletion success'})
	except:
		return jsonify({ 'status' : 'User deletion failed'})
