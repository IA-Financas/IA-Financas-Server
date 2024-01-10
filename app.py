from flask import Flask, render_template, request, url_for, redirect
import sqlalchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLACLHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/flask_crud'
@app.route("/base")
def base():
    return render_template("base.html")
@app.route("/")
def home(): 
    return render_template("index.html")
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")
if __name__ == "__main__":
    app.run(debug = True)