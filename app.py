from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

@socketio.on("message")
def handle_message(data):
    print(f"Received message: {data}")

@socketio.on("json")
def handle_json(json):
    print(f"Received message: {json}")

if __name__ == "__main__":
    socketio.run(app)