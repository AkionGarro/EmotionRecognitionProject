import cv2
from flask import Flask, redirect, url_for, request, jsonify
from firestore import firestoreService, userLogin, userRegister, serviceAdd, adminRegister, phaseProcedure, procedure
from flask_cors import CORS, cross_origin
import mes as me

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/sortImage', methods=['POST', 'GET'])
@cross_origin()
def sortImage():
    fire = firestoreService()
    imageBase64 = request.form.get('imageBase64')
    meetingId = request.form.get('meetingId')
    imagePng = me.base64_to_png(imageBase64)
    img = cv2.imread(imagePng)
    stats = me.predic_one(img,meetingId)
    fire.addSampleByMeetingId(stats)
    print(stats)
    return jsonify(stats)


@app.route('/prueba', methods=['POST', 'GET'])
@cross_origin()
def getChartsInfo():
    fire = firestoreService()
    meetingId = "12345678"
    samples = fire.getSamplesByMeetingId(meetingId)
    return jsonify(samples)


#---------------------------Ejemplo de flask---------------------------
@app.route('/login', methods=['POST', 'GET'])
@cross_origin()
def login():
    fire = firestoreService()
    name = request.form.get('name')
    password = request.form.get('password')
    userLog = userLogin(name, password)
    res = fire.getUser(userLog)
    return jsonify(res)





app.run()