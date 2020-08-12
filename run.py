from flask import Flask, render_template, request, redirect, url_for
import requests
import pyqrcode
from flask_socketio import SocketIO, join_room
import os

from game import Game
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.KEY
socketio = SocketIO(app)

ROOMS = {}

@app.route('/')
def main():
    url = pyqrcode.create(request.url)
    url.png('static/img/main_qr.png', scale=5)
    return render_template('main.html')

@socketio.on('join')
def join(data):
    room_name, player = data['roomname'], data['playername']
    sessid = request.sid

    if room_name in ROOMS:
        room = ROOMS[room_name]
    else:
        room = Game(room_name, sessid)
        ROOMS[room_name] = room
        socketio.emit('host', to=sessid)
        print('host:', sessid)
    join_room(room_name)
    socketio.emit('population', {'players': room.player_names + [player]}, room=room_name)
    room.add_player(sessid, player)

@socketio.on('startbtn')
def start(data):
    print('Starting game:', data['room'])
    room = ROOMS[data['room']]
    room.assign_roles()
    for ind, player in enumerate(room.sessids):
        socketio.emit('startgame', {'role': room.roles[ind], 'explanation': room.expl(room.roles[ind])}, to=player)

if __name__ == '__main__':
    socketio.run(app)