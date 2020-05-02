import os
import secrets
from PIL import Image
from flask_mail import Message
from flaskblog import mail
from flask import url_for, current_app

def save_picture(form_picture):
	if os.path.dirname(form_picture.filename) == os.path.join(current_app.root_path,'static/image_folder'):
		form_picture.save(form_picture.filename)
		return form_picture
	else:
		random = secrets.token_hex(8)
		_,f_ext = os.path.splitext(form_picture.filename)
		picture_random = random + f_ext
		picture_path = os.path.join(current_app.root_path,'static/image_folder/',picture_random)
		output_size = (125,125)
		i = Image.open(form_picture)
		i.thumbnail(output_size)
		i.save(picture_path)
		return picture_random

def send_reset_password(user):
	token = user.get_reset_token()
	msg = Message('Password reset request', sender = 'noreply@demo.com', recipients = [user.email])
	msg.body = f'''To reset your password please visit link below:
	{url_for('users.reset_token', token = token, _external = True)}
	If you did not make this request, just simply ignore this email and no change! 
	'''
	mail.send(msg)