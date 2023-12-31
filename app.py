import random
from flask import request , jsonify , Flask, render_template, send_from_directory
import os
from src.dj import create_playlist
import sys
import threading
# Create a queue to pass data between threads

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
# Directory where your MP3 files are stored
music_directory = 'music/'

@app.route('/')
def index():
    music_type = request.args.get('type')
    # print('This is error output', file=sys.stderr)
    # print('This is standard output', file=sys.stdout)
    if music_type == None:
        return render_template('index.html', music_type="dnb")
    return render_template('index.html', music_type=music_type)

@app.route('/music/dnb/<filename>')
def play_music(filename):
    return send_from_directory(music_directory + "dnb/", filename)


@app.route('/music/techno/<filename>')
def play_techno(filename):
    return send_from_directory(music_directory + "techno/", filename)

@app.route('/music/phonk/<filename>')
def play_phonk(filename):
    return send_from_directory(music_directory + "phonk/", filename)


@app.route('/create_playlist/<string:type_music>')
def generate_playlist(type_music):
    return create_playlist(5, type_music)
    





if __name__ == '__main__':

    app.run(debug=True)
