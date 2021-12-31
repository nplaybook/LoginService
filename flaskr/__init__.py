from flask_socketio import SocketIO, send
from flaskr.app import create_app

app = create_app()
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handle_message(message):
    print('Message: ' + message)
    send(message, broadcast=True)

if __name__ == '__main__':
    app.debug=True
    socketio.run(app, debug=True)