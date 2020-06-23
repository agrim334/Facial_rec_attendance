from app import db,login
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from time import time
import jwt

@login.user_loader
def load_user(username):
	return User.query.get(username)

stud_courses = 	db.Table('stud_courses',
				db.Column('stud_id',db.String(64),db.ForeignKey('user.username',onupdate="CASCADE",ondelete="CASCADE")),
				db.Column('course_id',db.String(64),db.ForeignKey('course.Course_ID',onupdate="CASCADE",ondelete="CASCADE"))
				)

ta_courses = db.Table('ta_courses',
			db.Column('ta_id',db.String(64),db.ForeignKey('user.username',onupdate="CASCADE",ondelete="CASCADE")),
			db.Column('course_id',db.String(64),db.ForeignKey('course.Course_ID',onupdate="CASCADE",ondelete="CASCADE"))
			)

prof_courses = db.Table('prof_courses',
			db.Column('prof_id',db.String(64),db.ForeignKey('user.username',onupdate="CASCADE",ondelete="CASCADE")),
			db.Column('course_id',db.String(64),db.ForeignKey('course.Course_ID',onupdate="CASCADE",ondelete="CASCADE"))
			)

class Role(db.Model):
	role_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	role = db.Column(db.String(20))
	users_role = db.relationship('User', backref='role')
	def to_json(self):
		return dict(id = self.role_id,
					role = self.role,
					users_role=[user.to_json() for user in self.users_role])

class Department(db.Model):
	Dept_ID = db.Column(db.Integer, primary_key=True,autoincrement=True)
	Dept_name = db.Column(db.String(64))
	users_dept = db.relationship('User', backref='udept')
	courses_dept = db.relationship('Course', backref='cdept')
	def to_json(self):
		return dict(id = self.Dept_ID,
					name = self.Dept_name,
					users_dept=[user.to_json() for user in self.users_dept],
					courses_dept=[course.to_json() for course in self.courses_dept],
					)
	def from_json(json_data):
		Dept_ID = json_data.get('Dept_ID')
		Dept_name = json_data.get('Dept_name')
		if Dept_ID and Dept_name:
			return Department(Dept_ID=Dept_ID,Dept_name=Dept_name)
		else:
			pass


class Course(db.Model):
	Course_ID = db.Column(db.String(64), primary_key=True)
	Course_name = db.Column(db.String(64))
	Classes_held = db.Column(db.Integer,default=0)
	dept_id = db.Column(db.Integer, db.ForeignKey('department.Dept_ID',onupdate="CASCADE",ondelete="CASCADE"))
	def to_json(self):
		return dict(id = self.Course_ID,
					name = self.Course_name,
					count = self.Classes_held,
					dept_id = self.dept_id,
					)
	def from_json(json_data):
		Course_ID = json_data.get('Course_ID')
		Course_name = json_data.get('Course_name')
		dept_id = json_data.get('dept_id')
		if dept_id and Course_ID and Course_name:
			return Course(dept_id=dept_id,Course_ID=Course_ID,Course_name=Course_name)
		else:
			pass


class User(UserMixin,db.Model):
	username = db.Column(db.String(64), index=True, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	fname = db.Column(db.String(64), index=True)
	lname = db.Column(db.String(64), index=True)
	password_hash = db.Column(db.String(128))
	dept = db.Column(db.Integer,db.ForeignKey('department.Dept_ID'))
	role_id = db.Column(db.Integer, db.ForeignKey('role.role_id',onupdate="CASCADE",ondelete="CASCADE"))

	facult = db.relationship('Course',
			secondary=prof_courses,
			primaryjoin = (prof_courses.c.prof_id == username & role_id ==  Role.query.filter_by(role ='Faculty').first().role_id),
			secondaryjoin = (prof_courses.c.course_id == Course.Course_ID),
			backref = db.backref('appointed_faculty',lazy='dynamic'),
			lazy = 'dynamic') 

	tutoring = db.relationship('Course',
			secondary=ta_courses,
			primaryjoin = (ta_courses.c.ta_id == username & role_id ==  Role.query.filter_by(role ='TA').first().role_id),
			secondaryjoin = (ta_courses.c.course_id == Course.Course_ID),
			backref = db.backref('tutored_by',lazy='dynamic'),
			lazy = 'dynamic') 

	opted = db.relationship('Course',
			secondary=stud_courses,
			primaryjoin = (stud_courses.c.stud_id == username & role_id == Role.query.filter_by(role ='Student').first().role_id),
			secondaryjoin = (stud_courses.c.course_id == Course.Course_ID),
			backref = db.backref('studied_by',lazy='dynamic'),
			lazy = 'dynamic')
	
	def to_json(self):
		user_obj =  { 'username' : self.username,
					'email' : self.email,
					'fname' : self.fname,
					'lname' : self.lname,
					'dept' : self.dept,
					'role' : self.role_id,
					'prof_course' : [course.to_json() for course in self.facult],
					'TA_course' : [course.to_json() for course in self.tutoring],
					'stud_course' : [course.to_json() for course in self.opted]
					}
		return user_obj

	def from_json(json_data):
		username = json_data.get('userid')
		email = json_data.get('email')
		fname = json_data.get('fname')
		lname = json_data.get('lname')		
		dept = json_data.get('deptc')
		print(dept)
		if username and email and fname and lname and dept:
			return User(username=username,email=email,fname=fname,lname=lname,dept=dept)
		else:
			pass

	def __repr__(self):
		return '<User {}>'.format(self.username)    
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode({'reset_password': self.username, 'exp': time() + expires_in},APP.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	def get_id(self):
			return self.username
	def is_active(self):
			return self.is_active
	def activate_user(self):
			self.is_active = True         
	def get_username(self):
			return self.username
	def get_urole(self):
			return self.role

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, APP.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

class Attendance(db.Model):													#attendance records
	course_id = db.Column(db.String(64),db.ForeignKey('stud_courses.course_id'),primary_key=True)
	student_id = db.Column(db.String(64),db.ForeignKey('stud_courses.stud_id'),primary_key=True)
	timestamp = db.Column(db.Date,primary_key=True)
	faculty_id = db.Column(db.String(64),db.ForeignKey('prof_courses.prof_id'))
	TA_id = db.Column(db.String(64),db.ForeignKey('ta_courses.ta_id'))

	def to_json(self):
		return dict(cid = self.course_id,
					stud_id = self.student_id,
					prof_id = self.faculty_id,
					ta_id = self.TA_id,
					time = self.timestamp)
	def from_json(json_data):
		course_ID = json_data.get('course_ID')
		student_id = json_data.get('student_id')
		TA_id = json_data.get('TA_id')
		timestamp = json_data.get('timestamp')
		faculty_id = json_data.get('faculty_id')
		if TA_ID and course_ID and timestamp and faculty_id and student_id:
			return Attendance(faculty_id=faculty_id,TA_id=TA_id,dept_id=dept_id,course_ID=course_ID,student_id=student_id)
		else:
			pass
