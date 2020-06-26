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

basedir = os.path.abspath(os.path.dirname(__file__))
AP.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')
upldir = os.path.join(basedir, 'uploads')
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

@attd_sysbp.route('/check_attd_json',methods=['GET','POST'])
def checkattdjson():
	attdrec = [attd.to_json() for attd in Attendance.query.all()]
	response = { 'records': attdrec }
	return jsonify(response)

@attd_sysbp.route('/add_attd_json',methods=['POST'])
def addattdjson():
	cid = None
	uid = None
	if request.json:
		fa_role = Role.query.filter_by(name="Faculty").first()
		ta_role = Role.query.filter_by(name="TA").first()
		admin_role = Role.query.filter_by(name="Admin").first()
		stud_role = Role.query.filter_by(name="Student").first()

		jsdat = request.json
		if jsdat.get('uid') == '' or jsdat.get('uid') is None:
			return jsonify({ 'status' : 'bad info'})

		check_user = User.query.filter_by(username = jsdat.get('uid')).all()

		if not check_user:
			return jsonify({ 'status' : 'User not in database'})

		if jsdat.get('cid') == '' or jsdat.get('cid') is None:
			return jsonify({ 'status' : 'bad info'})

		check_course = Course.query.filter_by(ID = jsdat.get('cid')).all()

		if not check_course:
			return jsonify({ 'status' : 'Course not in database'})

		check_map = None
		if check_user.role_id == fa_role.role_id:
			check_map = db.session.query(prof_courses).filter_by(FID=uid,CID=cid).all()
	
		elif check_user.role_id == ta_role.role_id:
			check_map = db.session.query(ta_courses).filter_by(TAID=uid,CID=cid).all()
	
		if check_map is None:
			return jsonify({ 'error' : 'bad info'})
	
		cid = jsdat.get('cid')
		uid = jsdat.get('uid')

		return jsonify({ 'error' : 'bad info'})

	elif request.files:
		for f in request.files:
			t = request.files[f]
			filename = secure_filename(request.files[f].filename)
			t.save(secure_filename(os.path.join(upldir, filename)))

		if cid and uid:
			detect_faces_in_image(upldir,cid,uid)

		return jsonify({ 'error' : 'bad info'})

@attd_sysbp.route('/modify_attd_json',methods=['POST'])
def modifyattdjson():
	oldjs = request.json['old']

	if not oldjs:
		return jsonify({ 'error' : 'bad info'})

	newjs = request.json['new']	

	if not newjs:
		return jsonify({ 'error' : 'bad info'})

	attd = Attendance.query.filter_by(CID=oldjs.get('cid'),SID=oldjs.get('markeeid'),timestamp=oldjs.get('ts')).first()
	if not attd:
		return jsonify({ 'error' : 'bad info'})

	if newjs.get('cid') == '' or newjs.get('cid') is None:
		return jsonify({ 'error' : 'bad info'})

	course = Course.query.filter_by(username=newjs.get('cid')).first()
	if not course:
		return jsonify({ 'error' : 'bad info'})

	if newjs.get('ts') == '' or newjs.get('ts') is None:
		return jsonify({ 'error' : 'bad info'})

	if newjs.get('markeeid') == '' or newjs.get('markeeid') is None:
		return jsonify({ 'error' : 'bad info'})

	user = User.query.filter_by(username=newjs.get('markeeid')).first()
	if not user:
		return jsonify({ 'error' : 'bad info'})

	if newjs.get('markerid') == '' or newjs.get('markerid') is None:
		return jsonify({ 'error' : 'bad info'})

	user = User.query.filter_by(username=newjs.get('markerid')).first()
	if not user:
		return jsonify({ 'error' : 'bad info'})

	attd.CID = request.json['new'].get('cid') or attd.CID
	attd.SID = request.json['new'].get('sid') or attd.SID
	attd.FID = request.json['new'].get('fid') or attd.FID
	attd.TAID = request.json['new'].get('taid') or attd.TAID
	attd.timestamp = request.json['new'].get('timestamp') or attd.timestamp

	db.session.commit()
	return jsonify({ 'status' : 'success'})


@attd_sysbp.route('/delete_attd_json',methods=['POST'])
def delattdjson():
	jsdat = request.json
	if not jsdat:
		return jsonify({ 'error' : 'bad info'})

	attd = Attendance.query.filter_by(CID=jsdat.get('cid'),SID=jsdat.get('markeeid'),timestamp=jsdat.get('ts')).first()
	if not attd:
		return jsonify({ 'error' : 'bad info'})

	try:
		db.session.delete(attd)
		db.session.commit()
		return jsonify({ 'status' : 'User deletion success'})
	except:
		return jsonify({ 'status' : 'User deletion failed'})

def detect_faces_in_image(file_stream,CID,user):
	result = []
	fa_role = Role.query.filter_by(name="Faculty").first()
	ta_role = Role.query.filter_by(name="TA").first()
	admin_role = Role.query.filter_by(name="Admin").first()
	stud_role = Role.query.filter_by(name="Student").first()

	try:
		known_dir = "/home/agrim/Downloads/known/"+str(CID)+"/"
		base = os.path.abspath(os.path.dirname(__file__))
		known_face_encd = []
		known_face_name = {}
		result = []
		num = 0
		pat = re.compile('[0-9A-Za-z]+\.')

		for image in os.listdir(known_dir):
			temp = face_recognition.load_image_file(known_dir+image)
			inp_face_locations = face_recognition.face_locations(temp, model = "cnn")
			encd= face_recognition.face_encodings(temp, known_face_locations = inp_face_locations)[0]
			known_face_encd.append(encd)
			image = pat.match(image)[0]
			image = image[:-1]
			known_face_name[str(encd)] = image

		for file in os.listdir(file_stream):

			un_image = face_recognition.load_image_file(file_stream+file)

			face_locations = face_recognition.face_locations(un_image,model = "cnn")

			un_face_encodings = face_recognition.face_encodings(un_image,known_face_locations=face_locations)

			if len(un_face_encodings) > 0:
				for face_encoding in un_face_encodings:
					num = num + 1
					matches = face_recognition.compare_faces(known_face_encd, face_encoding)
					name = "Unknown"

					face_distances = face_recognition.face_distance(known_face_encd, face_encoding)
					best_match_index = np.argmin(face_distances)

					if matches[best_match_index]:
						im = known_face_encd[best_match_index]
						name = known_face_name[str(im)]
					result.append(("Face number " + str(num),name))

					if name != "Unknown":
						name = pat.match(name)[0]
						name = name[:-1]
						stud = User.query.filter_by(username=name,role_id=stud_role.role_id).first() 
						if stud:
							c1 = db.session.query(stud_courses).filter_by(SID=stud.username,CID = CID)
							if c1:
								check = Attendance.query.filter_by(CID=CID,SID=stud.username,timestamp=datetime.today().strftime('%Y-%m-%d')) 
								if not check or check.count() == 0:
									if user.role_id == ta_role.role_id :
										atdrecord = Attendance(CID=CID,SID=stud.username,timestamp=datetime.today().strftime('%Y-%m-%d'),TAID = user.username)
									else:
										atdrecord = Attendance(CID=CID,SID=stud.username,timestamp=datetime.today().strftime('%Y-%m-%d'),FID = user.username)
									db.session.add(atdrecord)
									db.session.commit()

		already = db.session.query(stud_courses).join(Attendance,Attendance.CID == stud_courses.c.CID).filter_by(CID=CID,timestamp=datetime.today().strftime('%Y-%m-%d'))
		for image in os.listdir(base+"/uploads/"):
			if os.path.isfile(base+"/uploads/"+image):
				os.remove(base+"/uploads/"+image)
		return jsonify()
	except MemoryError as m:
		for image in os.listdir(base+"/uploads/"):
			if os.path.isfile(base+"/uploads/"+image):
				os.remove(base+"/uploads/"+image)
		return jsonify()
	except:
		for image in os.listdir(base+"/uploads/"):
			if os.path.isfile(base+"/uploads/"+image):
				os.remove(base+"/uploads/"+image)
		return jsonify()

def temp():
	for stu in recr:
		stud = User.query.filter_by(username=stu,role_id=stud_role.role_id) 
		if stud and stud.count() != 0:
			c1 = db.session.query(stud_courses).filter_by(stud_id=stu,course_id = request.args.get('CID'))
			if c1 and c1.count() != 0:
				check = Attendance.query.filter_by(course_id=request.args.get('CID'),student_id=stu,timestamp=datetime.today().strftime('%Y-%m-%d')) 
				if not check or check.count() == 0:
					atdrecord = Attendance(course_id=request.args.get('CID'),student_id=stu,timestamp=datetime.today().strftime('%Y-%m-%d'),faculty_id = current_user.username)
					db.session.add(atdrecord)
					db.session.commit()
					db.session.close()
