import datetime

from flask_wtf import FlaskForm 
from wtforms.fields import SelectField, FloatField, TextAreaField, StringField, PasswordField, FileField, BooleanField, SubmitField, SelectField, DateField, IntegerField, RadioField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

from models import User, Doctor

class DoctorProfileForm(FlaskForm):
	name = StringField('name')
	surname = StringField('surname',)
	gender = SelectField('gender', choices=[('Male', 'Male'), ('Female', 'Female')])
	email = StringField('email')
	achievements = StringField('achievements')
	years_in_practice = IntegerField('Years in service')
	rank = StringField('rank')
	career = TextAreaField('career')
	about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
	photo = FileField('photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])

class DocFeedbackForm(FlaskForm):
	content = TextAreaField('Feedback')
	patient = StringField('Patient Name')

class AssignDocForm(FlaskForm):
	username = StringField('User Name')
	doctor = SelectField('Doctor')

class DiagnosisForm(FlaskForm):
	age = IntegerField('Age')
	sex = SelectField('sex', choices=[('Male', 'Male'), ('Female', 'Female')])
	chestpain = SelectField('Chest Pain Type', choices=[('0','0'),('1','1'),('2','2'),('3','3'),('4','4')])
	electro = IntegerField('electro')
	heartrate = IntegerField('Heart Rate')
	cholesterol = IntegerField('Cholesterol')
	slope = IntegerField('Slope exercise')
	bloodsugar = IntegerField('Blood Sugar')
	bloodpressure = IntegerField('Blood Pressure')
	thal = IntegerField('thal')
	angina = IntegerField('Angina')
	peak = IntegerField('peak')
	vessel = IntegerField('vessels')
	

class FeedbackForm(FlaskForm):
    content = TextAreaField('Feedback')

class AddDocForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired(), Length(1, 120), Email()])

	def validate_email(self, email_field):
		if Doctor.query.filter_by(email=email_field.data).first():
			raise ValidationError('There is already a user with this email address.')

	def validate_username(self, username_field):
		if Doctor.query.filter_by(username=username_field.data).first():
			raise ValidationError('This username is already taken')

class UploadForm(FlaskForm):
    photo = FileField('photo', validators=[FileRequired(), FileAllowed(['jpg','png'], 'Images only')])

class UserProfileForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	surname = StringField('surname', validators=[DataRequired()])
	gender = SelectField('gender', choices=[('Male', 'Male'), ('Female', 'Female')])
	email = StringField('email', validators=[DataRequired()])
	weight = FloatField('weight')
	height = FloatField('height')
	location = StringField('location')
	about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
	photo = FileField('photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])
	password = PasswordField('password')

class AddUserForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired(), Length(1, 120), Email()])
	role = SelectField('role', choices=[('Doctor', 'Doctor'),('Patient','Patient')], validators=[DataRequired()])

	def validate_email(self, email_field):
		if User.query.filter_by(email=email_field.data).first():
			raise ValidationError('There is already a user with this email address.')

	def validate_username(self, username_field):
		if User.query.filter_by(username=username_field.data).first():
			raise ValidationError('This username is already taken')

class LoginForm(FlaskForm):
    username = StringField('Your Username: ', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
	username = StringField('Username',
							validators=[
							DataRequired(), Length(3, 80),
							#Regexp('^[A-Za-z0-9_]{3,}S',
							#	message='Usernames consist of numbers, letters,''and underscores.')
							])
	password = PasswordField('Password',
					validators=[
					DataRequired(),
					EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm Password', validators=[DataRequired()])
	email = StringField('Email',
				validators=[DataRequired(), Length(1, 120), Email()])

	def validate_email(self, email_field):
		if User.query.filter_by(email=email_field.data).first():
			raise ValidationError('There is already a user with this email address.')

	def validate_username(self, username_field):
		if User.query.filter_by(username=username_field.data).first():
			raise ValidationError('This username is already taken')
