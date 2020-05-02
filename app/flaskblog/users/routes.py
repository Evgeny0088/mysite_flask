from flask import request, render_template, url_for, redirect, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from flaskblog import db, bcrypt
from flaskblog.users.utils import save_picture, send_reset_password
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email = form.email.data, password = hashed_pass)
		db.session.add(user)
		db.session.commit()
		flash('Account created for {}!'.format(user.username), 'success')
		return redirect(url_for('users.login'))
	else:
		flash(f'User already exist!', 'danger')
	return render_template('register.html',title='Register',form=form)

@users.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			next_page = request.args.get('next')
			flash(f'{form.email.data} is login!','success')
			return redirect(next_page) if next_page else redirect(url_for('main.index'))
		else:
			flash('Unsuccessful login! Please check your data','danger')
	return render_template('login.html',title='Login',form=form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@users.route('/account', methods=['GET','POST'])
@login_required
def account():
	form=UpdateAccountForm()
	if request.method=='POST':
		if form.validate_on_submit():
			if form.picture.data:
				picture_fn = save_picture(form.picture.data)
				current_user.image_file = picture_fn
			current_user.username = form.username.data
			current_user.email = form.email.data
			db.session.commit()
			flash(f'{current_user.username} is updated!', 'success')
			return redirect(url_for('users.account'))
	elif request.method =='GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='image_folder/' + current_user.image_file)
	return render_template('account.html', title = 'Account',form = form, image_file = image_file)

@users.route("/user/<string:username>")
def user_posts(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', default = 1, type = int)
	posts = Post.query.filter_by(autor=user).order_by(Post.created.desc()).paginate(per_page=5,page=page)
	return render_template('user_posts.html', title = 'User posts', posts = posts, user = user)

@users.route("/reset_password", methods = ['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		send_reset_password(user)
		flash('An email has been send on you adress with instructions!', 'success')
	return render_template('reset_request.html', title = 'Reset request', form = form)

@users.route("/reset_passord/<token>", methods = ['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('Your temporary token is invalid or expired!', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pass
		db.session.commit()
		flash('Password has been updated for {}, you can log in!'.format(user.username), 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title = 'Reset Password', form = form)