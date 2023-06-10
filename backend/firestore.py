import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


#clases y ejemplos de modelos
class userLogin():
    def __init__(self, username, password):
        self.username = username
        self.password = password


class userRegister():
    def __init__(self, name, email, username, password, typeUser, address, telephone, tourismSector):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.typeUser = typeUser
        self.address = address
        self.telephone = telephone
        self.tourismSector = tourismSector


class adminRegister():
    def __init__(self, name, email, username, password, telephone):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.telephone = telephone


class phaseProcedure():
    def __init__(self, phase, serviceId):
        self.phase = phase
        self.serviceId = serviceId


class procedure():
    def __init__(self, id, name, category, description):
        self.id = id
        self.name = name
        self.category = category
        self.description = description


class serviceAdd():
    def __init__(self, companyDescription, serviceDescription, serviceType, username):
        self.companyDescription = companyDescription
        self.serviceDescription = serviceDescription
        self.serviceType = serviceType
        self.username = username


class firestoreService():

    def __init__(self):
        self.cred = credentials.Certificate('emotionKey.json')
        
        try:
            self.app = firebase_admin.get_app()
        except ValueError:
            self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    # Add document using know id, change document to document(user['name'])
    def addMeeting(self, data):
        checkMeeting = self.db.collection('Meetings').where("Id", "==", data.meetingId).get()
        if checkMeeting == []:
            doc_ref = self.db.collection(u'Meetings').document(data.meetingId)
            doc_ref.set({
                'Focused': data.detected_probability,
                'Emotion': data.emotion,
                'Engaged proba': data.engaged,
            })
            res = {'result': 'Sucess'}
            return res
        else:
            res = {'result': 'Change Username'}
            return res




    def addUser(self, user):
        checkUser = self.db.collection('users').where("username", "==", user.username).get()
        if checkUser == []:
            doc_ref = self.db.collection(u'users').document(user.username)
            doc_ref.set({
                'name': user.name,
                'email': user.email,
                'username': user.username,
                'password': user.password,
                'typeUser': user.typeUser,
                'address': user.address,
                'telephone': user.telephone,
                'tourismSector': user.tourismSector,
                'access': 'user'
            })
            res = {'result': 'Sucess'}
            return res
        else:
            res = {'result': 'Change Username'}
            return res

    def addAdmin(self, user):
        checkUser = self.db.collection('users').where("username", "==", user.username).get()
        if checkUser == []:
            doc_ref = self.db.collection(u'users').document(user.username)
            doc_ref.set({
                'name': user.name,
                'email': user.email,
                'username': user.username,
                'password': user.password,
                'telephone': user.telephone,
                'access': 'admin'
            })
            res = {'result': 'Sucess'}
            return res
        else:
            res = {'result': 'Change Username'}
            return res

    def getUsers(self):
        users = []
        users_ref = self.db.collection('users')
        docs = users_ref.stream()
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')
            users.append(doc.to_dict())
        return users

    # getUser with name and password
    def getUser(self, user):
        docRef = self.db.collection('users').where("username", "==", user.username).get()
        if docRef != []:
            userRes = docRef[0].to_dict()
            if userRes['password'] == user.password:
                print(userRes)
                return userRes
            else:
                print('Wrong Password')
                return None;
        else:
            print('No se encuentra el usuario')
            return None;

    def addService(self, service):
        doc_ref = self.db.collection('services').document()
        doc_ref.set({
            'serviceDescription': service.serviceDescription,
            'companyDescription': service.companyDescription,
            'serviceType': service.serviceType,
            'username': service.username,
            'id': doc_ref.id,
            'created': firestore.SERVER_TIMESTAMP
        })
        res = {'result': 'Success',
               'Id': doc_ref.id}
        return res

    def getUserServices(self, username):
        docs = self.db.collection('services').where("username", "==", username).get()
        services = []
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')
            services.append(doc.to_dict())
        return services

    def getServiceById(self, id):
        docs = self.db.collection('services').where("id", "==", id).get()
        if docs != []:
            serviceRes = docs[0].to_dict()
            return serviceRes
        else:
            print('No se encuentra el usuario')
            return None;

    def getAdminServices(self):
        docs = self.db.collection('services').get()
        services = []
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')
            services.append(doc.to_dict())
        return services

    def getProcedures(self, phaseP):
        docs = self.db.collection('phases').where("category", "==", phaseP.phase).where("id", "==",
                                                                                        phaseP.serviceId).get()
        phases = []
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')
            phases.append(doc.to_dict())
        return phases

    def addProcedure(self, prod):
        doc_ref = self.db.collection('phases').document()
        doc_ref.set({
            'category': prod.category,
            'date': firestore.SERVER_TIMESTAMP,
            'description': prod.description,
            'id': prod.id,
            'name': prod.name,
            'status': 'active',
            'idProcedure': doc_ref.id,
        })
        res = {'result': 'Success',
               'Id': doc_ref.id}
        return res

    def getProcedureId(self, id):
        docs = self.db.collection('phases').where("idProcedure", "==", id).get()
        if docs != []:
            procedure = docs[0].to_dict()
            return procedure
        else:
            print('No se encuentra')
            return None;



#def main():
#    user = userRegister('Akion', 'carloscamp1008@gmail.com', 'Garrido', '1234',
#                        'admin', 'san juan', '85045830', 'tourismSector')
#    fire = firestoreService()
#    res = fire.addUser(user)
#    print(res)

#main()