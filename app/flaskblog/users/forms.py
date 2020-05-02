from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),
						Length(min=2, max=20)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm_password',
						validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign up')

	def __init__(self, *args, **kwargs):
		super(RegistrationForm,self).__init__(*args, **kwargs)
		self.validate_username(self.username)
		self.validate_email(self.email)

	def validate_username(self, username):
		user = User.query.filter(User.username == username.data).first()
		if user:
			raise ValidationError(f'{user.username} already exist!')

	def validate_email(self, email):
		user = User.query.filter(User.email == email.data).first()
		if user:
			raise ValidationError(f'{user.email} already exist!')

class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),
						Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),
						Length(min=2, max=20)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	picture = FileField('Profile picture', validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Update')

	def __init__(self, *args, **kwargs):
		super(UpdateAccountForm,self).__init__(*args, **kwargs)
		self.validate_username(self.username)
		self.validate_email(self.email)

	def validate_username(self, username):
		if username.data!=current_user.username:
			user = User.query.filter(User.username == username.data).first()
			if user:
				raise ValidationError(f'{user.username} already exist!')

	def validate_email(self, email):
		if email.data!=current_user.email:
			user = User.query.filter(User.email == email.data).first()
			if user:
				raise ValidationError(f'{user.email} already exist!')

class RequestResetForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	submit = SubmitField('Request password reset')

	def verify_email(self,email):
		user = User.query.filter_by(email = self.email.data).first()
		if user is None:
			raise ValidationError('User does not exist, you must register first!')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm_password',
						validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Reset password')