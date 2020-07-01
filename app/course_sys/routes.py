from .. import db
from . import course_sysbp
from flask import jsonify, request
from ..models import Course,Permission
from app.log_sys.routes import token_required

@course_sysbp.after_request
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

@course_sysbp.route('/check_course_json',methods=['GET','POST'])
@token_required(Permission.READ)
def checkcoursejson():
	try:
		courserec = [course.to_json() for course in Course.query.all()]
		response = { 'records': courserec }
		return jsonify(response)
	except:
		return {'result':'data fetch failed'}

@course_sysbp.route('/add_course_json',methods=['POST'])
@token_required(Permission.ADMIN)
def addcoursejson():
	jsdat = request.json
	check_course = Course.query.filter_by(ID = jsdat.get('id'),name = jsdat.get('name')).all()

	if check_course and check_course.count() != 0:
		return jsonify({ 'result' : 'Course already in database'})

	if jsdat.get('id') == '' or jsdat.get('id') is None:
		return jsonify({ 'result' : 'no couse id given'})

	if jsdat.get('name') == '' or jsdat.get('name') is None:
		return jsonify({ 'result' : 'no course name given'})

	course = Course.from_json(jsdat)
	if course is None:
		return jsonify({ 'result' : 'couldn\'t create course record'})

	try:
		db.session.add(course)
		db.session.commit()
		return jsonify({ 'result' : 'success'})
	except:
		return jsonify({ 'result' : 'fail'})

@course_sysbp.route('/modify_course_json',methods=['POST'])
@token_required(Permission.ADMIN)
def modifycoursejson():
	oldjs = request.json['old']
	newjs = request.json['new']
	
	course = Course.query.filter_by(ID=oldjs.get('id'),name=oldjs.get('name')).all()

	if not course:
		return jsonify({ 'result' : 'No course {} in database'.format(oldjs.get('id'))})

	if newjs.get('id') == '' or newjs.get('id') is None:
		return jsonify({ 'result' : 'empty course id'})
	if newjs.get('name') == '' or newjs.get('name') is None:
		return jsonify({ 'result' : 'empty course name'})

	check_course = Course.query.filter_by(ID = newjs.get('id'),name = newjs.get('name')).all()

	if check_course:
		return jsonify({ 'result' : 'Course already in database'})

	course.ID = newjs.get('id') or course.ID
	course.name = newjs.get('name') or course.name

	try:

		db.session.commit()
		return jsonify({ 'result' : 'Course modify success'})
	except:
		return jsonify({ 'result' : 'Course modify fail'})

@course_sysbp.route('/delete_course_json',methods=['POST'])
@token_required(Permission.ADMIN)
def delcoursejson():
	if not request.get_data('id'):
		return jsonify({ 'result' : 'No id given'})

	course = Course.query.filter_by(ID=request.get_data('id')).all()
	if not course:
		return jsonify({ 'result' : 'No such course in database'})
	try:
		db.session.delete(course)
		db.session.commit()
		return jsonify({ 'result' : 'Course deletion success'})
	except:
		return jsonify({ 'result' : 'Course deletion failed'})
