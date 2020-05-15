from flask import jsonify,request,redirect,url_for
from flask_app import app
from flask import Flask
from flask_cors import CORS
import string
import csv
import os
import datetime
from app.facilityinfo import FacilityInfo as fc


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
    vendorname=request.form['vendor']
    print(vendorname)
    realfilename.save(os.path.join(UPLOAD_FOLDER,realfilename.filename))

    # Code to translate and map file will go here
    tf=fc.import_delegate_roster(os.path.join(UPLOAD_FOLDER,realfilename.filename),vendorname)

    filedatetimestamp=datetime.datetime.today().strftime("%m%d%Y")
    exportfilename='{0}_{1}.csv'.format(vendorname,filedatetimestamp)
    
    tf_final=tf.replace('nan','').replace('NaT','')
    tf_final.to_csv(os.path.join(UPLOAD_FOLDER,exportfilename),index=False,quoting=csv.QUOTE_MINIMAL)
    print(tf.head())

    return jsonify({"output":"File has been processed"})

@app.route('/api/delegateroster/facilityload',methods=['POST'])
def facilityload():
    print('hello')
    fl=fc.facility_list()
    print(fl)
    
    return jsonify({"output":fl})
