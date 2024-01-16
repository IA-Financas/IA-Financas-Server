from flask import Flask, render_template, request, url_for, redirect, session, flash
import sqlalchemy
from random_session_maker import random_string
from datetime import timedelta



app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)
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
        print(f"Received username: {user}")
        session["user"]= user
        #flash(f"{user} has been logged sucessfully!", "info")
        return redirect(url_for("user"))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    else:
        if "user" in session:
            flash(f"{user} has been logged sucessfully!", "info")
            return redirect(url_for("user"))
        
        else:
            print("Rendering login.html")
            return render_template("login.html")                       

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"{{user}} was logged out!", "info")    
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route ("/user", methods= ["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form[""]
            session["email"] = email
        else:
            if "email" in session:
                email = session 

        flash(f"{user} has been logged sucessfully!", "alert alert-warning")
        return render_template("user.html", user= user)
    else:
        flash(f"You are not logged in", "info")
        return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug = True)