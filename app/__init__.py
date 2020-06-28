from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler
import os
import MySQLdb
from flask_table import Table, Col
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
bootstrap = Bootstrap()
login.login_view = 'log_sysbp.login'

def create_app():
	APP = Flask(__name__)
	APP.config.from_object(Config)
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
	bootstrap.init_app(APP)
	mail.init_app(APP)
	db.init_app(APP)
	migrate.init_app(APP,db)
	login.init_app(APP)
	CORS(APP, resources={r'/*': {'origins': '*'}})
	with APP.app_context():
		from .log_sys import log_sysbp 
		from .attd_sys import attd_sysbp 
		from .dept_sys import dept_sysbp 
		from .course_sys import course_sysbp 
		from .UCmaps import mapbp
		from .role import role_sysbp

		APP.register_blueprint(log_sysbp,url_prefix='/users')
		APP.register_blueprint(attd_sysbp,url_prefix='/attd')
		APP.register_blueprint(course_sysbp,url_prefix='/courses')
		APP.register_blueprint(dept_sysbp,url_prefix='/dept')
		APP.register_blueprint(mapbp,url_prefix='/map')
		APP.register_blueprint(role_sysbp,url_prefix='/roles')
		
	from app import models

	return APP