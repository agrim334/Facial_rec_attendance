from app import db,login,APP
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from time import time
import jwt

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

'''@loginstud.user_loader
def load_stud(stud_id):
	return Student.query.get(int(stud_id))

@loginTA.user_loader
def load_TA(TA_id):
	return TA.query.get(int(TA_id))

@loginprof.user_loader
def load_prof(prof_id):
	return Prof.query.get(int(prof_id))'''


class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	fname = db.Column(db.String(64), index=True)
	lname = db.Column(db.String(64), index=True)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<User {}>'.format(self.username)    
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},APP.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, APP.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

class Student(UserMixin,db.Model):
	stud_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	fname = db.Column(db.String(64), index=True)
	lname = db.Column(db.String(64), index=True)
	year = db.Column(db.String(64), index=True)
	Dept = db.Column(db.String(20), index=True)
	email = db.Column(db.String(120), index=True, unique=True)

	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<Student ' +  str(fname) + ' '+ str(lname)  + ' SID' + str(stud_id) + 'Year' + str(year) + 'Department ' + str(Dept)+ ' >'   
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},APP.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, APP.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
		except:
			return
		return Student.query.get(stud_id)


class TA(UserMixin,db.Model):
	TA_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	fname = db.Column(db.String(64), index=True)
	lname = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	Dept = db.Column(db.String(20), index= True)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<Professor ' +  str(fname) + ' '+ str(lname)  + 'Department ' + str(Dept)+ ' >'   
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},APP.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, APP.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
		except:
			return
		return Prof.query.get(prof_id)

class Course(db.Model):
	Course_ID = db.Column(db.Integer, primary_key=True)
	Course_name = db.Column(db.String(64))
	Classes_held = db.Column(db.DateTime)

class Prof(UserMixin,db.Model):
	prof_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	fname = db.Column(db.String(64), index=True)
	lname = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	Dept = db.Column(db.String(20), index= True)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<Professor ' +  str(fname) + ' '+ str(lname)  + 'Department ' + str(Dept)+ ' >'   
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},APP.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, APP.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
		except:
			return
		return Prof.query.get(prof_id)

class Attendance(db.Model):
	record_id = db.Column('Attd_ID',db.Integer,primary_key=True)
#	course_id = db.Column('Course_ID',db.Integer,db.ForeignKey('stud_courses.course_id'))
#	student_id = db.Column('Stud_ID',db.Integer,db.ForeignKey('stud_courses.stud_id'))
	status = db.Column('Present',db.String)
	timestamp = db.Column(db.DateTime,index = True)
#	faculty_id = db.Column('Faculty',db.Integer,db.ForeignKey('prof_courses.prof_id'))
#	TA_id = db.Column('TA',db.Integer,db.ForeignKey('assist_courses.TA_id'))
	
'''stud_courses = 	db.Table('stud_courses',
				db.Column('stud_id',db.Integer,db.ForeignKey('student.stud_id')),
				db.Column('course_id',db.Integer,db.ForeignKey('course.Course_ID'))
				)

ta_courses = db.Table('ta_courses',
			 db.Column('ta_id',db.Integer,db.ForeignKey('TA.TA_id')),
			 db.Column('course_id',db.Integer,db.ForeignKey('course.Course_ID'))
			 )
'''
'''opted = db.relationship('Course',
			secondary=stud_courses,
			primaryjoin = (stud_courses.c.stud_id == stud_id),
			backref = db.backref('studied_by',lazy='dynamic'),
			lazy = 'dynamic') '''
'''	tutoring = db.relationship('Course',
			secondary=ta_courses,
			primaryjoin = (ta_courses.c.ta_id == TA_id),
			backref = db.backref('tutored_by',lazy='dynamic'),
			lazy = 'dynamic') '''

'''	tutors = db.relationship('TA',
			secondary=ta_courses,
			primaryjoin = (ta_courses.c.course_id == Course_ID),
			secondaryjoin = (ta_courses.c.ta_id == TA.TA_id),
			backref = db.backref('tutoring',lazy='dynamic'),
			lazy = 'dynamic')

	students = db.relationship('Student',
			secondary = stud_courses,
			primaryjoin = (stud_courses.c.course_id == Course_ID),
			secondaryjoin = (stud_courses.c.stud_id == Student.stud_id),
			backref = db.backref('tutoring',lazy='dynamic'),
			lazy = 'dynamic')'''
