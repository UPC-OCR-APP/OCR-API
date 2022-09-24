import flask
from flask import request, Response
from bson import json_util
import pymongo
USERS = flask.Blueprint('users', __name__)


myclient = pymongo.MongoClient("mongodb://3ce4e613-0ee0-4-231-b9ee:qfDSkSADTncQVX9L0T4910t4uhxe7QJpPaJCcWcNr5SYqB1EzXOZDPQz34bTXNCrdVcZ1X9ga6M4tRyepsRP7g==@3ce4e613-0ee0-4-231-b9ee.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@3ce4e613-0ee0-4-231-b9ee@")


@USERS.route('/users', methods=['GET'])
def getUsers():
    users = myclient.ocrapp.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')
