from .. import db,errors
from . import dept_sysbp
from app.log_sys import log_sysbp
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for,session
from app.forms import DeptForm,ViewDeptForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user,logout_user,login_required
from ..models import User,Role,Department
from datetime import datetime,timedelta
import re
from app.tables import DeptTable

#fa_role = Role.query.filter_by(name="Faculty").first()
#ta_role = Role.query.filter_by(name="TA").first()
#admin_role = Role.query.filter_by(name="Admin").first()
#stud_role = Role.query.filter_by(name="Student").first()

@dept_sysbp.before_request
def make_session_permanent():
	session.permanent = True
	dept_sysbp.permanent_session_lifetime = timedelta(minutes=10)		#idle timeout for user session

@dept_sysbp.after_request
def after_request(response):									#security
	response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-XSS-Protection'] = '1; mode=block'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response

@dept_sysbp.route('/check_dept_json',methods=['GET','POST'])
def checkdeptjson():
	try:
		deptrec = [dept.to_json() for dept in Department.query.all()]
		response = { 'records': deptrec }
		return jsonify(response)
	except:
		return {'status':'data fetch failed'}

@dept_sysbp.route('/add_dept_json',methods=['POST'])
def adddeptjson():
	jsdat = request.json
	check_dept = Department.query.filter_by(ID = jsdat.get('id')).all()

	if check_dept:
		return jsonify({ 'status' : 'dept already in database'})

	if jsdat.get('id') == '' or jsdat.get('id') is None:
		return jsonify({ 'status' : 'empty dept id'})
	if jsdat.get('name') == '' or jsdat.get('name') is None:
		return jsonify({ 'status' : 'empty dept name'})

	dept = Department.from_json(jsdat)
	if dept is None:
		return jsonify({ 'status' : 'can\'t create department record'})

	try:
		db.session.add(dept)
		db.session.commit()
		return jsonify({ 'status' : 'Dept add success'})
	except:
		return jsonify({ 'status' : 'Dept add fail'})

@dept_sysbp.route('/modify_dept_json',methods=['POST'])
def modifydeptjson():
	oldjs = request.json['old']
	newjs = request.json['new']
	
	dept = Department.query.filter_by(ID=oldjs.get('id'),name=oldjs.get('name')).first_or_404()
	if dept is None:
		return jsonify({ 'status' : 'No such Department as {}'.format(newjs.get('name'))})

	if newjs.get('id') == '' or newjs.get('id') is None:
		return jsonify({ 'status' : 'empty dept id'})

	if newjs.get('name') == '' or newjs.get('name') is None:
		return jsonify({ 'status' : 'empty dept name'})

	check_dept = Department.query.filter_by(ID = newjs.get('id')).all()

	if not check_dept:
		return jsonify({ 'status' : 'Dept {} already in database'.format(newjs.get('id'))})

	dept.ID = newjs.get('id') or dept.ID
	dept.name = newjs.get('name') or dept.name

	try:
		db.session.commit()
		return jsonify({ 'status' : 'Dept modify success'})
	except:
		return jsonify({ 'status' : 'Dept modify fail'})

@dept_sysbp.route('/delete_dept_json',methods=['POST'])
def deldeptjson():
	if not request.get_data('id'):
		return jsonify({ 'status' : 'No id given'})

	dept = Department.query.filter_by(ID=request.get_data('id')).all()
	if not check_dept:
		return jsonify({ 'status' : 'No such department in database'})
	try:
		db.session.delete(dept)
		db.session.commit()
		return jsonify({ 'status' : 'Dept deletion success'})
	except:
		return jsonify({ 'status' : 'Dept deletion failed'})
