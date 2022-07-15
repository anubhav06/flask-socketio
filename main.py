from email import message
import json
from flask import Flask 
from flask_socketio import SocketIO, send, emit
from flask import render_template, request, session, redirect, Response
from flask_session import Session
from deta import Deta
from decouple import config
from passlib.hash import bcrypt


deta = Deta(config('PROJECT_KEY'))
db = deta.Base('default')

app = Flask(__name__)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

socketio = SocketIO(app, cors_allowed_origins='*')

REGISTRANTS = {}

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #  Hash the user's password
        password_hash=bcrypt.hash(password)

        # Store the user's data in database
        user = db.put({
            'username' : username,
            'password' : password_hash
        })

        print('user registered!', user)
        return redirect('/')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db.fetch({'username' : username})._items
        if not user:
            return Response("{'msg': 'user not found'}", status=404)

        # Verify if the input password is same as the hashed password
        verify_pass =  bcrypt.verify(password, user[0]['password'])
        if verify_pass is False:
            return Response("{'msg' : 'Incorrect Password!'}", status=401)

        session['name'] = username
        print('user logged in!')
        return redirect('/')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session['name'] = None
    return redirect('/')


@app.route('/')
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template('index.html', data = session['name'])



# Socket-IO

@socketio.on('message')
def handle_message(data):
    print('user', session['name'])
    print('msg ', data)
    send(data, broadcast=True)


    
if __name__ == '__main__':
	socketio.run(app)