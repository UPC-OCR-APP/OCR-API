import flask
from flask import request, Response
from bson import json_util
import pymongo


CONSULTATIOS = flask.Blueprint('consultations', __name__)

myclient = pymongo.MongoClient(
    "mongodb://ocr-app:YTJVfr3w4SEFNPrOj461mwGdUJrMv4MYFsOSIUk4SA32YxBYekHdjaelHhOQBMnStmbSAs28SmJ56A4kW7NyqA==@ocr-app.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@ocr-app@")


@CONSULTATIOS.route('/consulta', methods=['POST'])
def setConsulta():
    fecha_atencion = request.json['fecha_atencion']
    hora = request.json['hora']
    edad = request.json['edad']
    diagnostico = request.json['diagnostico']
    tratamiento = request.json['tratamiento']
    examenes_auxiliares = request.json['examenes_auxiliares']
    proxima_cita = request.json['proxima_cita']
    observaciones = request.json['observaciones']
    numero_historia = request.json['numero_historia']
    detalle_consulta = request.json['detalle_consulta']
    signos_vitales = request.json['signos_vitales']
    datos_antropometricos = request.json['datos_antropometricos']
    funciones_biologicas = request.json['funciones_biologicas']

    if fecha_atencion and hora and edad:
        id = myclient.ocrapp.consulta.insert_one(
            {
                'fecha_atencion': fecha_atencion,
                'hora': hora,
                'edad': edad,
                'diagnostico': diagnostico,
                'tratamiento': tratamiento,
                'examenes_auxiliares': examenes_auxiliares,
                'proxima_cita': proxima_cita,
                'observaciones': observaciones,
                'numero_historia': numero_historia,
                'detalle_consulta': detalle_consulta,
                'signos_vitales': signos_vitales,
                'datos_antropometricos': datos_antropometricos,
                'funciones_biologicas': funciones_biologicas,
            })
        return {"meesage": "Registro de historia exitoso"}
    else:
        return {"meesage": "Faltan datos"}


@CONSULTATIOS.route('/consulta/<numero_historia>', methods=['GET'])
def getConsulta(numero_historia):
    users = myclient.ocrapp.consulta.find({"numero_historia": numero_historia})
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')


@CONSULTATIOS.route('/consulta/last/<numero_historia>', methods=['GET'])
def getConsultaByQuantity(numero_historia):
    myclient.ocrapp.consulta.create_index("fecha_atencion")
    consultas = myclient.ocrapp.consulta.find({"numero_historia": numero_historia}).limit(3).sort(
        'fecha_atencion', pymongo.DESCENDING)
    response = json_util.dumps(consultas)
    return Response(response, mimetype='application/json')


@CONSULTATIOS.route('/consulta/date/', methods=['POST'])
def getConsultaByDate():
    fecha_atencion = request.json['fecha_atencion']
    numero_historia = request.json['numero_historia']
    users = myclient.ocrapp.consulta.find(
        {"fecha_atencion": fecha_atencion, "numero_historia": numero_historia})
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')
