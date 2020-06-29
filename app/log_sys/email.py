from flask_mail import Message
from flask import render_template,current_app
from app import mail
from threading import Thread


def send_password_reset_email(user,email):
	token = user.get_reset_password_token()
	url = str(current_app.config['FRONTEND_URL']) + str(token)
	send_email('Reset Your Password',
				sender=current_app._get_current_object().config['ADMINS'][0],
				recipients=[email],
				text_body=render_template('reset_password.txt',url=url,user=user),
				html_body=render_template('reset_password.html',url=url,user=user))

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()