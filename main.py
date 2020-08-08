from flask import Flask, render_template, request, redirect, url_for
# from flask_socketio import join_room, leave_room


app = Flask(__name__)

@app.route("/")
def main():
    return 'Bonjourno Grande Padre'

@app.route('/join')
def join():
    room_id = requests.args.get('roomid')
    name = requests.args.get('name')

# @app.route('/create')
# def create():
#     room_id = 

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
