from .. import db,errors
from . import course_sysbp
from app.log_sys import log_sysbp
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for,session
from app.forms import CourseForm,ViewCourseForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user,logout_user,login_required
from ..models import User,Role,Course,Department
from datetime import datetime,timedelta
from app.tables import CourseResults
import re

fa_role = Role.query.filter_by(role="Faculty").first()
stud_role = Role.query.filter_by(role="Student").first()
ta_role = Role.query.filter_by(role="TA").first()
admin_role = Role.query.filter_by(role="Admin").first()

@course_sysbp.before_request
def make_session_permanent():
	session.permanent = True
	course_sysbp.permanent_session_lifetime = timedelta(minutes=10)		#idle timeout for user session

@course_sysbp.after_request
def after_request(response):									#security
	response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-XSS-Protection'] = '1; mode=block'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response

@course_sysbp.route('/add_courses',methods=['GET','POST'])
@login_required
def add_courses():
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:
			form = CourseForm()
			if form.validate_on_submit():
				check_course = Course.query.filter_by(Course_ID = form.CID.data)
				if check_course and check_course.count() != 0:
					flash('Course has been added already in database')
					return redirect(url_for('.add_courses'))					
				else:
					course = Course(Course_ID=form.CID.data, Course_name=form.Cname.data)       #add new course and correspondingly directory for students attending the course
					known_dir = "/home/agrim/Downloads/known/" + str(form.CID.data) +"/"
					if not os.path.exists(known_dir):
						os.makedirs(known_dir)
					db.session.add(course)
					db.session.commit()
					db.session.close()
					flash('Course has been added')
					return redirect(url_for('.add_courses'))
			return render_template('form_entry.html', title='Add Course', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('log_sysbp.home'))
	else:
		flash('Login please!!')
		return redirect(url_for('log_sysbp.login'))

@course_sysbp.route('/view_courses',methods=['GET','POST'])
@login_required
def view_courses():
	if current_user.is_authenticated:
		form = ViewCourseForm()
		table = []
		if form.validate_on_submit():
			criteria = form.criteria.data
			criteria = int(criteria)
			courses = []
			if criteria == 1:
				value = form.match.data
				check_dept = Department.query.filter_by(value)
				if check_dept:
					courses = db.session.query(Course,Department).filter(Course.dept_id == value & Course.dept_id == Department.Dept_ID).all()				
				else:
					flash("No courses under department " + value + ".Ensure that the department exists")
					return redirect(url_for('.view_courses'))
			elif criteria == 2:
				value = form.match.data
				courses = Course.query.filter_by(Course_ID=value)

			elif criteria == 3:
				courses = Course.query.all()

			if courses:
				table = CourseResults(courses)
				table.border = True
			else:
				flash("No Courses Found with given criteria")
				return redirect(url_for('.view_courses'))
		return render_template('view.html',title="Courses",form=form,table=table)

	else:
		flash('Login please')
		return redirect(url_for('log_sysbp.login'))

@course_sysbp.route('/upd_courses',methods=['GET','POST'])
@login_required
def upd_courses():
	if current_user.is_authenticated:
		table = []
		form = ViewCourseForm()
		if form.validate_on_submit():
			criteria = form.criteria.data
			criteria = int(criteria)
			courses = []
			if criteria == 1:
				value = form.match.data
				check_dept = Department.query.filter_by(value)
				if check_dept:
					courses = db.session.query(Course,Department).filter(Course.dept_id == value & Course.dept_id == Department.Dept_ID).all()				
				else:
					flash("No courses under department " + value + ".Ensure that the department exists")
					return redirect(url_for('.upd_courses'))
			elif criteria == 2:
				value = form.match.data
				courses = Course.query.filter_by(Course_ID=value)

			elif criteria == 3:
				courses = Course.query.all()

			if courses:
				columns = Course.__table__.columns.keys()
				for r in courses:
					records.append(r)
			else:
				flash("No Courses Found with given criteria")
				return redirect(url_for('.upd_courses'))
		return render_template('view.html',title="Courses",form=form,table=table)

	else:
		flash('Login please')
		return redirect(url_for('log_sysbp.login'))

@course_sysbp.route('/del_courses',methods=['GET','POST'])
@login_required
def del_courses():
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:
			form = CourseForm()
			if form.validate_on_submit():
				check_course = Course.query.filter_by(Course_ID = form.CID.data)
				if check_course and check_course.count() != 0:
					flash('Course has been added already in database')
					return redirect(url_for('.del_courses'))					
				else:
					course = Course(Course_ID=form.CID.data, Course_name=form.Cname.data)       #add new course and correspondingly directory for students attending the course
					known_dir = "/home/agrim/Downloads/known/" + str(form.CID.data) +"/"
					if not os.path.exists(known_dir):
						os.makedirs(known_dir)
					db.session.add(course)
					db.session.commit()
					db.session.close()
					flash('Course has been added')
					return redirect(url_for('.del_courses'))
			return render_template('form_entry.html', title='Add Course', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('log_sysbp.home'))
	else:
		flash('Login please!!')
		return redirect(url_for('log_sysbp.login'))
