from flask import Flask, render_template, request, url_for, redirect, session
import sqlalchemy
from random_session_maker import random_string
from datetime import timedelta


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=5)
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
        session.permanent = True
        user = request.form["name"]
        session["user"]= user
        return redirect(url_for("user", usuario= user))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    else:
        if "user" in session:
            return redirect(url_for("user"))
        else:
         return render_template("login.html")
   
@app.route("/child")
def child():
    return "<h1>{name}</h1>"                       

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route ("/user")
def user():
    
    if "user" in session:
        user = session["user"]
        return render_template("homepage.html")
    else:
        return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug = True)