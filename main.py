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


@socketio.on('join')
def join(data):
    print('join')
    room_id, name = data['roomname'], data['playername']

    if room_id in rooms:
        room = rooms[room_id]
        room.add_player(name)
        return redirect(url_for('wait'))
    else:
        print(room_id)
        room = Room(room_id)
        rooms[room_id] = room
        room.add_player(name)
        return redirect(url_for('hostwait'))


@socketio.on('start')
def start(data):
    print('start')
    room_id = data['roomname']


# @app.route('/join')
# def join():
#     sess_id = request.namespace.socket.sessid
#     room_id = request.args.get('roomid')
#     name = request.args.get('name')
#     print(room_id)
#     print(name)

#     if room_id in rooms:
#         room = rooms[room_id]
#         room.add_player(name)
#     else:
#         print(room_id)
#         room = Room(room_id)
#         rooms[room_id] = room
#         room.add_player(name)
#     return room_id

@app.route('/waitingroom')
def wait(): return render_template('wait.html', roomname='roomname')

@app.route('/hostwait')
def hostwait(): return render_template('hostwait.html')


if __name__ == '__main__':
    # app.run(host = '0.0.0.0')
    socketio.run(app)