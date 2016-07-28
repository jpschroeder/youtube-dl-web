from __future__ import unicode_literals
import youtube_dl

import uuid
import threading

import eventlet
eventlet.monkey_patch()


from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'digitalarbory'
socketio = SocketIO(app)

@app.route("/")
def index():
    return app.send_static_file('index.html')

class DownloadHandlers(object):
    def __init__(self, sid):
        self.sid = sid

    def debug(self, msg):
        socketio.emit('debug', msg, room=self.sid)

    def warning(self, msg):
        socketio.emit('warning', msg, room=self.sid)

    def error(self, msg):
        socketio.emit('error', msg, room=self.sid)

    def progress(self, d):
        socketio.emit(d['status'], d, room=self.sid);


def download_progress(d):
    socketio.emit(d['status'], d);

def do_download(sid, url):
    handle = DownloadHandlers(sid);
    ydl_opts = {
        'logger': handle,
        'progress_hooks': [handle.progress],
        'outtmpl': 'static/videos/%(title)s-%(id)s.%(ext)s',
        #'restrictfilenames': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@socketio.on('download')
def handle_init(message):
    #vidid = uuid.uuid4()
    sid = request.sid
    url = message['url']
    thread = threading.Thread(target=do_download, args=(sid, url,))
    thread.start()
    #return str(vidid)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5000,debug=False)