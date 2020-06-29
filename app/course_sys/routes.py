from .. import db,errors
from . import course_sysbp
from app.log_sys import log_sysbp
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for,session
from app.forms import CourseForm,ViewCourseForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user,logout_user,login_required
from ..models import User,Role,Course,Department,Permission
from datetime import datetime,timedelta
from app.tables import CourseResults
import re
from app.log_sys.routes import token_required

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
@token_required(Permission.READ | Permission.ADMIN)
def checkcoursejson():
	try:
		courserec = [course.to_json() for course in Course.query.all()]
		response = { 'records': courserec }
		return jsonify(response)
	except:
		return {'status':'data fetch failed'}

@course_sysbp.route('/add_course_json',methods=['POST'])
@token_required(Permission.ADMIN)
def addcoursejson():
	jsdat = request.json
	check_course = Course.query.filter_by(ID = jsdat.get('id'),name = jsdat.get('name')).all()

	if check_course and check_course.count() != 0:
		return jsonify({ 'status' : 'Course already in database'})

	if jsdat.get('id') == '' or jsdat.get('id') is None:
		return jsonify({ 'status' : 'no couse id given'})

	if jsdat.get('name') == '' or jsdat.get('name') is None:
		return jsonify({ 'status' : 'no course name given'})

	course = Course.from_json(jsdat)
	if course is None:
		return jsonify({ 'status' : 'couldn\'t create course record'})

	try:
		db.session.add(course)
		db.session.commit()
		return jsonify({ 'status' : 'success'})
	except:
		return jsonify({ 'status' : 'fail'})

@course_sysbp.route('/modify_course_json',methods=['POST'])
@token_required(Permission.ADMIN)
def modifycoursejson():
	oldjs = request.json['old']
	newjs = request.json['new']
	
	course = Course.query.filter_by(ID=oldjs.get('id'),name=oldjs.get('name')).all()

	if not course:
		return jsonify({ 'status' : 'No course {} in database'.format(oldjs.get('id'))})

	if newjs.get('id') == '' or newjs.get('id') is None:
		return jsonify({ 'status' : 'empty course id'})
	if newjs.get('name') == '' or newjs.get('name') is None:
		return jsonify({ 'status' : 'empty course name'})

	check_course = Course.query.filter_by(ID = newjs.get('id'),name = newjs.get('name')).all()

	if check_course:
		return jsonify({ 'status' : 'Course already in database'})

	course.ID = newjs.get('id') or course.ID
	course.name = newjs.get('name') or course.name

	try:

		db.session.commit()
		return jsonify({ 'status' : 'Course modify success'})
	except:
		return jsonify({ 'status' : 'Course modify fail'})

@course_sysbp.route('/delete_course_json',methods=['POST'])
@token_required(Permission.ADMIN)
def delcoursejson():
	if not request.get_data('id'):
		return jsonify({ 'status' : 'No id given'})

	course = Course.query.filter_by(ID=request.get_data('id')).all()
	if not course:
		return jsonify({ 'status' : 'No such course in database'})
	try:
		db.session.delete(course)
		db.session.commit()
		return jsonify({ 'status' : 'Course deletion success'})
	except:
		return jsonify({ 'status' : 'Course deletion failed'})
