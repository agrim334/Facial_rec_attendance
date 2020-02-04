from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler
import os

APP = Flask(__name__)
APP.config.from_object(Config)
db = SQLAlchemy(APP)
migrate = Migrate(APP,db)
login = LoginManager(APP)
login.login_view = 'login'
mail = Mail(APP)

if not APP.debug:
	if APP.config['MAIL_SERVER']:
		auth = None
		if APP.config['MAIL_USERNAME'] or APP.config['MAIL_PASSWORD']:
			auth = (APP.config['MAIL_USERNAME'], APP.config['MAIL_PASSWORD'])
		secure = None
		if APP.config['MAIL_USE_TLS']:
			secure = ()
		mail_handler = SMTPHandler(
			mailhost=(APP.config['MAIL_SERVER'], APP.config['MAIL_PORT']),
			fromaddr='no-reply@' + APP.config['MAIL_SERVER'],
			toaddrs=APP.config['ADMINS'], subject='Microblog Failure',
			credentials=auth, secure=secure)
		mail_handler.setLevel(logging.ERROR)
		APP.logger.addHandler(mail_handler)
	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,backupCount=10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	APP.logger.addHandler(file_handler)

	APP.logger.setLevel(logging.INFO)
	APP.logger.info('Microblog startup')

from app import routes,models