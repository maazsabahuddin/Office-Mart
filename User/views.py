import ast
import json

import flask
from flask import jsonify, request, Response
from flask.views import View, MethodView
from flask_api import status
from markupsafe import escape
from .models import User


class Login(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        data = {
            'status': status.HTTP_200_OK,
            'token': 'AasdJdAH2h91dhajsdkaDAHDsdD_1',
            'message': 'Login successfully.',
        }
        return jsonify(data)


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
