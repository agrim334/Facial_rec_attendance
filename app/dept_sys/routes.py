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
	deptrec = [dept.to_json() for dept in Department.query.all()]
	response = { 'records': deptrec }
	return jsonify(response)

@dept_sysbp.route('/add_dept_json',methods=['POST'])
def adddeptjson():
	print(request.json)
	dept = Department.from_json(request.json)
	if dept is None:
		return jsonify({ 'error' : 'bad info'})

	db.session.add(dept)
	db.session.commit()
	return jsonify({'status' : 'success'})

@dept_sysbp.route('/modify_dept_json',methods=['POST'])
def modifydeptjson():
	dept = Department.query.filter_by(ID=request.json['old'].get('id')).first_or_404()
	print(dept)
	if dept is None:
		return jsonify({ 'error' : 'bad info'})

	dept.ID = request.json['new'].get('id') or dept.ID
	dept.name = request.json['new'].get('name') or dept.name 

	db.session.commit()
	return jsonify({'status' : 'success'})

@dept_sysbp.route('/delete_dept_json',methods=['POST'])
def deldeptjson():
	dept = Department.query.filter_by(ID=request.get_data('id')).first_or_404()
	db.session.delete(dept)
	db.session.commit()
	return jsonify({'status' : 'success'})