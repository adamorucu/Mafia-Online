from flask import Flask, render_template, request, redirect, url_for
import requests
import pyqrcode
from flask_socketio import SocketIO
import os

from room import Room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}

@app.route("/")
def main(): 
    print(request.url)
    url = pyqrcode.create(request.url)
    url.png('static/img/qr.png', scale=5)
    return render_template('index.html')

@socketio.on('join')
def join(data):
    print('join')
    room_id, name = data['roomname'], data['playername']
    sessid = request.sid

    if room_id in rooms:
        room = rooms[room_id]
        socketio.emit('joinaff', {'ishost': 'F', 'room': room_id, 'players': room.player_names + [name]})
    else:
        print(room_id)
        room = Room(room_id, sessid)
        rooms[room_id] = room
        socketio.emit('joinaff', {'ishost': "T", 'room': room_id, 'players': room.player_names + [name]})
    room.add_player(sessid, name)
    # socketio.emit('plist', {'players': room.sessids}, to=room.sessids[0])

@socketio.on('start')
def start(data):
    print('start')
    room_id = data['roomname']
    room = rooms[room_id]
    room.assign_roles()
    print(room.roles)
    for ind, player in enumerate(room.sessids):
        print('EMITTING', {'role': room.roles[ind]}, ' to', player)
        socketio.emit('startgame', {'role': room.roles[ind], 'explanation': room.expl(room.roles[ind])}, to=player)

if __name__ == '__main__':
    socketio.run(app)