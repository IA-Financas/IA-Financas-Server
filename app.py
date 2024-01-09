from flask import Flask, render_template, request, url_for, redirect
import sqlalchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLACLHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/flask_crud'

@app.route("/")
def home(): 
    return render_template("index.html", content="main page")

if __name__ == "__main__":
    app.run()