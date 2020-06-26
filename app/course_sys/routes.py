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

#fa_role = Role.query.filter_by(name="Faculty").first()
#stud_role = Role.query.filter_by(name="Student").first()
#ta_role = Role.query.filter_by(name="TA").first()
#admin_role = Role.query.filter_by(name="Admin").first()

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

@course_sysbp.route('/check_course_json',methods=['GET','POST'])
def checkcoursejson():
	courserec = [course.to_json() for course in Course.query.all()]
	response = { 'records': courserec }
	return jsonify(response)

@course_sysbp.route('/add_course_json',methods=['POST'])
def addcoursejson():
	jsdat = request.json
	check_course = Course.query.filter_by(ID = jsdat.get_data('id')).all()

	if check_course and check_course.count() != 0:
		return jsonify({ 'error' : 'Course already in database'})

	check_course = Course.query.filter_by(name = jsdat.get_data('name')).all()

	if check_course and check_course.count() != 0:
		return jsonify({ 'error' : 'Course already in database'})

	if jsdat.get_data('id') == '' or jsdat.get_data('id') is None:
		return jsonify({ 'error' : 'bad info'})

	if jsdat.get_data('name') == '' or jsdat.get_data('name') is None:
		return jsonify({ 'error' : 'bad info'})

	course = Course.from_json(jsdat)
	if course is None:
		return jsonify({ 'error' : 'bad info'})

	try:
		db.session.add(course)
		db.session.commit()
		return jsonify({ 'status' : 'success'})
	except:
		return jsonify({ 'status' : 'fail'})

@course_sysbp.route('/modify_course_json',methods=['POST'])
def modifycoursejson():
	oldjs = request.json['old']
	newjs = request.json['new']
	
	course = Course.query.filter_by(ID=oldjs.get('id')).first_or_404()
	if course is None:
		return jsonify({ 'error' : 'bad info'})

	course = Course.query.filter_by(name=oldjs.get('name')).first_or_404()
	if course is None:
		return jsonify({ 'error' : 'bad info'})

	if newjs.get('id') == '' or newjs.get('id') is None:
		return jsonify({ 'error' : 'bad info'})
	if newjs.get('name') == '' or newjs.get('name') is None:
		return jsonify({ 'error' : 'bad info'})

	check_course = Course.query.filter_by(ID = newjs.get('id')).all()

	if check_course:
		return jsonify({ 'error' : 'Course already in database'})

	check_course = Course.query.filter_by(name = newjs.get('name')).all()

	if check_course:
		return jsonify({ 'error' : 'Course already in database'})

	try:
		course.ID = newjs.get('id') or course.ID
		course.name = newjs.get('name') or course.name

		db.session.commit()
		return jsonify({ 'status' : 'success'})
	except:
		return jsonify({ 'status' : 'fail'})

@course_sysbp.route('/delete_course_json',methods=['POST'])
def delcoursejson():
	course = Course.query.filter_by(ID=request.get_data('id')).first_or_404()
	if course is None:
		return jsonify({ 'error' : 'bad info'})

	db.session.delete(course)
	db.session.commit()
	return jsonify({ 'status' : 'success'})
