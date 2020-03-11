from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms import StringField, PasswordField, BooleanField, SubmitField,RadioField,FileField
from wtforms.validators import ValidationError,DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import User
from app import APP
import os

basedir = os.path.abspath(os.path.dirname(__file__))
APP.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')
photos = UploadSet('photos', IMAGES)
configure_uploads(APP, photos)
patch_request_class(APP)

class AttendForm(FlaskForm):
	CID = StringField('Course ID', validators=[DataRequired()])
	photo = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
	submit = SubmitField('Upload')

class CourseUserForm(FlaskForm):
	CID = StringField('CourseID', validators=[DataRequired()])
	User = StringField('UserID',validators=[DataRequired()])
	Role = StringField('Role',validators=[DataRequired()])
class CourseForm(FlaskForm):
	CID = StringField('CourseID', validators=[DataRequired()])
	Cname = StringField('Course Name', validators=[DataRequired()])
	Faculty = StringField('Faculty',validators=[DataRequired()])

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	role = RadioField('Role',choices=[('Student','Student'),('Faculty','Faculty'),('TA','TA'),('Admin','Admin')])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	fname =	StringField('First name', validators=[DataRequired()])
	lname = StringField('Last name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	dept = StringField('Department', validators=[DataRequired()])
	role = RadioField('Role',choices=[('Student','Student'),('Faculty','Faculty'),('TA','TA'),('Admin','Admin')] )
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField(
		'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		if username.data != self.original_username:
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

class EditProfileForm(FlaskForm):
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

class CheckAttendanceForm(FlaskForm):
	courseID = StringField("Course ID",validators=[DataRequired()])
	submit = SubmitField('Submit')
