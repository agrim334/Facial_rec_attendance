from app import db,login,APP
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from time import time
import jwt

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

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


class Prof(UserMixin,db.Model):
	prof_id = db.Column(db.String(20), primary_key=True)
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

class TA(UserMixin,db.Model):
	TA_id = db.Column(db.String(20), primary_key=True)
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

class Courses(db.Model):
	Course_ID = db.Column(db.Integer, primary_key=True)
	Course_name = db.Column(db.String(64))

'''class Attendance(db.Model):
	#Course_ID = db.Column(db.Integer, primary_key=True)
	#Stud_ID = db.Column(db.Integer, primary_key=True)
	Classes_held = db.Column(db.Integer)
	Classes_attended = db.Column(db.Integer)
class TA_Prof(db.Model):
	Course_ID = db.Column(db.Integer, primary_key=True)
	Course_name = db.Column(db.String(64))

class TA_Courses(db.Model):
	Course_ID = db.Column(db.Integer, primary_key=True)
	Course_name = db.Column(db.String(64))

class Prof_Courses(db.Model):
	Course_ID = db.Column(db.Integer, primary_key=True)
	Course_name = db.Column(db.String(64))
'''