from flask import Flask, render_template, request, redirect, url_for
import requests

from room import Room


app = Flask(__name__)
rooms = {}

@app.route("/")
def main():
    return 'Bonjourno Grande Padre'

@app.route('/join')
def join():
    room_id = request.args.get('roomid')
    name = request.args.get('name')
    print(room_id)
    print(name)

    if room_id in rooms:
        room = rooms[room_id]
        room.add_player(name)
    else:
        print(room_id)
        room = Room(room_id)
        rooms[room_id] = room
        room.add_player(name)
    return room_id

@app.route('/start')
def start():
    pass

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
