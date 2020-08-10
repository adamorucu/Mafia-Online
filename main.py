from flask import Flask, render_template, request, redirect, url_for
import requests
from flask_socketio import SocketIO

from room import Room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}

@app.route("/")
def main(): return render_template('home.html')

@app.route('/test')
def test():
    return redirect(url_for('main'))


@socketio.on('join')
def join(data):
    print('join')
    room_id, name = data['roomname'], data['playername']
    sessid = request.namespace.socket.sessid

    if room_id in rooms:
        room = rooms[room_id]
        room.add_player(name)
        socketio.emit('redirect', {'url': url_for('wait'), 'room': room_id})
    else:
        print(room_id)
        room = Room(room_id)
        rooms[room_id] = room
        room.add_player(name)
        print('redirecting')
        socketio.emit('redirect', {'url': url_for('hostwait'), 'room': room_id})
    room.add_player(sessid)


@socketio.on('start')
def start(data):
    print('start')
    room_id = data['roomname']
    room = rooms[room_id]
    room.assign_roles()
    for ind, player in enumerate(room.players):
        socketio.emit('startgame', {'url': url_for('game'), 'role': room.roles[ind]}, to=player)


@app.route('/waitingroom')
def wait(): 
    print('wait')
    room = request.args.get('room')
    return render_template('wait.html', roomname=room)

@app.route('/hostwait')
def hostwait(): 
    print('hostwait')
    return render_template('hostwait.html')

@app.route('/game')
def game():
    print('game')
    role = request.args.get('role')
    return render_template('game.html', role=role)


if __name__ == '__main__':
    # app.run(host = '0.0.0.0')
    socketio.run(app)