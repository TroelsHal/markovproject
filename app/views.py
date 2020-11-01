from app import app
from app import backend
from flask import render_template, request
import json

@app.route("/")
def index():
    return "Hello world"

@app.route("/about")
def about():
    return "All about Flask"

@app.route("/lostsong", methods=['POST', 'GET'])
def lostsong():
    if request.method == "POST":
        reqlist = request.form.getlist('album')
        song = backend.getSong(reqlist)
        prechecklist = reqlist
        return render_template("lostsong.html", song=song, prechecklist=json.dumps(prechecklist))
    else:
        return render_template("lostsong.html", song="choose albums")


