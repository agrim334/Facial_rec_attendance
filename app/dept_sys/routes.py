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

fa_role = Role.query.filter_by(role="Faculty").first()
ta_role = Role.query.filter_by(role="TA").first()
admin_role = Role.query.filter_by(role="Admin").first()
stud_role = Role.query.filter_by(role="Student").first()

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
@login_required
def checkdeptjson():
	deptrec = [dept.to_dict() for dept in Department.query.all()]
	response = { 'records': deptrec }
	return jsonify(response)

@dept_sysbp.route('/mark_dept_json',methods=['POST'])
@login_required
def markdeptjson():
	dept = Department.from_json(request.json)
	db.session.add(dept)
	db.session.commit()
	return jsonify(Department.to_dict())

@dept_sysbp.route('/modify_dept_json',methods=['POST'])
@login_required
def modifydeptjson():
	dept = Department.from_json(request.json)
	db.session.add(dept)
	db.session.commit()
	return jsonify(Department.to_dict())

@dept_sysbp.route('/delete_dept_json',methods=['POST'])
@login_required
def deldeptjson():
	dept = Department.from_json(request.json)
	db.session.add(dept)
	db.session.commit()
	return jsonify(Department.to_dict())

@dept_sysbp.route('/add_dept',methods=['GET','POST'])
@login_required
def add_dept():
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:
			form = DeptForm()
			if form.validate_on_submit():
				check_dept = Department.query.filter_by(Dept_name = form.depart.data)
				db.session.close()
				if check_dept and check_Department.count() != 0:
					flash('Department. has been added already in database')
					return redirect(url_for('.add_dept'))
				else:
					dept = Department(Dept_name = form.depart.data)
					db.session.add(dept)
					db.session.commit()
					db.session.close()
					flash('Department. has been added')
					return redirect(url_for('.add_dept'))
		
			return render_template('form_entry.html', title='Add Department.', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('log_sysbp.home'))
	else:
		flash('Login please!!')
		return redirect(url_for('log_sysbp.login'))

@dept_sysbp.route('/dept_view',methods=['GET','POST'])
@login_required
def view_dept():
	if current_user.is_authenticated:
		table = []
		form = ViewDeptForm()
		if form.validate_on_submit():
			if form.criteria.data == '1':
				dept = Department.query.all()
			else:
				dept = Department.query.filter_by(Dept_name=form.match.data)
			if dept:
				table = DeptTable(dept)
				table.border = True
			else:
				flash("No Department.s Found")
				return redirect(url_for('.view_dept'))
		return render_template('view.html',title="Department.",form=form,table=table)
	else:
		flash('Login please')
		return redirect(url_for('log_sysbp.login'))

@dept_sysbp.route('/upd_dept',methods=['GET','POST'])
@login_required
def upd_dept():
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:
			form = DeptForm()
			if form.validate_on_submit():
				check_dept = Department.query.filter_by(Dept_name = form.depart.data)
				db.session.close()
				if check_dept and check_Department.count() != 0:
					flash('Department. has been added already in database')
					return redirect(url_for('.upd_dept'))
				else:
					dept = Department(Dept_name = form.depart.data)
					db.session.add(dept)
					db.session.commit()
					db.session.close()
					flash('Department. has been added')
					return redirect(url_for('.upd_dept'))
		
			return render_template('form_entry.html', title='Add Department.', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('log_sysbp.home'))
	else:
		flash('Login please!!')
		return redirect(url_for('log_sysbp.login'))

@dept_sysbp.route('/del_dept',methods=['GET','POST'])
@login_required
def del_dept():
	if current_user.is_authenticated:
		if current_user.role_id == admin_role.role_id:
			form = DeptForm()
			if form.validate_on_submit():
				check_dept = Department.query.filter_by(Dept_name = form.depart.data)
				db.session.close()
				if check_dept and check_Department.count() != 0:
					flash('Department. has been added already in database')
					return redirect(url_for('.del_dept'))
				else:
					dept = Department(Dept_name = form.depart.data)
					db.session.add(dept)
					db.session.commit()
					db.session.close()
					flash('Department. has been added')
					return redirect(url_for('.del_dept'))
		
			return render_template('form_entry.html', title='Add Department.', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('log_sysbp.home'))
	else:
		flash('Login please!!')
		return redirect(url_for('log_sysbp.login'))
