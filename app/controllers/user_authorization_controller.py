# utils import
import datetime

from flask import request, jsonify, json, current_app

# parent class imports
from app.controllers.base_controller import BaseController
from app.models import db
from app.models.user import User
from app.services import userservice
from app.models.access_token import AccessToken

class UserAuthorizationController(BaseController):

	@staticmethod
	def login(request):
		username = request.form['username'] if 'username' in request.form else None
		password = request.form['password'] if 'password' in request.form else None
		if username and password:
			# check if user exist
			user = db.session.query(User).filter_by(username = username).first()
			if user is not None:
				if user.verify_password(password):
					refresh_token = user.generate_refresh_token()
					access_token = user.generate_auth_token()
					UserAuthorizationController.save_token(access_token, refresh_token, user.id)
					return BaseController.send_response({'access_token': access_token.decode(), 'refresh_token': refresh_token}, 'User logged in successfully')
				else:
					return BaseController.send_response(None, 'wrong credentials')
			else:
				return BaseController.send_response(None, 'username not found')
		return BaseController.send_response({}, 'username and password required')

	@staticmethod
	def register(request):
		firstname = request.json['first_name'] if 'first_name' in request.json else None
		lastname = request.json['last_name'] if 'last_name' in request.json else ''
		email = request.json['email'] if 'email' in request.json else None
		username = request.json['username'] if 'username' in request.json else None
		role = request.json['role'] if 'role' in request.json else None
		password = request.json['password'] if 'password' in request.json else None
		
		if firstname and email and username and role and password:
			payloads =  {
				"first_name": firstname,
				"last_name": lastname,
				"email": email,
				"username": username,
				"role": role,
				"password": password
			}
		else:
			return BaseController.send_response(None, 'payloads not valid')

		result = userservice.register(payloads)
		
		if not result['error']:
			return BaseController.send_response(result['data'].as_dict(), 'user succesfully registered')
		else:
			return BaseController.send_response(None, result['data'].decode('utf-8'))
		
	def save_token(access_token, refresh_token, user_id):
		token_exist = db.session.query(AccessToken).filter_by(user_id=user_id).first()
		if not token_exist:
			payload = AccessToken(access_token, refresh_token, user_id)
			db.session.add(payload)
			db.session.commit()
			return
		token_exist.access_token = access_token
		token_exist.refresh_token = refresh_token
		db.session.commit()
		return