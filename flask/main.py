# main.py

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from datetime import datetime


app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:abcd4321@Localhost:3306/test"

db.init_app(app)



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

# def random_name():
#     return 

sql_cmd_create_table = """
    CREATE TABLE potlala (id INT NOT NULL PRIMARY KEY, name  VARCHAR(40), email VARCHAR(40))
"""

@app.route('/')
def index():
    title = "first page"
    return render_template("index.html", title = title)


@app.route('/db', methods = ['POST', 'GET'])
def dbd():
    title = "mysql db"
    db_data = mydb.query.all()
    return render_template("db.html", title = title, db_data = db_data)


@app.route('/insert', methods = ['POST', 'GET'])
def insertdb():
    # db.engine.execute(sql_cmd_create_table)
    return "ok"

if __name__ == "__main__":
    app.run()