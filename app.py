from flask import Flask, render_template, request, url_for, redirect, session
import sqlalchemy
import random
import string
from datetime import datetime
from random_session_maker import random_string

app = Flask(__name__)
app.config['SQLACLHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/flask_crud'
app.secret_key = random_string(length=10)


@app.route("/base")
def base():
    return render_template("base.html")
@app.route("/")
def home(): 
    return render_template("index.html")
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")
@app.route("/login", methods=["POST", "GET"])

def login():
    
    if request.method == "POST": 
        user = request.form["name"]
        session["user"]= user
        return redirect(url_for("user", usuario= user))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    else:
        return render_template("login.html")
   
@app.route("/child")
def child():
    return render_template("childtest.html")                                                                                                                                                                                
@app.route ("/usuario")
def user():
    
    if "user" in session:
        user = session["user"]
        return f"<h1></h1>"
    else:
        return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug = True)