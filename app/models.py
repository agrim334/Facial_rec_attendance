from app import db,login
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from time import time
import jwt
from datetime import datetime

@login.user_loader
def load_user(username):
	return User.query.get(username)

stud_courses = 	db.Table('stud_courses',
				db.Column('SID',db.String(64),db.ForeignKey('user.username',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
				db.Column('CID',db.String(64),db.ForeignKey('course.ID',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True)
				)

ta_courses = db.Table('ta_courses',
			db.Column('TAID',db.String(64),db.ForeignKey('user.username',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
			db.Column('CID',db.String(64),db.ForeignKey('course.ID',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True)
			)

prof_courses = db.Table('prof_courses',
			db.Column('FID',db.String(64),db.ForeignKey('user.username',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
			db.Column('CID',db.String(64),db.ForeignKey('course.ID',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True)
			)
class Permission:
	READ = 0x01
	CUD_ATTD = 0X02
	ADMIN = 0xff

class Role(db.Model):
	ID = db.Column(db.Integer,primary_key=True,autoincrement=True)
	name = db.Column(db.String(20))
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users_name= db.relationship('User', backref='role')
	def to_json(self):
		return	{	'id' : self.ID,
					'name' : self.name,
				}
	@staticmethod
	def insert_roles():
		roles = {	'Student': (Permission.READ,True),
					'TA': (Permission.READ | Permission.CUD_ATTD,False),
					'Prof': (Permission.READ | Permission.CUD_ATTD,False),
					'Admin': (Permission.ADMIN,False)
				}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
				role.permissions = roles[r][0]
			db.session.add(role)
		db.session.commit()

class Department(db.Model):
	ID = db.Column(db.String(64), primary_key=True)
	name = db.Column(db.String(64))
	users_dept = db.relationship('User', backref='udept', cascade="all,delete",)
	courses_dept = db.relationship('Course', backref='cdept', cascade="all,delete",)
	def to_json(self):
		return	{	'id' : self.ID,
					'name' : self.name,
				}
	def from_json(json_data):
		ID = json_data.get('id')
		name = json_data.get('name')
		if ID and name:
			return Department(ID=ID,name=name)
		else:
			pass


class Course(db.Model):
	ID = db.Column(db.String(64), primary_key=True)
	name = db.Column(db.String(64))
	classes_held = db.Column(db.Integer,default=0)
	dept_ID = db.Column(db.String(64), db.ForeignKey('department.ID',onupdate="CASCADE",ondelete="CASCADE"))
	def to_json(self):
		return	{	'id' : self.ID,
					'name' : self.name,
					'classes_held' : self.classes_held,
					'dept_ID' : self.dept_ID,
				}
	def from_json(json_data):
		ID = json_data.get('id')
		name = json_data.get('name')
		dept_ID = json_data.get('dept_id')
		if ID and ID and name:
			return Course(dept_ID=dept_ID,ID=ID,name=name)
		else:
			pass


class User(UserMixin,db.Model):
	username = db.Column(db.String(64), index=True, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	fname = db.Column(db.String(64), index=True)
	lname = db.Column(db.String(64), index=True)
	password_hash = db.Column(db.String(128))
	dept = db.Column(db.String(64),db.ForeignKey('department.ID'))
	role_id = db.Column(db.Integer, db.ForeignKey('role.ID',onupdate="CASCADE",ondelete="CASCADE"))

	facult = db.relationship('Course',
			secondary=prof_courses,
			primaryjoin = (prof_courses.c.FID == username and role_id == Role.query.filter_by(name='Faculty').first().role_id),
			secondaryjoin = (prof_courses.c.CID == Course.ID),
			backref = db.backref('appointed_faculty',lazy='dynamic'),
			lazy = 'dynamic') 

	tutoring = db.relationship('Course',
			secondary=ta_courses,
			primaryjoin = (ta_courses.c.TAID == username and role_id == Role.query.filter_by(name='TA').first().role_id),
			secondaryjoin = (ta_courses.c.CID == Course.ID),
			backref = db.backref('tutored_by',lazy='dynamic'),
			lazy = 'dynamic') 

	opted = db.relationship('Course',
			secondary=stud_courses,
			primaryjoin = (stud_courses.c.SID == username and role_id == Role.query.filter_by(name='Student').first().role_id),
			secondaryjoin = (stud_courses.c.CID == Course.ID),
			backref = db.backref('studied_by',lazy='dynamic'),
			lazy = 'dynamic')

	def to_json(self):
		user_obj =  {'username' : self.username,
					'email' : self.email,
					'fname' : self.fname,
					'lname' : self.lname,
					'dept' : self.dept,
					'role' : self.role_id,
					}
		return user_obj

	def from_json(json_data):
		username = json_data.get('username')
		email = json_data.get('email')
		fname = json_data.get('fname')
		lname = json_data.get('lname')
		dept = json_data.get('deptc')
		role_id = json_data.get('rolec')
		if dept == '':
			dept = None
		return User(username=username,email=email,fname=fname,lname=lname,dept=dept,role_id=role_id)

	def __repr__(self):
		return '<User {}>'.format(self.username)    

	def set_password(self, password):
		self.password_hash = generate_password_hash(password, method='sha256')

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode({'reset_password': self.username, 'exp': time() + expires_in},APP.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	def can(self, permissions):
		return self.role is not None and (self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.can(Permission.ADMINISTER)

	def check_password(self,password):
		return check_password_hash(self.password_hash, password)

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, APP.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(username)

	@classmethod
	def authenticate(self,username,password):
		
		print(password)
		if not username or not password:
			return None

		if username:
			user = User.query.filter_by(username=username).first()

		if not user or not check_password_hash(user.password_hash, password):
			return None

		return user

class Attendance(db.Model):													#attendance records
	CID = db.Column(db.String(64),db.ForeignKey('stud_courses.CID'),primary_key=True)
	SID = db.Column(db.String(64),db.ForeignKey('stud_courses.SID'),primary_key=True)
	timestamp = db.Column(db.Date,primary_key=True)
	FID = db.Column(db.String(64),db.ForeignKey('prof_courses.FID'))
	TAID = db.Column(db.String(64),db.ForeignKey('ta_courses.TAID'))

	def to_json(self):
		return 	{	'cid' : self.CID,
					'sid' : self.SID,
					'fid' : self.FID,
					'taid' : self.TAID,
					'time' : self.timestamp
				}
	def from_json(json_data):
		CID = json_data.get('cid')
		SID = json_data.get('sid')
		TAID = json_data.get('taid')
		timestamp = json_data.get('timestamp')
		FID = json_data.get('fid')
		if TAID and ID and timestamp and FID and SID:
			return Attendance(FID=FID,TAID=TAID,CID=CID,SID=SID,timestamp=timestamp)
		else:
			pass
