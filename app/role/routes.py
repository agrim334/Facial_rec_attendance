from .. import db,errors
from . import role_sysbp
from flask import render_template,flash,Flask, jsonify, request, redirect,url_for,session
from ..models import User,Role,Department
import re
from flask import current_app
from datetime import datetime,timedelta

APP = current_app._get_current_object()

@role_sysbp.before_request
def make_session_permanent():
	session.permanent = True
	role_sysbp.permanent_session_lifetime = timedelta(minutes=10)		#idle timeout for user session

@role_sysbp.after_request
def after_request(response):									#security
	response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'SAMEORIGIN'
	response.headers['X-XSS-Protection'] = '1; mode=block'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
	response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
	return response

@role_sysbp.route('/check_role_json',methods=['GET'])
def checkrolejson():
	roles = [role.to_json() for role in Role.query.all()]
	response = { 'records': roles }
	return jsonify(response)