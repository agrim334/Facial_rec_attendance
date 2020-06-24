from app import db
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for,session,current_app
from app.forms import ManualAttendForm,CheckAttendanceForm,AttendForm
import face_recognition
import os
from . import attd_sysbp
from app.log_sys import log_sysbp
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user,logout_user,login_required
from app.models import User,Course,Attendance,ta_courses,prof_courses,stud_courses,Department,Role
import numpy as np
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from datetime import datetime,timedelta
import re
from app.tables import AttendanceResults

AP = current_app._get_current_object()

#fa_role = Role.query.filter_by(name="Faculty").first()
#ta_role = Role.query.filter_by(name="TA").first()
#admin_role = Role.query.filter_by(name="Admin").first()
#stud_role = Role.query.filter_by(name="Student").first()

basedir = os.path.abspath(os.path.dirname(__file__))
AP.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')
photos = UploadSet('photos', IMAGES)
configure_uploads(AP, photos)
patch_request_class(AP)

@attd_sysbp.before_request
def make_session_permanent():
	session.permanent = True
	attd_sysbp.permanent_session_lifetime = timedelta(minutes=10)		#idle timeout for user session

@attd_sysbp.after_request
def after_request(response):									#security
	response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-XSS-Protection'] = '1; mode=block'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response

@attd_sysbp.route('/check_attendance_json',methods=['GET','POST'])
def checkattdjson():
	attdrec = [attd.to_json() for attd in Attendance.query.all()]
	response = { 'records': attdrec }
	return jsonify(response)

@attd_sysbp.route('/mark_attendance_json',methods=['POST'])
def markattdjson():
	attd = Attendance.from_json(request.json)
	db.session.add(attd)
	db.session.commit()
	return jsonify(attd.to_json())

@attd_sysbp.route('/modify_attendance_json',methods=['POST'])
def modifyattdjson():
	attd = Attendance.from_json(request.json)
	db.session.add(attd)
	db.session.commit()
	return jsonify(attd.to_json())

@attd_sysbp.route('/delete_attendance_json',methods=['POST'])
def delattdjson():
	attd = Attendance.from_json(request.json)
	db.session.add(attd)
	db.session.commit()
	return jsonify(attd.to_json())