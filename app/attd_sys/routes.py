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

fa_role = Role.query.filter_by(role="Faculty").first()
ta_role = Role.query.filter_by(role="TA").first()
admin_role = Role.query.filter_by(role="Admin").first()
stud_role = Role.query.filter_by(role="Student").first()

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

@attd_sysbp.route('/check_attendance',methods=['GET','POST'])
@login_required
def checkattd():
	if current_user.is_authenticated:
		if current_user.role_id == stud_role.role_id:
			form =CheckAttendanceForm()
			table = []
			if form.validate_on_submit():
				CID = form.courseID.data
				course = Course.query.filter_by(Course_ID=CID).first()
				count = 0
				if course:
					count = course.Classes_held
					is_stud = db.session.query(stud_courses).filter_by(stud_id=current_user.username,course_id = CID)
					if is_stud and is_stud.count() != 0:
						attd = Attendance.query.filter_by(course_id=CID,student_id=current_user.username)
						if not attd or attd.count() == 0:
							flash('No record found')
							return redirect(url_for('.checkattd'))
						else:
							table = AttendanceResults(attd)
							table.border = True
					else:
						flash("You are not registered for this course")
						return redirect(url_for('.checkattd'))
				else:
					flash("No course with ID " + CID + " found")
					return redirect(url_for('.checkattd'))
				return render_template('check_attendance.html',form=form,table=table)
		else:
			flash('Not allowed')
			return redirect(url_for('log_sysbp.home'))
	else:
		flash('Login please')
		return redirect(url_for('log_sysbp.login'))
	return render_template('check_attendance.html',form=form,table=table)

def allowed_file(filename):															#set allowed extensions for images
	ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@attd_sysbp.route('/faces', methods=['GET', 'POST'])
@login_required
def upload_image():																	#upload images to mark attendance
	if current_user.is_authenticated:
		if current_user.role_id == fa_role.role_id:
			flash("Image format should be png,jpg or jpeg")
			form = AttendForm()
			if form.validate_on_submit():
				base = os.path.abspath(os.path.dirname(__file__))
				CID = form.CID.data
				course = Course.query.filter_by(Course_ID=CID) 			
				if course and course.count() != 0:
					confirm = db.session.query(prof_courses).filter_by(prof_id=current_user.username,course_id = CID)
					if confirm and confirm.count() != 0:
						file = request.files.getlist("photo")
					upl_dir = os.path.join(attd_sysbp.config['UPLOAD_PATH'],"uploads/")
					if not os.path.exists(upl_dir):
						os.makedirs(upl_dir)

						for f in file:
							filename = secure_filename(f.filename)
							f.save(os.path.join(upl_dir, filename))
						user = User.query.filter_by(username=current_user.username,role_id=fa_role.role_id)
						return detect_faces_in_image(upl_dir,CID,user)

					else:
						flash("You are not authorized to mark attendance for this course.")
						return redirect(url_for('log_sysbp.home'))
				else:
					flash("No Course found with code " + CID)
					return redirect(url_for('log_sysbp.home'))

		elif current_user.role_id == ta_role.role_id:
			form = AttendForm()
			flash("Image format should be png,jpg or jpeg")
			if form.validate_on_submit():
				base = os.path.abspath(os.path.dirname(__file__))
				CID = form.CID.data
				course = Course.query.filter_by(Course_ID=CID) 			

				if course and course.count() != 0:
					confirm = db.session.query(ta_courses).filter_by(ta_id=current_user.username,course_id = CID)
					if confirm and confirm.count() != 0:
						file = request.files.getlist("photo")
						upl_dir = os.path.join(attd_sysbp.config['UPLOAD_PATH'],"uploads/")
						if not os.path.exists(upl_dir):
							os.makedirs(upl_dir)

						for f in file:
							filename = secure_filename(f.filename)
							f.save(os.path.join(upl_dir, filename))
						user = User.query.filter_by(username=current_user.username,role_id=ta_role.role_id)
						return detect_faces_in_image(upl_dir,CID,user)

					else:
						flash("You are not authorized to mark attendance for this course.")
						return redirect(url_for('log_sysbp.home'))
				else:
					flash("No Course found with code " + CID)
					return redirect(url_for('log_sysbp.home'))
		else:
			flash('Not allowed')
			return redirect(url_for('log_sysbp.home'))
		return render_template("form_entry.html",title="Automated Attendance",form=form)
	else:
		flash('Login please')
		return redirect(url_for('log_sysbp.login'))

def detect_faces_in_image(file_stream,CID,user):
	result = []
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
							c1 = db.session.query(stud_courses).filter_by(ta_id=stud.username,course_id = CID)
							if c1:
								check = Attendance.query.filter_by(course_id=CID,student_id=stud.username,timestamp=datetime.today().strftime('%Y-%m-%d')) 
								if not check or check.count() == 0:
									if user.role_id == ta_role.role_id :
										atdrecord = Attendance(course_id=CID,student_id=stud.username,timestamp=datetime.today().strftime('%Y-%m-%d'),TA_id = user.username)
									else:
										atdrecord = Attendance(course_id=CID,student_id=stud.username,timestamp=datetime.today().strftime('%Y-%m-%d'),faculty_id = user.username)
									db.session.add(atdrecord)
									db.session.commit()

		for image in os.listdir(base+"/uploads/"):
			if os.path.isfile(base+"/uploads/"+image):
				os.remove(base+"/uploads/"+image)

		return redirect(url_for('.manual_mark',CID=CID))										#redirect to manual attendance to handle missed cases
	except MemoryError as m:
		flash("Ran out of memory.Switching to manual attendance")
		for image in os.listdir(base+"/uploads/"):
			if os.path.isfile(base+"/uploads/"+image):
				os.remove(base+"/uploads/"+image)

		return redirect(url_for('.manual_mark',CID=CID))

	except:

		for image in os.listdir(base+"/uploads/"):
			if os.path.isfile(base+"/uploads/"+image):
				os.remove(base+"/uploads/"+image)

		return redirect(url_for('.manual_mark',CID=CID))

@attd_sysbp.route('/manual', methods=['GET', 'POST'])
@login_required
def manual_mark():
	if current_user.is_authenticated:
		if current_user.role_id == fa_role.role_id:
			form = ManualAttendForm()
			form.manual.choices = [(student.stud_id,student.stud_id) for student in db.session.query(stud_courses).filter_by(course_id=request.args.get('CID'))]
			already = db.session.query(stud_courses).join(Attendance,Attendance.course_id == stud_courses.c.course_id).filter_by(course_id=request.args.get('CID'),timestamp=datetime.today().strftime('%Y-%m-%d'))
			form.manual.data = [r.stud_id for r in already]
			course = Course.query.filter_by(Course_ID=request.args.get('CID')).first()
			course.Classes_held = course.Classes_held + 1
			if form.validate_on_submit():
				recr = form.manual.data
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
				flash("Attendance marked")
				return redirect(url_for('log_sysbp.home'))

			return render_template('form_entry.html',title='Manual marking',form=form)

		elif current_user.role_id == ta_role.role_id:
			form = ManualAttendForm()
			form.manual.choices = [(student.stud_id,student.stud_id) for student in db.session.query(stud_courses).filter_by(course_id=request.args.get('CID'))]
			already = db.session.query(stud_courses).join(Attendance,Attendance.course_id == stud_courses.c.course_id).filter_by(course_id=request.args.get('CID'),timestamp=datetime.today().strftime('%Y-%m-%d'))
			form.manual.data = [r.stud_id for r in already]
			course = Course.query.filter_by(Course_ID=request.args.get('CID')).first()
			course.Classes_held = course.Classes_held + 1
			if form.validate_on_submit():
				recr = form.manual.data
				for stu in recr:
					stud = User.query.filter_by(username=stu,role_id=stud_role.role_id) 
					if stud and stud.count() != 0:
						c1 = db.session.query(stud_courses).filter_by(stud_id=stu,course_id = request.args.get('CID'))
						if c1 and c1.count() != 0:
							check = Attendance.query.filter_by(course_id=request.args.get('CID'),student_id=stu,timestamp=datetime.today().strftime('%Y-%m-%d')) 
							if not check or check.count() == 0:
								atdrecord = Attendance(course_id=request.args.get('CID'),student_id=stu,timestamp=datetime.today().strftime('%Y-%m-%d'),TA_id = current_user.username)
								db.session.add(atdrecord)
								db.session.commit()
								db.session.close()

				flash("Attendance marked")
				return redirect(url_for('log_sysbp.home'))
			return render_template('form_entry.html',title='Manual marking',form=form)

		else:
			flash('Not allowed')
			return redirect(url_for('log_sysbp.home'))
		return render_template('form_entry.html',title='Manual marking',form=form)
	else:
		flash('Login please')
		return redirect(url_for('log_sysbp.login'))