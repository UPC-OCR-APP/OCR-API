import flask
from flask import request, Response
from bson import json_util
import pymongo

STORIES = flask.Blueprint('stories', __name__)

myclient = pymongo.MongoClient("mongodb://ocr-app:YTJVfr3w4SEFNPrOj461mwGdUJrMv4MYFsOSIUk4SA32YxBYekHdjaelHhOQBMnStmbSAs28SmJ56A4kW7NyqA==@ocr-app.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@ocr-app@")


@STORIES.route('/history', methods=['POST'])
def createHistory():
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    dni = request.json['dni']
    numHistory = request.json['numHistory']
    date = request.json['date']
    sexo = request.json['sexo']

    if numHistory and date and nombre and apellido and dni and sexo:
        history = myclient.ocrapp.history.find_one(
            {'numHistory': numHistory})
        print(history)
        if (history == None):
            id = myclient.ocrapp.history.insert_one(
                {
                    'nombre': nombre,
                    'apellido': apellido,
                    'dni': dni,
                    'numHistory': numHistory,
                    'date': date,
                    'sexo': sexo})
            return {
                'message': 'registro exitoso'
            }
        else:
            return {'message': 'historia clinica ya existe'}

    return {'message': 'faltan datos'}


@STORIES.route('/history/<dni>', methods=['GET'])
def getHistoryByNumOfHistory(dni):
    history = myclient.ocrapp.history.find_one({'dni': dni})
    if (history == None):
        return {'message': 'Historia clinica no existe'}
    else:
        return Response(json_util.dumps(history), mimetype='application/json')


@STORIES.route('/history/name/<name>/<lastName>', methods=['GET'])
def getHistoryByName(name, lastName):
    history = myclient.ocrapp.history.find_one(
        {'nombre': name, "apellido": lastName})
    prueba = json_util.dumps(history)
    print(prueba)
    if (history == None):
        return {'message': 'Historia clinica no existe'}
    else:
        return Response(json_util.dumps(history), mimetype='application/json')
