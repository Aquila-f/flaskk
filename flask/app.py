from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:abcd4321@Localhost:3306/test"
db.init_app(app)
socketio = SocketIO(app)


class mydb(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    student_id = db.Column(db.Integer)
    major = db.Column(db.String(40), nullable=True)

    def __init__(self, id, name, student_id, major):
        self.id = id
        self.name = name
        self.student_id = student_id
        self.major = major


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/class_create')
def createclass():
    return "Adsf"

@app.route('/class')
def gotoclass(name):
    return name

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/db', methods = ['POST', 'GET'])
def dbd():
    title = "mysql db"
    db_data = mydb.query.all()
    return render_template("db.html", title = title, db_data = db_data)

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template("chat.html", username=username, room=room)
    else:
        return redirect(url_for('login'))



@socketio.on('send_message')
def handle_send_message(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'], data['room'], data['message']))
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('jr')
def handle_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)
    

if __name__=="__main__":
    socketio.run(app, debug=True)

# if __name__=="__main__":
#     app.run()