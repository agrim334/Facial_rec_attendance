from .. import db,errors
from . import mapbp
from app.log_sys import log_sysbp
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for,session
from app.forms import CourseUserForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user,logout_user,login_required
from ..models import User,Role,Department,Course,stud_courses,ta_courses,prof_courses
from datetime import datetime,timedelta
import re
from app.tables import MapResults

fa_role = Role.query.filter_by(role="Faculty").first()
ta_role = Role.query.filter_by(role="TA").first()
admin_role = Role.query.filter_by(role="Admin").first()
stud_role = Role.query.filter_by(role="Student").first()

@mapbp.before_request
def make_session_permanent():
	session.permanent = True
	mapbp.permanent_session_lifetime = timedelta(minutes=10)		#idle timeout for user session

@mapbp.after_request
def after_request(response):									#security
	response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-XSS-Protection'] = '1; mode=block'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response

@mapbp.route('/add_course_user',methods=['GET','POST'])
@login_required
def add_course_user():														#map course to user url
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:						
			form = CourseUserForm()
			if form.validate_on_submit():
				#role_id = Role.query.filter_by(role = form.role.data).first().role_id
				role_id = 1
				course = Course.query.filter(Course.Course_ID == form.CID.data) 
				if not course:
					flash('This course was not found in Database.Please add this course to database and then try or enter correct course id.')
					return redirect(url_for('.course_user_add'))
				user = User.query.filter_by(username=form.user.data,role_id=form.role.data).first()
				if not user:
					flash('No such TA or Faculty found')
					return redirect(url_for('.add_course_user'))
				if role_id == fa_role.role_id:
					check_map = db.session.query(prof_courses).filter_by(prof_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.add_course_user'))
					statement = prof_courses.insert().values(prof_id=form.user.data,course_id=form.CID.data)
				elif role_id == ta_role.role_id:
					check_map = db.session.query(ta_courses).filter_by(ta_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.add_course_user'))
					statement = ta_courses.insert().values(ta_id=form.user.data,course_id=form.CID.data)					#TA prof mapped to course
				elif role_id == stud_role.role_id:
					check_map = db.session.query(stud_courses).filter_by(stud_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.add_course_user'))
					statement = stud_courses.insert().values(stud_id=form.user.data,course_id=form.CID.data)			#for students save mapping + image corresponding to course
					known_dir = "/home/agrim/Downloads/known/" + str(form.CID.data) +"/"								#set known dir to your required location
					if not os.path.exists(known_dir):
						os.makedirs(known_dir)
					file = request.files.getlist("photo")
					for f in file:
						filename = secure_filename(f.filename)
						f.save(os.path.join(known_dir, filename))
						filename, file_extension = os.path.splitext(os.path.join(known_dir, filename))		#save images renaming them appropriately
						nf = form.user.data + file_extension
						os.rename(os.path.join(known_dir, filename),os.path.join(known_dir, nf))
				else:
					flash("Not allowed for this role_id")
					return redirect(url_for('.add_course_user'))
				db.session.execute(statement)
				db.session.commit()
				db.session.close()
				flash('Mapping has been added')
				return redirect(url_for('.add_course_user'))
			return render_template('form_entry.html', title='Course_user', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('log_sysbp.home'))
	else:
		flash('Login please!!')
		return redirect(url_for('log_sysbp.login'))

@mapbp.route('/view_course_user',methods=['GET','POST'])
@login_required
def view_course_user():														#map course to user url
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:						
			form = CourseUserForm()
			if form.validate_on_submit():
				#role_id = Role.query.filter_by(role = form.role.data).first().role_id
				role_id = 1
				course = Course.query.filter(Course.Course_ID == form.CID.data) 
				if not course:
					flash('This course was not found in Database.Please add this course to database and then try or enter correct course id.')
					return redirect(url_for('.view_course_user'))
				user = User.query.filter_by(username=form.user.data,role_id=form.role.data).first()
				if not user:
					flash('No such TA or Faculty found')
					return redirect(url_for('.view_course_user'))
				if role_id == fa_role.role_id:
					check_map = db.session.query(prof_courses).filter_by(prof_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.view_course_user'))
					statement = prof_courses.insert().values(prof_id=form.user.data,course_id=form.CID.data)
				elif role_id == ta_role.role_id:
					check_map = db.session.query(ta_courses).filter_by(ta_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.view_course_user'))
					statement = ta_courses.insert().values(ta_id=form.user.data,course_id=form.CID.data)					#TA prof mapped to course
				elif role_id == stud_role.role_id:
					check_map = db.session.query(stud_courses).filter_by(stud_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.view_course_user'))
					statement = stud_courses.insert().values(stud_id=form.user.data,course_id=form.CID.data)			#for students save mapping + image corresponding to course
					known_dir = "/home/agrim/Downloads/known/" + str(form.CID.data) +"/"								#set known dir to your required location
					if not os.path.exists(known_dir):
						os.makedirs(known_dir)
					file = request.files.getlist("photo")
					for f in file:
						filename = secure_filename(f.filename)
						f.save(os.path.join(known_dir, filename))
						filename, file_extension = os.path.splitext(os.path.join(known_dir, filename))		#save images renaming them appropriately
						nf = form.user.data + file_extension
						os.rename(os.path.join(known_dir, filename),os.path.join(known_dir, nf))
				else:
					flash("Not allowed for this role_id")
					return redirect(url_for('.view_course_user'))
				db.session.execute(statement)
				db.session.commit()
				db.session.close()
				flash('Mapping has been added')
				return redirect(url_for('.view_course_user'))
			return render_template('view.html', title='Course_user', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('log_sysbp.home'))
	else:
		flash('Login please!!')
		return redirect(url_for('log_sysbp.login'))

@mapbp.route('/upd_course_user',methods=['GET','POST'])
@login_required
def upd_course_user():														#map course to user url
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:						
			form = CourseUserForm()
			if form.validate_on_submit():
				#role_id = Role.query.filter_by(role = form.role.data).first().role_id
				role_id = 1
				course = Course.query.filter(Course.Course_ID == form.CID.data) 
				if not course:
					flash('This course was not found in Database.Please add this course to database and then try or enter correct course id.')
					return redirect(url_for('.upd_course_user'))
				user = User.query.filter_by(username=form.user.data,role_id=form.role.data).first()
				if not user:
					flash('No such TA or Faculty found')
					return redirect(url_for('.upd_course_user'))
				if role_id == fa_role.role_id:
					check_map = db.session.query(prof_courses).filter_by(prof_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.upd_course_user'))
					statement = prof_courses.insert().values(prof_id=form.user.data,course_id=form.CID.data)
				elif role_id == ta_role.role_id:
					check_map = db.session.query(ta_courses).filter_by(ta_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.upd_course_user'))
					statement = ta_courses.insert().values(ta_id=form.user.data,course_id=form.CID.data)					#TA prof mapped to course
				elif role_id == stud_role.role_id:
					check_map = db.session.query(stud_courses).filter_by(stud_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.upd_course_user'))
					statement = stud_courses.insert().values(stud_id=form.user.data,course_id=form.CID.data)			#for students save mapping + image corresponding to course
					known_dir = "/home/agrim/Downloads/known/" + str(form.CID.data) +"/"								#set known dir to your required location
					if not os.path.exists(known_dir):
						os.makedirs(known_dir)
					file = request.files.getlist("photo")
					for f in file:
						filename = secure_filename(f.filename)
						f.save(os.path.join(known_dir, filename))
						ofilename, ofile_extension = os.path.splitext(os.path.join(known_dir, filename))		#save images renaming them appropriately
						nf = form.user.data + ofile_extension
						os.rename(os.path.join(known_dir, filename),os.path.join(known_dir, nf))
				else:
					flash("Not allowed for this role_id")
					return redirect(url_for('.upd_course_user'))
				db.session.execute(statement)
				db.session.commit()
				db.session.close()
				flash('Mapping has been added')
				return redirect(url_for('.upd_course_user'))
			return render_template('form_entry.html', title='Course_user', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('log_sysbp.home'))
	else:
		flash('Login please!!')
		return redirect(url_for('log_sysbp.login'))

@mapbp.route('/del_course_user',methods=['GET','POST'])
@login_required
def del_course_user():														#map course to user url
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:						
			form = CourseUserForm()
			if form.validate_on_submit():
				#role_id = Role.query.filter_by(role = form.role.data).first().role_id
				role_id = 1
				course = Course.query.filter(Course.Course_ID == form.CID.data) 
				if not course:
					flash('This course was not found in Database.Please add this course to database and then try or enter correct course id.')
					return redirect(url_for('.del_course_user'))
				user = User.query.filter_by(username=form.user.data,role_id=form.role.data).first()
				if not user:
					flash('No such TA or Faculty found')
					return redirect(url_for('.del_course_user'))
				if role_id == fa_role.role_id:
					check_map = db.session.query(prof_courses).filter_by(prof_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.del_course_user'))
					statement = prof_courses.insert().values(prof_id=form.user.data,course_id=form.CID.data)
				elif role_id == ta_role.role_id:
					check_map = db.session.query(ta_courses).filter_by(ta_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.del_course_user'))
					statement = ta_courses.insert().values(ta_id=form.user.data,course_id=form.CID.data)					#TA prof mapped to course
				elif role_id == stud_role.role_id:
					check_map = db.session.query(stud_courses).filter_by(stud_id=form.user.data,course_id = form.CID.data)
					if check_map and check_map.count() != 0:
						flash("Mapping already in database")
						return redirect(url_for('.del_course_user'))
					statement = stud_courses.insert().values(stud_id=form.user.data,course_id=form.CID.data)			#for students save mapping + image corresponding to course
					known_dir = "/home/agrim/Downloads/known/" + str(form.CID.data) +"/"								#set known dir to your required location
					if not os.path.exists(known_dir):
						os.makedirs(known_dir)
					file = request.files.getlist("photo")
					for f in file:
						filename = secure_filename(f.filename)
						f.save(os.path.join(known_dir, filename))
						ofilename, ofile_extension = os.path.splitext(os.path.join(known_dir, filename))		#save images renaming them appropriately
						nf = form.user.data + ofile_extension
						os.rename(os.path.join(known_dir, filename),os.path.join(known_dir, nf))
				else:
					flash("Not allowed for this role_id")
					return redirect(url_for('.del_course_user'))
				db.session.execute(statement)
				db.session.commit()
				db.session.close()
				flash('Mapping has been added')
				return redirect(url_for('.del_course_user'))
			return render_template('form_entry.html', title='Course_user', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('log_sysbp.home'))
	else:
		flash('Login please!!')
		return redirect(url_for('log_sysbp.login'))
