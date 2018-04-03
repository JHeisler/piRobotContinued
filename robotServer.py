from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import logging
#logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('Mov')
def test_message(message):
    print(message)
    socketio.emit('movement', message)

if __name__ == '__main__':
    socketio.run(app)