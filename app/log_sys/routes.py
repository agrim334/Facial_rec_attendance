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

fa_role = Role.query.filter_by(role="Faculty").first()
ta_role = Role.query.filter_by(role="TA").first()
admin_role = Role.query.filter_by(role="Admin").first()
stud_role = Role.query.filter_by(role="Student").first()

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

@log_sysbp.route('/check_user_json',methods=['GET','POST'])
def checklogjson():
	logrec = [user.to_json() for user in User.query.all()]
	response = { 'records': logrec }
	print(response)
	return jsonify(response)

@log_sysbp.route('/mark_log_json',methods=['POST'])
def marklogjson():
	user = User.from_json(request.json)
	db.session.add(user)
	db.session.commit()
	return jsonify(user.to_json())

@log_sysbp.route('/modify_log_json',methods=['POST'])
def modifylogjson():
	user = User.from_json(request.json)
	db.session.add(user)
	db.session.commit()
	return jsonify(user.to_json())

@log_sysbp.route('/delete_log_json',methods=['POST'])
def dellogjson():
	user = User.from_json(request.json)
	db.session.add(user)
	db.session.commit()
	return jsonify(user.to_json())

@log_sysbp.route('/')
@login_required
def home():													#home page url
	return render_template('home.html', title='Home',user = user,faculty = fa_role.role_id,ta = ta_role.role_id,admin = admin_role.role_id,stud = stud_role.role_id)

@log_sysbp.route('/user/<username>')
@login_required
def user(username):
	if current_user.is_authenticated:
		user = User.query.filter_by(username=username).first_or_404()
		if user:
			if current_user.username == username:
				return render_template('user.html', user=user)
			else:
				flash('Not allowed')
				return redirect('.home')
	else:
		flash('login please')
		return redirect(url_for('.login'))

@log_sysbp.route('/login',methods={'GET','POST'})
def login():										#login page url
	if current_user.is_authenticated:
		return redirect(url_for('.home'))
	form = LoginForm()
	form.role.choices = [(int(role.role_id),role.role) for role in Role.query.all()]
	print(type(form.role.data))
		
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data,role_id=form.role.data).first()  #check if credentials valid
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			APP.logger.error('login failed for user ' + user.username )
			return redirect(url_for('.login'))
		else:
			login_user(user, remember=form.remember_me.data)
			APP.logger.error('Successfull login for user ' + user.username )
			next_page = request.args.get('next')
		
			if not next_page or url_parse(next_page).netloc != '':							#redirect to home
				next_page = url_for('.home',user = user)

			return redirect(next_page)

	return render_template('login.html', title='Sign In', form=form)

@log_sysbp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	if current_user.is_authenticated:
		form = EditProfileForm(current_user)
		if form.validate_on_submit():
			current_user.email = form.email.data
			current_user.fname = form.fname.data
			current_user.lname = form.lname.data
			db.session.commit()
			flash('Your changes have been saved.')
			return redirect(url_for('.edit_profile'))

		elif request.method == 'GET':
			form.email.data = current_user.email
			form.fname.data = current_user.fname
			form.lname.data = current_user.lname
		return render_template('form_entry.html', title='Edit Profile',form=form)	
	else:
		flash('login please')
		return redirect(url_for('.login'))

@log_sysbp.route('/change_password', methods=['GET','POST'])
@login_required
def change_password():
	if current_user.is_authenticated:
		form = ChangePWDForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				if current_user.check_password(form.currentpassword.data):
					current_user.set_password(form.newpassword.data)
					db.session.commit()
					flash('Your changes have been saved.')
					return redirect(url_for('.home'))
				else :
					flash('Old password incorrect')
					return redirect(url_for('change_password'))
		return render_template('form_entry.html', title='Change Password',form=form)	
	else:
		flash('login please')
		return redirect(url_for('.login'))

@log_sysbp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data) 
		if user:
			send_password_reset_email(user,user.email)
			flash('Check your email for the instructions to reset your password')
			return redirect(url_for('.login'))
		else:
			flash('Error could not send email as user not registered or no email address set for this user')
			return redirect(url_for('.reset_password_request'))

	return render_template('form_entry.html',title='Reset Password', form=form)

@log_sysbp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('.home'))
	user = User.verify_reset_password_token(token)
	if not user:
		flash('Time expired.')
		return redirect(url_for('.home'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset.')
		return redirect(url_for('.login'))
	return render_template('form_entry.html',title='Reset Password', form=form)

@log_sysbp.route('/logout')
def logout():
	if not current_user.is_anonymous:
		logout_user()
		flash('You have logged out')
	else:
		flash('Error.Not logged in')
	return redirect(url_for('.login'))

@log_sysbp.route('/add_users',methods=['GET','POST'])
@login_required
def add_users():
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:
			form = RegistrationForm()
			form.log.choices = [(int(log.log_ID), log.log_name) for log in Department.query.all()]
			form.role.choices = [(int(role.role_id), role.role) for role in Role.query.all()]
			if form.validate_on_submit():
				check_user = User.query.filter_by(username = form.username.data)
				if user and user.count() != 0:
					flash('User has been added already in database')
					return redirect(url_for('.add_users'))
				else:
					user = User(username=form.username.data, fname=form.fname.data, lname=form.lname.data,email=form.email.data,role_id=form.role.data,log=int(form.log.data))
					user.set_password(form.password.data)
					db.session.add(user)
					db.session.commit()
					db.session.close()
					flash('User has been added')
					return redirect(url_for('add_users'))
			return render_template('form_entry.html', title='Register new user', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('.home'))
	else:
		flash('Login please!!')
		return redirect(url_for('.login'))

@log_sysbp.route('/view_users',methods=['GET','POST'])
@login_required
def view_users():
	if current_user.is_authenticated:
		table = []
		title = "User"
		form = ViewUserForm()
		if form.validate_on_submit():
			if current_user.role_id == admin_role.role_id:
				criteria = form.criteria.data			
				criteria = int(criteria)
				if criteria == 1:
					value = form.match.data
					check_log = Department.query.filter_by(value)
					if check_log:
						user = db.session.query(User,Department).filter(User.log == value).all()
						if user:
							table = UserResults(user)
							table.border = True
						else:
							flash("No users under department " + value + ".Ensure that the department exists")
							return redirect(url_for('view_users'))
					else:
						flash("No users under department " + value + ".Ensure that the department exists")
						return redirect(url_for('view_users'))

				elif criteria == 2:
					value = form.match.data
					check_role = Role.query.filter_by(role=value).first().role_id
					if check_role:
						user = User.query.filter_by(role_id=value)
						if user:
							table = UserResults(user)
							table.border = True
						else:
							flash("No users under role " + value +". Ensure role exists")
							return redirect(url_for('view_users'))
					else:
						flash("No users under role " + value +". Ensure role exists")
						return redirect(url_for('view_users'))

				elif criteria == 3:
					value = form.match.data
					user = User.query.filter_by(username=value)
					if user:
						table = UserResults(user)
						table.border = True
					else:
						flash("No Users Found with ID " + value)
						return redirect(url_for('view_users'))

				elif criteria == 4:
					user = User.query.all()
					if user and len(user) != 0:
						table = UserResults(user)
						table.border = True
					else:
						flash("No Users Found")
						return redirect(url_for('view_users'))
			else:
				flash('Not allowed')
				return redirect(url_for('home'))

		return render_template('view.html',title=title,form=form,table=table)
	else:
		flash('Login please')
		return redirect(url_for('login'))

@log_sysbp.route('/upd_users',methods=['GET','POST'])
@login_required
def upd_users():
	if current_user.is_authenticated:
		table = []
		title = "User"
		form = ViewUserForm()
		if form.validate_on_submit():
			if current_user.role_id == admin_role.role_id:
				criteria = form.criteria.data			
				criteria = int(criteria)
				if criteria == 1:
					value = form.match.data
					check_log = Department.query.filter_by(value)
					if check_log:
						user = db.session.query(User,Department).filter(User.log == value).all()
						if user:
							columns = User.__table__.columns.keys()
							columns.remove('password_hash')
							for r in user:
								records.append(r)
						else:
							flash("No users under department " + value + ".Ensure that the department exists")
							return redirect(url_for('users'))
					else:
						flash("No users under department " + value + ".Ensure that the department exists")
						return redirect(url_for('users'))
				elif criteria == 2:
					value = form.match.data
					check_role = Role.query.filter_by(role=value).first().role_id
					if check_role:
						user = User.query.filter_by(role_id=value)
						if user:
							columns = User.__table__.columns.keys()
							columns.remove('password_hash')
							for r in user:
								records.append(r)
						else:
							flash("No users under role " + value +". Ensure role exists")
							return redirect(url_for('users'))
					else:
						flash("No users under role " + value +". Ensure role exists")
						return redirect(url_for('users'))

				elif criteria == 3:
					value = form.match.data
					user = User.query.filter_by(username=value)
					if user:
						columns = User.__table__.columns.keys()
						columns.remove('password_hash')
						for r in user:
							records.append(r)
					else:
						flash("No Users Found with ID " + value)
						return redirect(url_for('users'))
				elif criteria == 4:
					user = User.query.all()
					print(user)
					if user and len(user) != 0:
						columns = User.__table__.columns.keys()
						columns.remove('password_hash')
						for r in user:
							records.append(r)
					else:
						flash("No Users Found")
						return redirect(url_for('users'))
			else:
				flash('Not allowed')
				return redirect(url_for('home'))

		return render_template('view.html',title=title,form=form,table=table)
	else:
		flash('Login please')
		return redirect(url_for('login'))


@log_sysbp.route('/del_users',methods=['GET','POST'])
@login_required
def del_users():
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:
			form = RegistrationForm()
			form.log.choices = [(int(log.log_ID), log.log_name) for log in Department.query.all()]
			form.role.choices = [(int(role.role_id), role.role) for role in Role.query.all()]
			if form.validate_on_submit():
				check_user = User.query.filter_by(username = form.username.data)
				if user and user.count() != 0:
					flash('User has been added already in database')
					return redirect(url_for('del_users'))
				else:
					user = User(username=form.username.data, fname=form.fname.data, lname=form.lname.data,email=form.email.data,role_id=form.role.data,log=int(form.log.data))
					user.set_password(form.password.data)
					db.session.add(user)
					db.session.commit()
					db.session.close()
					flash('User has been added')
					return redirect(url_for('del_users'))
			return render_template('form_entry.html', title='Register new user', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('home'))
	else:
		flash('Login please!!')
		return redirect(url_for('login'))
