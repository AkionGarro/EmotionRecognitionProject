import cv2
from flask import Flask, redirect, url_for, request, jsonify
from firestore import firestoreService, userLogin, userRegister, serviceAdd, adminRegister, phaseProcedure, procedure
from flask_cors import CORS, cross_origin
import mes as me

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/hello', methods=['POST', 'GET'])
@cross_origin()
def hello():

    res = {'hello':'pai'}
    return jsonify(res)


@app.route('/sortImage', methods=['POST', 'GET'])
@cross_origin()
def sortImage():
    imageBase64 = request.form.get('imageBlob')
    imagePng = me.base64_to_png(imageBase64)
    img = cv2.imread(imagePng)
    stats = me.predic_one(img,'a')
    print(stats)
    return jsonify(stats)











@app.route('/login', methods=['POST', 'GET'])
@cross_origin()
def login():
    fire = firestoreService()
    name = request.form.get('name')
    password = request.form.get('password')
    userLog = userLogin(name, password)
    res = fire.getUser(userLog)
    return jsonify(res)




@app.route('/register', methods=['POST', 'GET'])
@cross_origin()
def register():
    fire = firestoreService()
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    userType = request.form.get('userType')
    address = request.form.get('address')
    telephone = request.form.get('telephone')
    tourismSector = request.form.get('tourismSector')
    userLog = userRegister(name, email, username, password, userType, address, telephone, tourismSector)
    res = fire.addUser(userLog)
    return jsonify(res)


@app.route('/service', methods=['POST', 'GET'])
@cross_origin()
def service():
    fire = firestoreService()
    serviceDescription = request.form.get('serviceDescription')
    companyDescription = request.form.get('companyDescription')
    serviceType = request.form.get('serviceType')
    username = request.form.get('username')
    serv = serviceAdd(companyDescription, serviceDescription, serviceType, username)
    res = fire.addService(serv)
    return jsonify(res)


@app.route('/userServices', methods=['POST', 'GET'])
@cross_origin()
def userServices():
    fire = firestoreService()
    username = request.form.get('username')
    res = fire.getUserServices(username)
    return jsonify(res)

@app.route('/serviceById', methods=['POST', 'GET'])
@cross_origin()
def getServiceId():
    fire = firestoreService()
    id = request.form.get('id')
    res = fire.getServiceById(id)
    return jsonify(res)



@app.route('/adminServices', methods=['POST', 'GET'])
@cross_origin()
def adminServices():
    fire = firestoreService()
    res = fire.getAdminServices()
    return jsonify(res)


@app.route('/adminRegister', methods=['POST', 'GET'])
@cross_origin()
def addAdmin():
    fire = firestoreService()
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    telephone = request.form.get('telephone')
    userLog = adminRegister(name, email, username, password,telephone)
    res = fire.addAdmin(userLog)
    return jsonify(res)

@app.route('/servicePhase', methods=['POST', 'GET'])
@cross_origin()
def getPhaseProcedure():
    fire = firestoreService()
    phase = request.form.get('phase')
    serviceId = request.form.get('serviceId')
    serviceId = serviceId[1:-1]
    phaseObj = phaseProcedure(phase,serviceId)
    res = fire.getProcedures(phaseObj)
    return jsonify(res)



@app.route('/newProcedure', methods=['POST', 'GET'])
@cross_origin()
def newProcedure():
    fire = firestoreService()
    category = request.form.get('category')
    description = request.form.get('description')
    id = request.form.get('id')
    id = id[1:-1]
    name = request.form.get('name')
    phaseObj = procedure(id,name,category,description)
    res = fire.addProcedure(phaseObj)
    return jsonify(res)
@app.route('/procedureById', methods=['POST', 'GET'])
@cross_origin()
def getProcedureById():
    fire = firestoreService()
    idProd = request.form.get('idProcedure')
    res = fire.getProcedureId(idProd)
    return jsonify(res)



app.run()