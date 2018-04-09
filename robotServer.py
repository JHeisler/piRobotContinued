from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
#import logging
import pickle
#logging.basicConfig(level=logging.DEBUG)
from PIL import Image
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('Mov')
def on_message(message):
    print(message)
    socketio.emit('move', message)

@socketio.on('vid')
def on_vid(frame):
    image_stream = io.BytesIO()
    image_stream.write(pickle.loads(frame))
    image_stream.seek(0)
    t = Image.open(image_stream)
    print('Image Received')
    t.save("/home/pi/robots/static/test.jpg", "JPEG")
    socketio.emit('frame', '')

if __name__ == '__main__':
    socketio.run(app)
