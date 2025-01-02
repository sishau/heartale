#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tools.constant import *
from tools import logger
from flask import Flask, request, Response
import threading
import queue

def t_get_text(q):
    SERVER.initialize()
    logger.info("Server initialized")
    TTS.initialize()
    logger.info("TTS initialized")
    gen = SERVER.GenText()
    while True:
        gen_text = next(gen)
        text = gen_text["text"]
        gen_text["audio"] = TTS.synthesize(text)
        q.put(gen_text)


app = Flask(__name__)
q = queue.Queue(3)
t = threading.Thread(target=t_get_text, args=(q,))
t.start()

cur_index = 0
cur_pos = 0

@app.route('/tts', methods=['GET', 'POST'])
def tts():
    gen_audio = q.get()
    audio = gen_audio["audio"]
    index = gen_audio["chapterIndex"]
    position = gen_audio["position"]

    app.logger.debug("reading  index: {}, position: {}".format(index, position))
    global cur_index, cur_pos
    if index != cur_index:
        SERVER.save_book_progress(index, position)
    cur_index = index
    cur_pos = position

    return Response(audio, mimetype="audio/x-wav")

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
    app.run(debug=False, host='0.0.0.0', port=8080)
