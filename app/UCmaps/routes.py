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
	value = int(request.get_data('choice'))
	pc = []
	sc = []
	tc = []
	if value == 1:
		pc = [{'cid': tup.CID, 'uid': tup.FID} for tup in db.session.query(prof_courses).all()]
	if value == 2:
		tc = [{'cid': tup.CID, 'uid': tup.TAID} for tup in db.session.query(ta_courses).all()]
	if value == 3:
		sc = [{'cid': tup.CID, 'uid': tup.SID} for tup in db.session.query(stud_courses).all()]
	response =	{
				'records_p' : pc,
				'records_t' : tc,
				'records_s' : sc,
				}

	return jsonify(response)

@mapbp.route('/add_map_json',methods=['POST'])
def addmapjson():
	user = User.query.filter_by(username=request.json['uid']).first()
	course = Course.query.filter_by(ID=request.json['cid']).first()
	fa_role = Role.query.filter_by(name="Prof").first()
	stud_role = Role.query.filter_by(name="Student").first()
	ta_role = Role.query.filter_by(name="TA").first()
	admin_role = Role.query.filter_by(name="Admin").first()

	if user.role_id == fa_role.ID:
		user.facult.append(course)
	elif user.role_id == ta_role.ID:
		user.tutoring.append(course)
	elif user.role_id == stud_role.ID:
		user.opted.append(course)

	db.session.commit()
	return jsonify({'status':'success'})

@mapbp.route('/modify_map_json',methods=['POST'])
def modifymapjson():
	oldjs = request.json['old']
	newjs = request.json['new']

	user_old = User.query.filter_by(username=oldjs.get('uid')).first()
	user_new = User.query.filter_by(username=newjs.get('uid')).first()
	course_old = Course.query.filter_by(ID = oldjs.get('cid')).first()
	course_new = Course.query.filter_by(ID = newjs.get('cid')).first()

	fa_role = Role.query.filter_by(name="Prof").first()
	stud_role = Role.query.filter_by(name="Student").first()
	ta_role = Role.query.filter_by(name="TA").first()
	admin_role = Role.query.filter_by(name="Admin").first()

	if user_old.role_id == fa_role.ID:
		user_old.facult.remove(course_old)

	elif user_old.role_id == ta_role.ID:
		user_old.tutoring.remove(course_old)

	elif user_old.role_id == stud_role.ID:
		user_old.opted.remove(course_old)

	if user_new.role_id == fa_role.ID:
		user_new.facult.append(course_new)

	elif user_new.role_id == ta_role.ID:
		user_new.tutoring.append(course_new)

	elif user_new.role_id == stud_role.ID:
		user_new.opted.append(course_new)


	db.session.commit()

	return jsonify({'status':'success'})

@mapbp.route('/delete_map_json',methods=['POST'])
def delmapjson():
	user = User.query.filter_by(username=request.json['uid']).first()
	course = Course.query.filter_by(ID=request.json['cid']).first()
	fa_role = Role.query.filter_by(name="Prof").first()
	stud_role = Role.query.filter_by(name="Student").first()
	ta_role = Role.query.filter_by(name="TA").first()
	admin_role = Role.query.filter_by(name="Admin").first()

	if user.role_id == fa_role.ID:
		user.facult.remove(course)
	elif user.role_id == ta_role.ID:
		user.tutoring.remove(course)
	elif user.role_id == stud_role.ID:
		user.opted.remove(course)

	db.session.commit()
	return jsonify({'status':'success'})