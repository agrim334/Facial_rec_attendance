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
def markcoursejson():
	course = Course.from_json(request.json)
	if course is None:
		return jsonify({ 'error' : 'bad info'})
	
	db.session.add(course)
	db.session.commit()
	return jsonify({ 'status' : 'success'})

@course_sysbp.route('/modify_course_json',methods=['POST'])
def modifycoursejson():
	course = Course.query.filter_by(ID=request.json['old'].get('id')).first_or_404()
	if course is None:
		return jsonify({ 'error' : 'bad info'})

	course.ID = request.json['new'].get('id') or course.ID
	course.name = request.json['new'].get('name') or course.name

	db.session.commit()
	return jsonify({ 'status' : 'success'})

@course_sysbp.route('/delete_course_json',methods=['POST'])
def delcoursejson():
	course = Course.query.filter_by(ID=request.get_data('id')).first_or_404()
	if course is None:
		return jsonify({ 'error' : 'bad info'})

	db.session.delete(course)
	db.session.commit()
	return jsonify({ 'status' : 'success'})
