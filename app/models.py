from app import db,login,APP
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from time import time
import jwt

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

stud_courses = 	db.Table('stud_courses',
				db.Column('stud_id',db.Integer,db.ForeignKey('user.id')),
				db.Column('course_id',db.Integer,db.ForeignKey('course.Course_ID'))
				)

ta_courses = db.Table('ta_courses',
			 db.Column('ta_id',db.Integer,db.ForeignKey('user.id')),
			 db.Column('course_id',db.Integer,db.ForeignKey('course.Course_ID'))
			 )


prof_courses = db.Table('prof_courses',
			 db.Column('prof_id',db.Integer,db.ForeignKey('user.id')),
			 db.Column('course_id',db.Integer,db.ForeignKey('course.Course_ID'))
			 )

class Course(db.Model):
	Course_ID = db.Column(db.Integer, primary_key=True)
	Course_name = db.Column(db.String(64))
	Classes_held = db.Column(db.DateTime)

class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	fname = db.Column(db.String(64), index=True)
	lname = db.Column(db.String(64), index=True)
	password_hash = db.Column(db.String(128))
	dept = db.Column(db.String(20), index=True)
	role = db.Column(db.String(20))

	facult = db.relationship('Course',
			secondary=prof_courses,
			primaryjoin = (prof_courses.c.prof_id == id & role == 'Faculty'),
			secondaryjoin = (prof_courses.c.course_id == Course.Course_ID),
			backref = db.backref('appointed_faculty',lazy='dynamic'),
			lazy = 'dynamic') 

	tutoring = db.relationship('Course',
			secondary=ta_courses,
			primaryjoin = (ta_courses.c.ta_id == id & role == 'TA'),
			secondaryjoin = (ta_courses.c.course_id == Course.Course_ID),
			backref = db.backref('tutored_by',lazy='dynamic'),
			lazy = 'dynamic') 

	opted = db.relationship('Course',
			secondary=stud_courses,
			primaryjoin = (stud_courses.c.stud_id == id & role == 'Student'),
			secondaryjoin = (stud_courses.c.course_id == Course.Course_ID),
			backref = db.backref('studied_by',lazy='dynamic'),
			lazy = 'dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)    
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},APP.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	def get_id(self):
			return self.id
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

class Attendance(db.Model):
	course_id = db.Column('Course_ID',db.Integer,db.ForeignKey('stud_courses.course_id'),primary_key=True)
	student_id = db.Column('Stud_ID',db.Integer,db.ForeignKey('stud_courses.stud_id'),primary_key=True)
	status = db.Column('Present',db.String(4))
	timestamp = db.Column(db.Date,primary_key=True)
	faculty_id = db.Column('Faculty',db.Integer,db.ForeignKey('prof_courses.prof_id'))
	TA_id = db.Column('TA',db.Integer,db.ForeignKey('ta_courses.ta_id'))