from flask import Flask, Response
from flask_socketio import SocketIO
from flask_cors import CORS
from send2trash import send2trash
from engineio.async_drivers import gevent

from .shared import Config
from .api.quiz import api_quiz
from .api.editor import api_editor
from .api.io import api_io, r_import_progress
from .api.media import api_media

app = Flask(__name__, static_folder=str(Config.MEDIA_FOLDER))
socketio = SocketIO(app, engineio_logger=True, async_mode='gevent')
CORS(app)

app.register_blueprint(api_quiz)
app.register_blueprint(api_editor)
app.register_blueprint(api_io)
app.register_blueprint(api_media)


@app.route("/api/reset", methods=["DELETE"])
def r_reset():
    Config.DB.close()
    send2trash(Config.COLLECTION)
    return Response(status=201)


@socketio.on("message")
def io_anki_progress(message):
    r_import_progress(message)


def run_server():
    socketio.run(app, port=Config.PORT)
