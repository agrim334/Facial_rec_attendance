from .. import db
from . import dept_sysbp
from flask import jsonify, request
from ..models import Department,Permission
from app.log_sys.routes import token_required

@dept_sysbp.after_request
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

@dept_sysbp.route('/check_dept_json',methods=['GET','POST'])
@token_required(Permission.READ)
def checkdeptjson():
	try:
		deptrec = [dept.to_json() for dept in Department.query.all()]
		response = { 'records': deptrec }
		return jsonify(response)
	except:
		return {'result':'data fetch failed'}

@dept_sysbp.route('/add_dept_json',methods=['GET','POST'])
@token_required(Permission.ADMIN)
def adddeptjson():
	jsdat = request.json
	check_dept = Department.query.filter_by(ID = jsdat.get('id')).all()

	if check_dept:
		return jsonify({ 'result' : 'dept already in database'})

	if jsdat.get('id') == '' or jsdat.get('id') is None:
		return jsonify({ 'result' : 'empty dept id'})
	if jsdat.get('name') == '' or jsdat.get('name') is None:
		return jsonify({ 'result' : 'empty dept name'})

	dept = Department.from_json(jsdat)
	if dept is None:
		return jsonify({ 'result' : 'can\'t create department record'})

	try:
		db.session.add(dept)
		db.session.commit()
		return jsonify({ 'result' : 'Dept add success'})
	except:
		return jsonify({ 'result' : 'Dept add fail'})

@dept_sysbp.route('/modify_dept_json',methods=['GET','POST'])
@token_required(Permission.ADMIN)
def modifydeptjson():
	oldjs = request.json['old']
	newjs = request.json['new']
	dept = Department.query.filter_by(ID=oldjs.get('id'),name=oldjs.get('name')).first_or_404()
	if dept is None:
		return jsonify({ 'result' : 'No such Department as {}'.format(newjs.get('name'))})

	if newjs.get('id') == '' or newjs.get('id') is None:
		return jsonify({ 'result' : 'empty dept id'})

	if newjs.get('name') == '' or newjs.get('name') is None:
		return jsonify({ 'result' : 'empty dept name'})

	check_dept = Department.query.filter_by(ID = newjs.get('id')).all()

	if not check_dept:
		return jsonify({ 'result' : 'Dept {} already in database'.format(newjs.get('id'))})

	dept.ID = newjs.get('id') or dept.ID
	dept.name = newjs.get('name') or dept.name

	try:
		db.session.commit()
		return jsonify({ 'result' : 'Dept modify success'})
	except:
		return jsonify({ 'result' : 'Dept modify fail'})

@dept_sysbp.route('/delete_dept_json',methods=['GET','POST'])
@token_required(Permission.ADMIN)
def deldeptjson():
	if not request.get_data('id'):
		return jsonify({ 'result' : 'No id given'})

	dept = Department.query.filter_by(ID=request.get_data('id')).all()
	if not dept:
		return jsonify({ 'result' : 'No such department in database'})
	try:
		db.session.delete(dept)
		db.session.commit()
		return jsonify({ 'result' : 'Dept deletion success'})
	except:
		return jsonify({ 'result' : 'Dept deletion failed'})
