import flask
from flask import request, Response
from bson import json_util
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash


USERS = flask.Blueprint('users', __name__)


myclient = pymongo.MongoClient("mongodb://ocr-app:YTJVfr3w4SEFNPrOj461mwGdUJrMv4MYFsOSIUk4SA32YxBYekHdjaelHhOQBMnStmbSAs28SmJ56A4kW7NyqA==@ocr-app.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@ocr-app@")


@USERS.route('/users', methods=['GET'])
def getUsers():
    users = myclient.ocrapp.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')


@USERS.route('/user', methods=['POST'])
def getAuthUser():
    usuario = request.json['usuario']
    password = request.json['password']
    user = myclient.ocrapp.authusers.find_one({'usuario': usuario})
    if (user != None):
        if (check_password_hash(str(user.get("password")), str(password))):
            dataUser = myclient.ocrapp.users.find_one({'usuario': usuario})
            return {
                'usuario': dataUser["usuario"],
                'nombre': dataUser["nombre"],
                'apellido': dataUser["apellido"],
                'dni': dataUser["dni"],
                'email': dataUser["email"]
            }

    return {'message': 'usuario o contraseña incorrecta'}


@USERS.route('/users', methods=['POST'])
def createUser():
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    dni = request.json['dni']
    email = request.json['email']
    usuario = request.json['usuario']
    password = request.json['password']

    if usuario and password and nombre and apellido and dni and email:
        hashedPassword = generate_password_hash(password)
        user = myclient.ocrapp.users.find({'email': email, 'usuario': usuario})
        us = []
        for doc in user:
            us.append(doc)
        print(us)
        if (len(us) == 0):
            id = myclient.ocrapp.users.insert_one(
                {'nombre': nombre, 'apellido': apellido, 'dni': dni, 'email': email, 'usuario': usuario})
            id2 = myclient.ocrapp.authusers.insert_one(
                {'usuario': usuario, 'password': hashedPassword}
            )
            return {
                'message': 'registro'
            }
        else:
            return {'message': 'usuario o correo en uso'}

    return {'message': 'faltan datos'}


@USERS.route('/users', methods=['PUT'])
def updateUsers():
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    email = request.json['email']
    usuario = request.json['usuario']
    password = request.json['password']

    if password and nombre and apellido and email:
        hashedPassword = generate_password_hash(password)
        user = myclient.ocrapp.users.find_one({'usuario': usuario})
        if (user != None):
            id = myclient.ocrapp.users.update_one(
                {'usuario': usuario}, {
                    '$set': {'nombre': nombre, 'apellido': apellido, 'email': email}}
            )
            id2 = myclient.ocrapp.authusers.update_one(
                {'usuario': usuario}, {'$set': {'password': hashedPassword}}
            )
            return {
                'message': 'registro'
            }
        else:
            return {'message': 'usuario o correo en uso'}

    return {'message': 'faltan datos'}
