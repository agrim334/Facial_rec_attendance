from app import APP,db,errors
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for,session
from app.forms import DeptForm,ManualAttendForm,CheckAttendanceForm,CourseForm,LoginForm,RegistrationForm,ResetPasswordRequestForm,ResetPasswordForm,EditProfileForm,ChangePWDForm,AttendForm,CourseUserForm
import face_recognition
import os
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user,logout_user,login_required
from app.models import User,Course,Attendance,ta_courses,prof_courses,stud_courses,Department
from app.email import send_password_reset_email
import numpy as np
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from datetime import datetime,timedelta
import re

basedir = os.path.abspath(os.path.dirname(__file__))
APP.config['UPLOAD_PATH'] = os.path.join(basedir, 'uploads')
photos = UploadSet('photos', IMAGES)
configure_uploads(APP, photos)
patch_request_class(APP)

@APP.before_request
def make_session_permanent():
	session.permanent = True
	APP.permanent_session_lifetime = timedelta(minutes=10)

@APP.after_request
def after_request(response):									#security
	response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-XSS-Protection'] = '1; mode=block'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response

@APP.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@APP.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

@APP.route('/')
@login_required
def home():													#home page url
	return render_template('home.html', title='Home',user = user)

@APP.route('/login',methods={'GET','POST'})
def login():										#login page url
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data,role=form.role.data).first()  #check if credentials valid
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		
		if not next_page or url_parse(next_page).netloc != '':							#redirect to home
			next_page = url_for('home',user = user)

		return redirect(next_page)

	return render_template('login.html', title='Sign In', form=form)

@APP.route('/course_user',methods=['GET','POST'])
@login_required
def course_user_add():														#map course to user url
	if current_user.is_authenticated:
		if current_user.role == "Admin":										
			form = CourseUserForm()
			if form.validate_on_submit():
				course = Course.query.filter(Course.Course_ID == form.CID.data) 
				if not course:
					flash('This course was not found in Database.Please add this course to database and then try or enter correct course id.')
					return redirect(url_for('course_user_add'))
				user = User.query.filter_by(username=form.user.data,role=form.role.data).first()
				if not user:
					flash('No such TA or Faculty found')
					return redirect(url_for('course_user_add'))
				if form.role.data == 'Faculty':
					statement = prof_courses.insert().values(prof_id=form.user.data,course_id=form.CID.data)
				elif form.role.data == 'TA':
					statement = ta_courses.insert().values(ta_id=form.user.data,course_id=form.CID.data)					#TA prof mapped to course
				elif form.role.data == 'Student':
					statement = stud_courses.insert().values(stud_id=form.user.data,course_id=form.CID.data)			#for students save mapping + image corresponding to course
					known_dir = "/home/agrim/Downloads/known/" + str(form.CID.data) +"/"								#set known dir to your required location
					if not os.path.exists(known_dir):
						os.makedirs(known_dir)
					file = request.files.getlist("photo")
					for f in file:
						filename = secure_filename(f.filename)
						f.save(os.path.join(known_dir, filename))
						ofilename, ofile_extension = os.path.splitext(os.path.join(known_dir, filename))		#save images renaming them appropriately
						nf = form.user.data + ofile_extension
						os.rename(os.path.join(known_dir, filename),os.path.join(known_dir, nf))
				else:
					flash("Not allowed for this role")
					return redirect(url_for('course_user_add'))
				db.session.execute(statement)
				db.session.commit()
				db.session.close()
				flash('Mapping has been added')
				return redirect(url_for('course_user_add'))
			return render_template('course_user.html', title='Course_user', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('home'))
	else:
		flash('Login please!!')
		return redirect(url_for('login'))

@APP.route('/course',methods=['GET','POST'])
@login_required
def course_add():
	if current_user.is_authenticated:
		if current_user.role == "Admin":
			form = CourseForm()
			if form.validate_on_submit():
				course = Course(Course_ID=form.CID.data, Course_name=form.Cname.data)       #add new course and correspondingly directory for students attending the course
				known_dir = "/home/agrim/Downloads/known/" + str(form.CID.data) +"/"
				if not os.path.exists(known_dir):
					os.makedirs(known_dir)
				db.session.add(course)
				db.session.commit()
				db.session.close()
				flash('Course has been added')
				return redirect(url_for('home'))
			return render_template('course.html', title='Course', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('home'))
	else:
		flash('Login please!!')
		return redirect(url_for('login'))

@APP.route('/register',methods=['GET','POST'])
@login_required
def register():
	if current_user.is_authenticated:
		if current_user.role == "Admin":
			form = RegistrationForm()
			if form.validate_on_submit():
				user = User(username=form.username.data, fname=form.fname.data, lname=form.lname.data,email=form.email.data,role=form.role.data,dept=int(form.dept.data))
				user.set_password(form.password.data)
				db.session.add(user)
				db.session.commit()
				db.session.close()
				flash('User has been added')
				return redirect(url_for('register'))
			return render_template('register.html', title='Register', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('home'))
	else:
		flash('Login please!!')
		return redirect(url_for('login'))

@APP.route('/dept_add',methods=['GET','POST'])
@login_required
def add_dept():
	if current_user.is_authenticated:
		if current_user.role == "Admin":
			form = DeptForm()
			if form.validate_on_submit():
				dept = Department(Dept_name = form.depart.data)
				db.session.add(dept)
				db.session.commit()
				db.session.close()
				flash('Department has been added')
				return redirect(url_for('add_dept'))
			return render_template('dept.html', title='Add Department', form=form)
		else:
			flash('Only admins can access this page')
			return redirect(url_for('home'))
	else:
		flash('Login please!!')
		return redirect(url_for('login'))

@APP.route('/dept_view',methods=['GET','POST'])
@login_required
def view_dept():
	if current_user.is_authenticated:
		columns = []
		records = []
		dept = Department.query.all()
		if dept:
			columns = Department.__table__.columns.keys()
			for r in dept:
				records.append(r)
		else:
			flash("No Departments Found")
			return redirect(url_for('home'))
		return render_template('view_dept.html',columns=columns,items=records)
	else:
		flash('Login please')
		return redirect(url_for('login'))

@APP.route('/user/<username>')
@login_required
def user(username):
	if current_user.is_authenticated:
		user = User.query.filter_by(username=username).first_or_404()
		if user:
			if current_user.username == username:
				return render_template('user.html', user=user)
			else:
				flash('Not allowed')
				return redirect('home')
	else:
		flash('login please')
		return redirect(url_for('login'))

@APP.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	if current_user.is_authenticated:
		form = EditProfileForm(current_user)
		if form.validate_on_submit():
			current_user.email = form.email.data
			current_user.fname = form.fname.data
			current_user.lname = form.lname.data
			db.session.commit()
			flash('Your changes have been saved.')
			return redirect(url_for('edit_profile'))

		elif request.method == 'GET':
			form.email.data = current_user.email
			form.fname.data = current_user.fname
			form.lname.data = current_user.lname
		return render_template('edit_profile.html', title='Edit Profile',form=form)	
	else:
		flash('login please')
		return redirect(url_for('login'))

@APP.route('/change_password', methods=['GET','POST'])
@login_required
def change_password():
	if current_user.is_authenticated:
		form = ChangePWDForm()
		if request.method == 'POST':
			if form.validate_on_submit(): 
				if current_user.check_password(form.currentpassword.data):
					current_user.set_password(form.newpassword.data)
					db.session.commit()
					flash('Your changes have been saved.')
					return redirect(url_for('home'))
				else :
					flash('Old password incorrect')
					return redirect(url_for('change_password'))
		return render_template('change_password.html', title='Change Password',form=form)	
	else:
		flash('login please')
		return redirect(url_for('login'))

@APP.route('/logout')
def logout():
	if not current_user.is_anonymous:
		logout_user()
		flash('You have logged out')
	else:
		flash('Error.Not logged in')
	return redirect(url_for('login'))

@APP.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data) 
		if user:
			send_password_reset_email(user,user.email)
			flash('Check your email for the instructions to reset your password')
			return redirect(url_for('login'))
		else:
			flash('Error could not send email as User not registered or no email entered for this user')
			return redirect(url_for('reset_password_request'))

	return render_template('reset_password_request.html',title='Reset Password', form=form)

@APP.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user = User.verify_reset_password_token(token)
	if not user:
		flash('Time expired.')
		return redirect(url_for('home'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset.')
		return redirect(url_for('login'))
	return render_template('reset_password.html', form=form)

@APP.route('/check_attendance',methods=['GET','POST'])
@login_required
def checkattd():
	if current_user.is_authenticated:
		if current_user.role == "Student":
			form =CheckAttendanceForm()
			columns = []
			records = []
			if form.validate_on_submit():
				CID = form.courseID.data
				course = Course.query.filter_by(Course_ID=CID) 
				count = 0
				if course and course.count() != 0:
					count = course.Classes_held
					is_stud = db.session.query(stud_courses).filter_by(stud_id=current_user.username,course_id = CID)
					if is_stud and is_stud.count() != 0:
						attd = Attendance.query.filter_by(course_id=CID,student_id=current_user.username)
						if not attd:
							flash('Incorrect course code')
							return redirect(url_for('checkattd'))
						else:
							columns = Attendance.__table__.columns.keys()
							for r in attd:
								records.append(r)
					else:
						flash("Student not registered for this course")
						return redirect(url_for('checkattd'))
				else:
					flash('No such course')
					return redirect(url_for('checkattd'))
				return render_template('check_attendance.html',form=form,columns=columns,items=records,class_count=count)
		else:
			flash('Not allowed')
			return redirect(url_for('home'))
	else:
		flash('Login please')
		return redirect(url_for('login'))
	return render_template('check_attendance.html',form=form,columns=columns,items=records)

@APP.route('/view_courses',methods=['GET','POST'])
@login_required
def courses():
	if current_user.is_authenticated:
		columns = []
		records = []
		courses = Course.query.all()
		if courses and courses.count() != 0:
			columns = Course.__table__.columns.keys()
			for r in courses:
				records.append(r)
		else:
			flash("No Courses Found")
			return redirect(url_for('home'))
		return render_template('view.html',columns=columns,items=records)
	else:
		flash('Login please')
		return redirect(url_for('login'))
	return render_template('view.html',columns=columns,items=records)

@APP.route('/view_users',methods=['GET','POST'])
@login_required
def users():
	if current_user.is_authenticated:
		columns = []
		records = []
		if current_user.role == "Admin":
			user = User.query.all()
			if user and user.count() != 0:
				columns = User.__table__.columns.keys()
				columns.remove('password_hash')
				for r in user:
					records.append(r)
			else:
				flash("No Users Found")
				return redirect(url_for('home'))
			return render_template('view_user.html',columns=columns,items=records)
		else:
			flash('Not allowed')
			return redirect(url_for('home'))
	else:
		flash('Login please')
		return redirect(url_for('login'))
	return render_template('view_user.html',form=form,columns=columns,items=records)

def allowed_file(filename):															#set allowed extensions for images
	ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP.route('/faces', methods=['GET', 'POST'])
@login_required
def upload_image():																	#upload images to mark attendance
	if current_user.is_authenticated:
		if current_user.role == "Faculty":
			form = AttendForm()
			if form.validate_on_submit():
				base = os.path.abspath(os.path.dirname(__file__))
				CID = form.CID.data
				course = Course.query.filter_by(Course_ID=CID) 			
				if course and course.count() != 0:
					confirm = db.session.query(prof_courses).filter_by(prof_id=current_user.username,course_id = CID)
					if confirm and confirm.count() != 0:
						file = request.files.getlist("photo")
						for f in file:
							filename = secure_filename(f.filename)
							f.save(os.path.join(APP.config['UPLOAD_PATH'], filename))
						user = User.query.filter_by(username=current_user.username,role='Faculty')
						return detect_faces_in_image(base+"/uploads/",CID,user)

					else:
						flash("No TA or Faculty with given ID found for this course")
						return redirect(url_for('home'))
				else:
					flash("No such Course found")
					return redirect(url_for('home'))

		elif current_user.role == "TA":
			form = AttendForm()
			if form.validate_on_submit():
				base = os.path.abspath(os.path.dirname(__file__))
				CID = form.CID.data
				course = Course.query.filter_by(Course_ID=CID) 			
				if course and course.count() != 0:
					confirm = db.session.query(ta_courses).filter_by(ta_id=current_user.username,course_id = CID)
					if confirm and confirm.count() != 0:
						file = request.files.getlist("photo")
						for f in file:
							filename = secure_filename(f.filename)
							f.save(os.path.join(APP.config['UPLOAD_PATH'], filename))
						user = User.query.filter_by(username=current_user.username,role='TA')
						return detect_faces_in_image(base+"/uploads/",CID,user)

					else:
						flash("No TA or Faculty with given ID found for this course")
						return redirect(url_for('home'))
				else:
					flash("No such Course found")
					return redirect(url_for('home'))
		else:
			flash('Not allowed')
			return redirect(url_for('home'))
		return render_template("face_rec.html",title="Hello",form=form)
	else:
		flash('Login please')
		return redirect(url_for('login'))

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
			inp_face_locations = face_recognition.face_locations(temp, model = "hog")
			encd= face_recognition.face_encodings(temp, known_face_locations = inp_face_locations)[0]
			known_face_encd.append(encd)
			image = pat.match(image)[0]
			image = image[:-1]
			print(image)
			known_face_name[str(encd)] = image

		for file in os.listdir(file_stream):

			un_image = face_recognition.load_image_file(file_stream+file)

			face_locations = face_recognition.face_locations(un_image,model = "hog")

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
						stud = User.query.filter_by(username=name,role="Student") 
						if stud:
							c1 = db.session.query(stud_courses).filter_by(ta_id=stud.username,course_id = CID)
							if c1:
								check = Attendance.query.filter_by(course_id=CID,student_id=stud.username,timestamp=datetime.today().strftime('%Y-%m-%d')) 
								if not check or check.count() == 0:
									if user.role == 'TA':
										atdrecord = Attendance(course_id=CID,student_id=stud.username,timestamp=datetime.today().strftime('%Y-%m-%d'),TA_id = user.username)
									else:
										atdrecord = Attendance(course_id=CID,student_id=stud.username,timestamp=datetime.today().strftime('%Y-%m-%d'),faculty_id = user.username)
									print(atdrecord)
									db.session.add(atdrecord)
									db.session.commit()

		for image in os.listdir(base+"/uploads/"):
			if os.path.isfile(base+"/uploads/"+image):
				os.remove(base+"/uploads/"+image)

		return redirect(url_for('manual_mark',CID=CID))										#redirect to manual attendance to handle missed cases
	except:

		for image in os.listdir(base+"/uploads/"):
			if os.path.isfile(base+"/uploads/"+image):
				os.remove(base+"/uploads/"+image)

		return redirect(url_for('manual_mark',CID=CID))


@APP.route('/manual', methods=['GET', 'POST'])
@login_required
def manual_mark():
	if current_user.is_authenticated:
		if current_user.role == "Faculty":
			form = ManualAttendForm()
			form.manual.choices = [(student.stud_id,student.stud_id) for student in db.session.query(stud_courses).filter_by(course_id=request.args.get('CID'))]
			already = db.session.query(stud_courses).join(Attendance,Attendance.course_id == stud_courses.c.course_id).filter_by(course_id=request.args.get('CID'),timestamp=datetime.today().strftime('%Y-%m-%d'))
			form.manual.data = [r.stud_id for r in already]
			course = Course.query.filter_by(Course_ID=request.args.get('CID')).first()
			course.Classes_held = course.Classes_held + 1
			if form.validate_on_submit():
				recr = form.manual.data
				for stu in recr:
					stud = User.query.filter_by(username=stu,role="Student") 
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
				return redirect(url_for('home'))

			return render_template("manual.html",form=form)

		elif current_user.role == "TA":
			form = ManualAttendForm()
			form.manual.choices = [(student.stud_id,student.stud_id) for student in db.session.query(stud_courses).filter_by(course_id=request.args.get('CID'))]
			already = db.session.query(stud_courses).join(Attendance,Attendance.course_id == stud_courses.c.course_id).filter_by(course_id=request.args.get('CID'),timestamp=datetime.today().strftime('%Y-%m-%d'))
			form.manual.data = [r.stud_id for r in already]
			
			course = Course.query.filter_by(Course_ID=request.args.get('CID')).first()
			course.Classes_held = course.Classes_held + 1
			if form.validate_on_submit():
				recr = form.manual.data
				for stu in recr:
					stud = User.query.filter_by(username=stu,role="Student") 
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
				return redirect(url_for('home'))
			return render_template("manual.html",form=form)

		else:
			flash('Not allowed')
			return redirect(url_for('home'))
		return render_template("manual.html",form=form)
	else:
		flash('Login please')
		return redirect(url_for('login'))