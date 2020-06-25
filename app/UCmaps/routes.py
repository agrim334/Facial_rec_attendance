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
	fa_role = Role.query.filter_by(name="Prof").first()
	stud_role = Role.query.filter_by(name="Student").first()
	ta_role = Role.query.filter_by(name="TA").first()
	admin_role = Role.query.filter_by(name="Admin").first()

	if user.role_id == fa_role.ID:
		stmt = prof_courses.insert().values(FID=request.json['uid'],CID=request.json['cid'])
	elif user.role_id == ta_role.ID:
		stmt = ta_courses.insert().values(TAID=request.json['uid'],CID=request.json['cid'])
	elif user.role_id == stud_role.ID:
		stmt = stud_courses.insert().values(SID=request.json['uid'],CID=request.json['cid'])

	db.session.execute(stmt)
	db.session.commit()
	return jsonify({'status':'success'})

@mapbp.route('/modify_map_json',methods=['POST'])
def modifymapjson():
	user = User.query.filter_by(username=request.json['old'].get('uid')).first()
	fa_role = Role.query.filter_by(name="Prof").first()
	stud_role = Role.query.filter_by(name="Student").first()
	ta_role = Role.query.filter_by(name="TA").first()
	admin_role = Role.query.filter_by(name="Admin").first()

	if user.role_id == fa_role.ID:
		stmt = prof_courses.delete().where(prof_courses.c.FID == request.json['old'].get('uid') and prof_courses.c.CID == request.json['old'].get('cid'))
		db.session.execute(stmt)
		stmt2 = prof_courses.insert().values(FID=request.json['new'].get('uid'),CID=request.json['new'].get('cid'))
		db.session.execute(stmt2)

	elif user.role_id == ta_role.ID:
		stmt = ta_courses.delete().where(ta_courses.c.TAID == request.json['old'].get('uid') and ta_courses.c.CID == request.json['old'].get('cid'))
		db.session.execute(stmt)
		stmt2 = ta_courses.insert().values(TAID=request.json['new'].get('uid'),CID=request.json['new'].get('cid'))
		db.session.execute(stmt2)

	elif user.role_id == stud_role.ID:
		stmt = stud_courses.delete().where(stud_courses.c.SID == request.json['old'].get('uid') and stud_courses.c.CID == request.json['old'].get('cid'))
		db.session.execute(stmt)
		stmt2 = stud_courses.insert().values(SID=request.json['new'].get('uid'),CID=request.json['new'].get('cid'))
		db.session.execute(stmt2)

	db.session.commit()

	return jsonify({'status':'success'})

@mapbp.route('/delete_map_json',methods=['POST'])
def delmapjson():
	user = User.query.filter_by(username=request.json['uid']).first()
	fa_role = Role.query.filter_by(name="Prof").first()
	stud_role = Role.query.filter_by(name="Student").first()
	ta_role = Role.query.filter_by(name="TA").first()
	admin_role = Role.query.filter_by(name="Admin").first()

	if user.role_id == fa_role.ID:
		stmt = prof_courses.delete().where(prof_courses.c.FID == request.json['uid'] and prof_courses.c.CID == request.json['cid'])
	elif user.role_id == ta_role.ID:
		stmt = ta_courses.delete().where(ta_courses.c.TAID == request.json['uid'] and ta_courses.c.CID == request.json['cid'])
	elif user.role_id == stud_role.ID:
		stmt = stud_courses.delete().where(stud_courses.c.SID == request.json['uid'] and stud_courses.c.CID ==  request.json['cid'])

	db.session.execute(stmt)
	db.session.commit()

	return jsonify({'status':'success'})