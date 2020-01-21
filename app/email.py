from flask_mail import Message
from flask import render_template
from app import mail,APP
from threading import Thread

def send_password_reset_email(user,email):
	token = user.get_reset_password_token()
	send_email('[Microblog] Reset Your Password',
			   sender=APP.config['ADMINS'][0],
			   recipients=[email],
			   text_body=render_template('email/reset_password.txt',user=user, token=token),
			   html_body=render_template('email/reset_password.html',user=user, token=token))

def send_async_email(APP, msg):
	with APP.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	Thread(target=send_async_email, args=(APP, msg)).start()	