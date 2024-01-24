from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from server.random_session_maker import random_string
from datetime import timedelta
from server.dashboards_test import *
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app import app
#configurações do app
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:123456@localhost/flask_base'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = random_string(length=10)

#ORM -> database
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

class User(db.Model):
    __tablename__ = 'users'  # Make sure the table name matches your actual table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    
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

        found_User = User.query.filter_by(name="user").first()
        if found_User:
         session["email"] = found_User.email
         flash("Email was saved!")
        else:
          if "email" in session:
              email = session["email"]
              user = User(user, "")
              db.session.add(user)
              db.session.commit()
              flash(f"{user} has been logged sucessfully!", "info")
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
            found_User = User.query.filter_by(name="user").first()
            found_User.email= email
            db.session.commit()
        else:
            if "email" in session:
                email = session["email"]
    
        flash(f"{user} has been logged sucessfully!", "alert")
        return render_template("user.html", user= user, email= email)
    else:
        flash(f"You are not logged in", "info")
        return redirect(url_for("login"))


@app.route("/dashboards")
def display_dashboards():
    return render_template("dashboards.html")

#Loop da aplicação
if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)