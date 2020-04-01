import flask
from flask import jsonify, request, Response
from flask.views import View, MethodView
from flask_api import status
from .models import User
import jwt


class GetUser(MethodView):

    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)

    def post(self):
        return jsonify({
            'message': 'Method \"POST\" not allowed.'
        })


class AddUser(MethodView):

    def post(self):
        try:
            body = request.get_json()
            token = flask.request.headers.get('Authorization')
            print(token)

            if not body:
                return jsonify({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Missing body',
                })

            user = User(**body).save()
            id = user.id

            return jsonify({
                'status': status.HTTP_200_OK,
                'id': str(id),
                'message': 'User Added',
            })

        except Exception as e:
            return jsonify({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e),
            })


class A(View):

    def dispatch_request(self):
        return Response("HAAHHAHA", mimetype="application/json", status=200)


class Login(MethodView):

    def post(self):
        try:
            payload = request.get_json()

            user = User(name=payload['name'])
            if not user:
                return jsonify({
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'Invalid Credentials',
                })

            from app import app
            token = jwt.encode({'data': payload}, app.config['SECRET_KEY'], algorithm='HS256')
            data = {
                'status': status.HTTP_200_OK,
                'token': token.decode('UTF-8'),
                'message': 'Login successfully.',
            }
            return jsonify(data)

        except Exception as e:
            return jsonify({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e),
            })