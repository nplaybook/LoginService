from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from flaskr.app import create_app

db = SQLAlchemy()
app = create_app(db)
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handle_message(message):
    print('Message: ' + message)
    send(message, broadcast=True)

if __name__ == '__main__':
    app.debug=True
    socketio.run(app, debug=True)