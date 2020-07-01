from app import db
from flask import jsonify, request,current_app
import face_recognition
import os
from . import attd_sysbp
from app.models import Permission,User,Course,Attendance,ta_courses,prof_courses,stud_courses
import numpy as np
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from datetime import datetime
import re
from app.log_sys.routes import token_required
from werkzeug.utils import secure_filename

AP = current_app._get_current_object()

basedir = os.path.abspath(os.path.dirname(__file__))
AP.config['UPLOADED_PHOTOS_DEST'] = AP.config['UPL_DIR']
upldir = AP.config['UPL_DIR']
known_dir = AP.config['KWN_DIR']
photos = UploadSet('photos', IMAGES)
configure_uploads(AP, photos)
patch_request_class(AP)


@attd_sysbp.after_request
def after_request(response):									#security
	response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-XSS-Protection'] = '1; mode=block'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
	return response

@attd_sysbp.route('/check_attd_json',methods=['GET','POST'])
@token_required(Permission.READ)
def checkattdjson():
	attdrec = [attd.to_json() for attd in Attendance.query.all()]
	response = { 'records': attdrec }
	return jsonify(response)

@attd_sysbp.route('/add_attd_json',methods=['GET','POST'])
@token_required(Permission.CUD_ATTD)
def addattdjson():
	if request.json:
		jsdat = request.json
		if jsdat.get('mancheck') == 1:
			manmark(jsdat.get('studlist'),jsdat.get('cid'),jsdat.get('uid'))
			return jsonify({ 'result' : 'success'})
		else:
			if jsdat.get('uid') == '' or jsdat.get('uid') is None:
				return jsonify({ 'result' : 'bad info'})

			check_user = User.query.filter_by(username = jsdat.get('uid')).first()
			if not check_user:
				return jsonify({ 'result' : 'User not in database'})

			if jsdat.get('cid') == '' or jsdat.get('cid') is None:
				return jsonify({ 'result' : 'No such course'})

			check_course = Course.query.filter_by(ID = jsdat.get('cid')).first()

			if not check_course:
				return jsonify({ 'result' : 'Course not in database'})

			check_map = None
			cid = jsdat.get('cid')
			uid = jsdat.get('uid')
			if check_user.role.name == 'Prof':
				check_map = db.session.query(prof_courses).filter_by(FID=uid,CID=cid).all()
			elif check_user.role.name == 'TA':
				check_map = db.session.query(ta_courses).filter_by(TAID=uid,CID=cid).all()
				
			if check_map is None:
				return jsonify({ 'result' : 'No such mapping'})

			return jsonify({ 'result' : 'Success'})

	elif request.files:
		uid = request.form.get('uid')
		cid = request.form.get('cid')
		temp = os.path.join(upldir,cid)
		if not os.path.exists(temp):
			os.makedirs(temp)

		for f in request.files:
			t = request.files[f]
			filename = secure_filename(request.files[f].filename)
			t.save(os.path.join(temp, filename))

		reglist = detect_faces_in_image(upldir,cid,uid)
		return jsonify({'studlist' : reglist, 'result': 'success'})

@attd_sysbp.route('/modify_attd_json',methods=['POST'])
@token_required(Permission.CUD_ATTD)
def modifyattdjson():
	oldjs = request.json['old']

	if not oldjs:
		return jsonify({ 'result' : 'not received original record info'})

	newjs = request.json['new']	

	if not newjs:
		return jsonify({ 'result' : 'not received modified record info'})

	attd = Attendance.query.filter_by(CID=oldjs.get('cid'),SID=oldjs.get('sid'),timestamp=oldjs.get('ts')).all()

	if not attd:
		return jsonify({ 'result' : 'original record not in database'})

	if newjs.get('cid') == '' or newjs.get('cid') is None:
		return jsonify({ 'result' : 'no cid given'})

	course = Course.query.filter_by(username=newjs.get('cid')).first()
	if not course:
		return jsonify({ 'result' : 'no course with given course id'})


	if newjs.get('mid') == '' or newjs.get('mid') is None:
		return jsonify({ 'result' : 'missing marker id'})

	if newjs.get('sid') == '' or newjs.get('sid') is None:
		return jsonify({ 'result' : 'missing student id'})

	user = User.query.filter_by(username=newjs.get('sid')).all()
	if not user:
		return jsonify({ 'result' : 'no student with given student id'})

	user = User.query.filter_by(username=newjs.get('mid')).all()
	if not user:
		return jsonify({ 'result' : 'No faculty or ta with given marker id'})

	attd.CID = newjs.get('cid') or attd.CID
	attd.SID = newjs.get('sid') or attd.SID
	
	check_stud_map = db.session.query(stud_courses).filter_by(SID=newjs.get('sid'),CID=newjs.get('cid')).all()
	if not check_stud_map:
		return jsonify({ 'result' : 'Student with id {} not registered for course {}'.format(newjs.get('sid'),newjs.get('cid'))})

	if user.role.name == 'TA':
		check_ta_map = db.session.query(ta_courses).filter_by(TAID=newjs.get('mid'),CID=newjs.get('cid')).all()
		if not check_ta_map:
			return jsonify({ 'result' : 'TA with id {} not authorized for course {}'.format(newjs.get('mid'),newjs.get('cid'))})

		attd.TAID = newjs.get('mid') or attd.TAID
	
	elif user.role.name == 'Prof':
		check_prof_map = db.session.query(prof_courses).filter_by(FID=newjs.get('mid'),CID=newjs.get('cid')).all()
		if not check_prof_map:
			return jsonify({ 'result' : 'Faculty with id {} not authorized for course {}'.format(newjs.get('mid'),newjs.get('cid'))})

		attd.FID = newjs.get('mid') or attd.FID

	if newjs.get('time') == '' or newjs.get('time') is None:
		return jsonify({ 'result' : 'missing timestamp'})
	

	attd.timestamp = newjs.get('time') or attd.timestamp

	try:
		db.session.commit()
		return jsonify({ 'result' : 'success'})
	except:
		return jsonify({ 'result' : 'fail'})

@attd_sysbp.route('/delete_attd_json',methods=['POST'])
@token_required(Permission.CUD_ATTD)
def delattdjson():
	jsdat = request.json
	if not jsdat:
		return jsonify({ 'result' : 'bad info'})

	try:
		attd = Attendance.query.filter_by(CID=jsdat.get('cid'),SID=jsdat.get('sid'),timestamp=jsdat.get('time')).first()
		if not attd:
			return jsonify({ 'result' : 'no such record'})

		db.session.delete(attd)
		db.session.commit()
		return jsonify({ 'result' : 'Record deletion success'})
	except:
		return jsonify({ 'result' : 'Record deletion failed'})

def detect_faces_in_image(file_stream,CID,user):
	result = []

	reglist = []
	for r in db.session.query(stud_courses).filter_by(CID=CID):
		reglist.append({ 'id' : r.SID, 'result': 0 })
	try:
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
						stud = User.query.filter_by(username=name).first() 
						if stud and stud.role.name == 'Student':
							c1 = db.session.query(stud_courses).filter_by(SID=name,CID = CID)
							if c1:
								check = Attendance.query.filter_by(CID=CID,SID=name,timestamp=datetime.today().strftime('%Y-%m-%d')) 
								if not check or check.count() == 0:
									if user.role.name == 'TA' :
										atdrecord = Attendance(CID=CID,SID=name,timestamp=datetime.today().strftime('%Y-%m-%d'),TAID = user.username)
										db.session.add(atdrecord)
										db.session.commit()

									elif user.role.name == 'Prof':
										atdrecord = Attendance(CID=CID,SID=name,timestamp=datetime.today().strftime('%Y-%m-%d'),FID = user.username)
										db.session.add(atdrecord)
										db.session.commit()

		for r in db.session.query(stud_courses).join(Attendance,Attendance.CID == stud_courses.c.CID).filter_by(CID=CID,timestamp=datetime.today().strftime('%Y-%m-%d')):
			for d in reglist:
				if d['id'] == r.SID:
					d['result'] = 1
		for image in os.listdir(upldir):
			if os.path.isfile(upldir+image):
				os.remove(upldir+image)

	except MemoryError:
		for image in os.listdir(upldir):
			if os.path.isfile(upldir+image):
				os.remove(upldir+image)

	except:
		for image in os.listdir(upldir):
			if os.path.isfile(upldir+image):
				os.remove(upldir+image)
	return reglist

def manmark(studlist,CID,uid):
	check_course = Course.query.filter_by(ID=CID).all()
	if not check_course:
		return False

	check_user = User.query.filter_by(username=uid).first()
	if not check_user:
		return False

	for stu in studlist:
		stud_id = stu['id']
		if int(stu['result']) == 1:
			stud = User.query.filter_by(username=stud_id).first() 
			if stud and stud.role.name == 'Student':
				c1 = db.session.query(stud_courses).filter_by(SID=stud_id,CID = CID)
				if c1:
					check = Attendance.query.filter_by(CID=CID,SID=stud_id,timestamp=datetime.today().strftime('%Y-%m-%d')) 
					if not check or check.count() == 0:
						if check_user.role.name == 'TA' :
							atdrecord = Attendance(CID=CID,SID=stud_id,timestamp=datetime.today().strftime('%Y-%m-%d'),TAID = check_user.username)
							db.session.add(atdrecord)
							db.session.commit()

						elif check_user.role.name == 'Prof':
							atdrecord = Attendance(CID=CID,SID=stud_id,timestamp=datetime.today().strftime('%Y-%m-%d'),FID = check_user.username)
							db.session.add(atdrecord)
							db.session.commit()

	check_course.classes_held = check_course.classes_held + 1
	db.session.close()
	return True
