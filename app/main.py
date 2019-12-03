from __future__ import unicode_literals
import os
import sys
import time
import threading

import youtube_dl

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

import eventlet # use eventlet for the websocket server
eventlet.monkey_patch()

from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
socketio = SocketIO(app,cors_allowed_origins='*')

# Remove a file or directory
def remove(path):
    if os.path.isdir(path):
        try:
            os.rmdir(path)
        except OSError:
            print "Unable to remove folder: %s" % path
    else:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            print "Unable to remove file: %s" % path
 
# Remove files from path that are older than the number_of_days
def cleanup(number_of_days, path):
    time_in_secs = time.time() - (number_of_days * 24 * 60 * 60)
    for root, dirs, files in os.walk(path, topdown=False):
        for file_ in files:
            full_path = os.path.join(root, file_)
            stat = os.stat(full_path)
            if stat.st_mtime <= time_in_secs:
                remove(full_path)
        if not os.listdir(root):
            remove(root)

# Handlers that update the client over socket.io
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

# Kick off youtube-dl to perform the download
def do_download(sid, url):
    cleanup(2, 'static/videos') # Remove videos older than 2 days
    handle = DownloadHandlers(sid);
    ydl_opts = {
        'logger': handle,
        'progress_hooks': [handle.progress],
        'outtmpl': 'static/videos/%(title)s-%(id)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Load the main html page
@app.route("/")
def index():
    return app.send_static_file('index.html')

# Start the download
@socketio.on('download')
def handle_init(message):
    sid = request.sid
    url = message['url']
    thread = threading.Thread(target=do_download, args=(sid, url,))
    thread.start()

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5000,debug=False)
