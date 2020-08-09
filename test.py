from flask import *
from flask_socketio import *

# Init the server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'some super secret key!'
socketio = SocketIO(app, logger=True)

# Send HTML!
@app.route('/')
def root():    
    return "Hello world!"

# Prints the user id
@app.route('/user/<id>')
def user_id(id):
    return str(id)

# Display the HTML Page & pass in a username parameter
@app.route('/html/<username>')
def html(username):
    return render_template('test.html', username=username)

# Receive a message from the front end HTML
@socketio.on('send_message')   
def message_recieved(data):
    print('asdasdas')
    # emit('message_from_server', {'text':'Message recieved!'})

# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """    
    socketio.run(app, port=8000, debug=True)