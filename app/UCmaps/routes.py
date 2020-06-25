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
from app.models import stud_courses,prof_courses,ta_courses,Role
from app.tables import MapResults

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

@mapbp.route('/check_map_json',methods=['GET','POST'])
def checkmapjson():
	PC = [tup.to_json() for tup in db.session.query(prof_courses).all()]
	TC = [tup.to_json() for tup in db.session.query(ta_courses).all()]
	SC = [tup.to_json() for tup in db.session.query(stud_courses).all()]
	response = {'records_P': PC, 
				'records_T': TC,
				'records_S': SC
				}
	return jsonify(response)

@mapbp.route('/add_map_json',methods=['POST'])
def addmapjson():
	
	return jsonify(response)

@mapbp.route('/modify_map_json',methods=['POST'])
def modifymapjson():
	maprec = [tup.to_json() for tup in db.session.query(prof_courses).all()]
	maprec.append([tup.to_json() for tup in db.session.query(ta_courses).all()])
	maprec.append([tup.to_json() for tup in db.session.query(stud_courses).all()])	
	response = { 'records': maprec }
	return jsonify(response)

@mapbp.route('/delete_map_json',methods=['POST'])
def delmapjson():
	maprec = [tup.to_json() for tup in db.session.query(prof_courses).all()]
	maprec.append([tup.to_json() for tup in db.session.query(ta_courses).all()])
	maprec.append([tup.to_json() for tup in db.session.query(stud_courses).all()])	
	response = { 'records': maprec }
	return jsonify(response)
