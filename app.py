import os
import flask
from controllers.user_controller import USERS
from controllers.consultation_controller import CONSULTATIOS
from controllers.history_controller import STORIES
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from flask import request, Response
from PIL import Image, ImageOps

app = flask.Flask(__name__)

valor = '/image.jpeg'
path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
pathfinal = path + valor
picture = Image.open(pathfinal)
picture = ImageOps.exif_transpose(picture)
picture.save('image.jpeg', 'JPEG', optimize=True, quality=50)

endpoint = "https://ocr-app-ocr-app.cognitiveservices.azure.com/"
key = "c33dd42ea5a84541b2d1ff04bd82c314"


@app.route('/')
def index():
    print(pathfinal)
    return {"message": "Probando api"}


@app.route("/consulta")
def pruebas():

    ultima_cadena = ""
    cadena_vacía = ""
    diccionario = {}
    diccionario["Fec_Atencion"] = ""
    diccionario["Hora"] = ""
    diccionario["Edad"] = ""
    diccionario["Motivo"] = ""
    diccionario["Tipo_Enf"] = ""
    diccionario["Signos_Sintomas"] = ""
    diccionario["Apetito"] = ""
    diccionario["Sed"] = ""
    diccionario["Suenio"] = ""
    diccionario["Estado_Animo"] = ""
    diccionario["Orina"] = ""
    diccionario["Deposiciones"] = ""
    diccionario["Ex_Fisico"] = ""
    diccionario["Temperatura"] = ""
    diccionario["Pa"] = ""
    diccionario["Fc"] = ""
    diccionario["Fr"] = ""
    diccionario["Peso"] = ""
    diccionario["Talla"] = ""
    diccionario["Imc"] = ""
    diccionario["Diagnostico"] = ""
    diccionario["Tratamiento"] = ""
    diccionario["Examenes_Auxiliares"] = ""
    diccionario["Referencia"] = ""
    diccionario["Proxima_Cita"] = ""
    diccionario["Atendido_Por"] = ""
    diccionario["Observaciones"] = ""

    with open(pathfinal, "rb") as fd:
        invoice = fd.read()

        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key))
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-document", invoice)
        result = poller.result()
        for kv_pair in result.key_value_pairs:
            if kv_pair.key.content == "FECHA:":
                diccionario["Fec_Atencion"] = kv_pair.value.content
            if kv_pair.key.content == "HORA:":
                diccionario["Hora"] = kv_pair.value.content
            if kv_pair.key.content == "EDAD:":
                diccionario["Edad"] = kv_pair.value.content
            if kv_pair.key.content == "Motivo de consulta:":
                diccionario["Motivo"] = kv_pair.value.content
            if kv_pair.key.content == "Tiempo de enfermedad:":
                diccionario["Tipo_Enf"] = kv_pair.value.content
            if kv_pair.key.content == "Apetito:":
                diccionario["Apetito"] = kv_pair.value.content
            if kv_pair.key.content == "Sed:":
                diccionario["Sed"] = kv_pair.value.content
            if kv_pair.key.content == "Sue":
                diccionario["Suenio"] = kv_pair.value.content
            if kv_pair.key.content == "Orina:":
                diccionario["Orina"] = kv_pair.value.content
            if kv_pair.key.content == "Ex. Fisico:" or kv_pair.key.content.startswith("Ex"):
                diccionario["Ex_Fisico"] = kv_pair.value.content
            if kv_pair.key.content == "FC:":
                diccionario["Fc"] = kv_pair.value.content
            if kv_pair.key.content == "FR:":
                diccionario["Fr"] = kv_pair.value.content
            if kv_pair.key.content == "Peso:":
                diccionario["Peso"] = kv_pair.value.content
            if kv_pair.key.content == "Talla:":
                diccionario["Talla"] = kv_pair.value.content
            if kv_pair.key.content == "IMC:":
                diccionario["Imc"] = kv_pair.value.content
            if kv_pair.key.content == "Exámenes auxiliares:":
                diccionario["Examenes_Auxiliares"] = kv_pair.value.content
            # if kv_pair.key.content == "Referencia (lugar y motivo):" or kv_pair.key.content.startswith("Referen"):
            #        diccionario["Referencia"] = kv_pair.value.content
            if kv_pair.key.content == "Atendido por:" or kv_pair.key.content.startswith("Atendido"):
                diccionario["Atendido_Por"] = kv_pair.value.content
            if kv_pair.key.content == "Próxima cita:":
                diccionario["Proxima_Cita"] = kv_pair.value.content
            if kv_pair.key.content == "Estado de ánimo:":
                diccionario["Estado_Animo"] = kv_pair.value.content

        for style in result.styles:
            if style.is_handwritten:
                for span in style.spans:
                    cadena = result.content[span.offset:span.offset + span.length]

                    Estado = cadena.find("Estado")
                    Orina = cadena.find("Orina")
                    Temperatura = cadena.find("To:")
                    Presion = cadena.find("PA:")
                    Diagnostico = cadena.find("· ")
                    Tratamiento = cadena.find("· ") or cadena.find(".")
                    if Estado > -1:
                        if len(diccionario["Estado_Animo"]) == 0:
                            subcadena = cadena[Estado +
                                               17:span.offset + span.length]
                            diccionario["Estado_Animo"] = subcadena
                    if Orina > -1:
                        if len(diccionario["Orina"]) == 0:
                            subcadena = cadena[Orina +
                                               2:span.offset + span.length]
                            diccionario["Orina"] = subcadena
                    if Temperatura > -1:
                        Nuevo = len("To:")
                        if len(diccionario["Temperatura"]) == 0:
                            subcadena = cadena[Temperatura+Nuevo:4]
                            diccionario["Temperatura"] = subcadena
                    if Presion > -1:
                        Nuevo = len("PA:")
                        if len(diccionario["Pa"]) == 0:
                            subcadena = cadena[Presion+Nuevo:5]
                            diccionario["Pa"] = subcadena
                    if Diagnostico > -1:
                        Nuevo = len("· ")
                        if len(diccionario["Diagnostico"]) == 0:
                            subcadena = cadena[Diagnostico+Nuevo:]
                            diccionario["Diagnostico"] = subcadena
                    if Tratamiento > -1:
                        Nuevo = len("· ")
                        if len(diccionario["Tratamiento"]) == 0:
                            subcadena = cadena[Tratamiento:]
                            diccionario["Tratamiento"] = subcadena

    return {
        'Fec_Atencion': diccionario["Fec_Atencion"],
        'Hora': diccionario["Hora"],
        'Edad': diccionario["Edad"],
        'Motivo': diccionario["Motivo"],
        'Tipo_Enf': diccionario["Tipo_Enf"],
        'Signos_Sintomas': diccionario["Signos_Sintomas"],
        'Apetito': diccionario["Apetito"],
        'Sed': diccionario["Sed"],
        'Suenio': diccionario["Suenio"],
        'Estado_Animo': diccionario["Estado_Animo"],
        'Orina': diccionario["Orina"],
        'Deposiciones': diccionario["Deposiciones"],
        'Ex_Fisico': diccionario["Ex_Fisico"],
        'Temperatura': diccionario["Temperatura"],
        'Pa': diccionario["Pa"],
        'Fc': diccionario["Fc"],
        'Fr': diccionario["Fr"],
        'Peso': diccionario["Peso"],
        'Talla': diccionario["Talla"],
        'Imc': diccionario["Imc"],
        'Diagnostico': diccionario["Diagnostico"],
        'Tratamiento': diccionario["Tratamiento"],
        'Examenes_Auxiliares': diccionario["Examenes_Auxiliares"],
        'Referencia': diccionario["Referencia"],
        'Proxima_Cita': diccionario["Proxima_Cita"],
        'Atendido_Por': diccionario["Atendido_Por"],
        'Observaciones': diccionario["Observaciones"]
    }


@app.route("/image", methods=['GET', 'POST'])
def image():
    if (request.method == "POST"):
        bytesOfImage = request.get_data()
        with open(pathfinal, 'wb') as out:
            out.write(bytesOfImage)
        return "Image read"


app.register_blueprint(USERS)
app.register_blueprint(CONSULTATIOS)
app.register_blueprint(STORIES)
if __name__ == "__main__":
    app.run(debug=True)
