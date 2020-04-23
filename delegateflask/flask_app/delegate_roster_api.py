from flask import jsonify,request,redirect,url_for
from flask_app import app
from flask import Flask
from flask_cors import CORS
import string
import csv
import os

UPLOAD_FOLDER='C:\\Users\\Public\\Documents\\VillageCare\\DELEGATE_UPLOAD\\delegateflask\\flask_app\\uploaddoc'
ALLOWED_EXTENSIONS=set(['csv','xls','xlsx'])

UNAUTHORIZED={"error:":"unauthorized","STATUS CODE":400}
BADREQUEST={"error:":"unauthorized","STATUS CODE":400}
NOTFOUND={"error:":"NOT FOUND","STATUS CODE":404}

@app.errorhandler(400)
def error400(e):
    return jsonify(UNAUTHORIZED),400

@app.errorhandler(404)
def error404(e):
    return jsonify(NOTFOUND),404


@app.route('/')
def root():
    return jsonify({"message":"Delegate Roster Upload API"})

@app.route('/api/delegateroster/importfile',methods=['POST'])
def importfile():
    filehold=[]
    print(request.files['filename'])
    realfilename=request.files['filename']
    realfilename.save(os.path.join(UPLOAD_FOLDER,realfilename.filename))

    # Code to translate and map file will go here

    return jsonify({"output":"File has been processed"})
