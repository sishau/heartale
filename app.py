#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import base64
from queue import Queue
from flask import Flask, request, Response, render_template, session
from flask_socketio import SocketIO, emit

from tools.constant import *
from tools import logger

q = Queue(maxsize=3)
qlock = threading.Lock()
cur_index = 0
cur_pos = 0
cur_audio = None

def t_get_text(q: Queue):
    SERVER.initialize()
    logger.info("Server initialized")
    TTS.initialize()
    logger.info("TTS initialized")
    gen = SERVER.GenText()
    while True:
        gen_text = next(gen)
        text = gen_text["text"]
        gen_text["audio"] = TTS.synthesize(text).read()
        q.put(gen_text)

app = Flask(__name__)
app.config['SECRET_KEY'] = '~heartale!'
socketio = SocketIO(app)
t = threading.Thread(target=t_get_text, args=(q,))
t.start()

@socketio.on('request_next_audio')
def request_next_audio():
    global cur_index, cur_pos, cur_audio
    app.logger.info("request_next_audio")
    cur_audio = q.get()
    audio = cur_audio["audio"]
    text = cur_audio["text"]
    index = cur_audio["chapterIndex"]
    position = cur_audio["position"]
    logger.info(f"Sending audio {index} {position} {text}")

    if index != cur_index:
        SERVER.save_book_progress(index, position)
    cur_index = index
    cur_pos = position

    audio_data = base64.b64encode(audio).decode('utf-8')
    emit("audio_data", {'audio_base64': audio_data})
    if session.get('text_sync', False):
        emit("text_data", text)

@socketio.on('connect')
def handle_connect():
    app.logger.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    q.queue.appendleft(cur_audio)
    app.logger.info('Client disconnected')

@socketio.on('text_sync')
def handle_text_sync(checked):
    session['text_sync'] = checked

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/save', methods=['GET', 'POST'])
def save():
    index = int(request.args.get('index', None))
    position = int(request.args.get('pos', None))
    global cur_index, cur_pos
    if index is None or position is None:
        index = cur_index
        position = cur_pos
    SERVER.save_book_progress(index, position)
    return Response("success", status=200)

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=8080, allow_unsafe_werkzeug=True)
    # app.run(debug=False, host='0.0.0.0', port=8080)
