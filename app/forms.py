from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms import StringField, PasswordField, BooleanField, SubmitField,RadioField,FileField,SelectMultipleField,widgets
from wtforms.validators import ValidationError,DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import User,Course,Department,Attendance,stud_courses,prof_courses,ta_courses
from app import APP,db
import os

basedir = os.path.abspath(os.path.dirname(__file__))
APP.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')
photos = UploadSet('photos', IMAGES)
configure_uploads(APP, photos)
patch_request_class(APP)

class DeptForm(FlaskForm):												#add new departments
	depart = StringField('Department Name', validators=[DataRequired()])
	submit = SubmitField('Upload')

class CheckAttendanceForm(FlaskForm):											# form for checking attendance
	courseID = StringField("Course ID",validators=[DataRequired()])
	submit = SubmitField('Submit')

class AttendForm(FlaskForm):														#attendance form using facial recognition
	CID = StringField('Course ID', validators=[DataRequired()])
	photo = FileField(render_kw={'multiple':True},validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
	submit = SubmitField('Upload')

class ManualAttendForm(FlaskForm):												#for manual entries if facial recognition does not work or some error occurs
	manual = SelectMultipleField('Remaining Students',widget = widgets.ListWidget(prefix_label=False),option_widget = widgets.CheckboxInput())
	submit = SubmitField('Upload')

class CourseUserForm(FlaskForm):											#Map courses and users
	CID = StringField('CourseID', validators=[DataRequired()])
	user = StringField('UserID',validators=[DataRequired()])
	role = RadioField('Role', coerce=int)
	photo = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
	submit = SubmitField('Upload')

class CourseForm(FlaskForm):
	CID = StringField('CourseID', validators=[DataRequired()])								#add new course
	Cname = StringField('Course Name', validators=[DataRequired()])
	submit = SubmitField('Upload')

class ViewUserForm(FlaskForm):
	criteria = RadioField('Method',choices=[('1','By Department'),('2','By Role'),('3','By User ID'),('4','Display All')])
	match = StringField('Filter', validators=[DataRequired()])
	submit = SubmitField('Upload')

class ViewCourseForm(FlaskForm):
	criteria = RadioField('Method',choices=[('1','By Department'),('2','By Course ID'),('3','Display All')])
	match = StringField('Filter', validators=[DataRequired()])
	submit = SubmitField('Upload')

class ViewDeptForm(FlaskForm):
	criteria = RadioField('Method',choices=[('1','Display All'),('2','Search')])
	match = StringField('Filter')
	submit = SubmitField('Upload')

class LoginForm(FlaskForm):															#user login form
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	role = RadioField('Role',coerce=int)
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):															#add new users
	username = StringField('Username', validators=[DataRequired()])
	fname =	StringField('First name', validators=[DataRequired()])
	lname = StringField('Last name', validators=[DataRequired()])
	dept = RadioField('Department',coerce=int)
	email = StringField('Email', validators=[DataRequired(), Email()])
	role = RadioField('Role', coerce=int)
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		if username.data != self.username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Request Password Reset')

class ChangePWDForm(FlaskForm):
	currentpassword = PasswordField('Old Password', validators=[DataRequired()])
	newpassword = PasswordField('New Password', validators=[DataRequired()])
	newpassword2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('newpassword')])
	submit = SubmitField('Change Password')

class EditProfileForm(FlaskForm):									#basic profile editing
	fname =	StringField('First name', validators=[DataRequired()])
	lname = StringField('Last name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Submit')
	
	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')
