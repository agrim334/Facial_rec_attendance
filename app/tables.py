from app.models import User,Course,Department,Attendance,stud_courses,prof_courses,ta_courses
from app import db
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
	Course_ID = Col('Course ID')
	Course_name = Col('Course Name')
	Classes_held = Col('Classes Held')
	dept_id = Col('Department')

class MapResults(Table):
	user = Col('User')
	course = Col('Course')

class AttendanceResults(Table):
	course_id = Col('Course')
	student_id = Col('Student')
	timestamp = Col('Time')
	faculty_id = Col('Faculty')
	TA_id = Col('TA')

class DeptTable(Table):
	Dept_ID = Col('Dept ID')
	Dept_name = Col('Name')	