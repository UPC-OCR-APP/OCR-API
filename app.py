import flask
from controllers.user_controller import USERS
from controllers.consultation_controller import CONSULTATIOS
from controllers.history_controller import STORIES

app = flask.Flask(__name__)


@app.route('/')
def index():
    return {"message": "Probando api"}


app.register_blueprint(USERS)
app.register_blueprint(CONSULTATIOS)
app.register_blueprint(STORIES)
if __name__ == "__main__":
    app.run()
