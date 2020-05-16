from app.models import User,Course,Department,Attendance,stud_courses,prof_courses,ta_courses
from app import APP,db
from flask_table import Table, Col
import os

class UserResults(Table):
	username = Col('Username')
	email = Col('Email Id')
	fname = Col('First Name')
	lname = Col('Last Name')
	password_hash = Col('pwd',show=False)
	dept = Col('Department')
	role_id = Col('Role')

class CourseResults(Table):

class MapResults(Table):
