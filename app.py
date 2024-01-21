from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
    
from server.random_session_maker import random_string
from datetime import timedelta


#configurações do app
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:123456@localhost/flask_base'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = random_string(length=10)

#ORM -> database
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column("ID", db.Integer, primary_key = True)
    name = db.Column("NAME", db.String(30))
    email = db.Column("EMAIL", db.String(30))
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
#Rotas
@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/")
def index(): 
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

        found_users = users.query.filter_by(name="user").first()
        if found_users:
            session["email"] = found_users.email
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
            user = users(user, "")
            db.session.add(user)
            db.sessioncommit()
        #flash(f"{user} has been logged sucessfully!", "info")
        return redirect(url_for("user"), email=email)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    else:
        if "user" in session:
            flash(f"{user} has been logged sucessfully!","alert")
            return redirect(url_for("user"))
        
        else:
            print("Rendering login.html")
            return render_template("login.html")                       

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"{user} has been logged out!","alert")    
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route ("/user", methods= ["POST", "GET"])
def user():
    email= None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_users = users.query.filter_by(name="user").first()
            found_users.email= email
            db.commit()
        else:
            if "email" in session:
                email = session["email"]
    
        flash(f"{user} has been logged sucessfully!", "alert")
        return render_template("user.html", user= user, email= email)
    else:
        flash(f"You are not logged in", "info")
        return redirect(url_for("login"))



#Loop da aplicação
if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)