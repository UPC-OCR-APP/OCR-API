import flask
from controllers.user_controller import USERS


app = flask.Flask(__name__)


@app.route('/')
def index():
    return {"message": "Probando api"}


app.register_blueprint(USERS)
if __name__ == "__main__":
    app.run()
