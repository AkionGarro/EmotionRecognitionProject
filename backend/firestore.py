import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class firestoreService():

    def __init__(self):
        self.cred = credentials.Certificate('emotionKey.json')
        
        try:
            self.app = firebase_admin.get_app()
        except ValueError:
            self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()


    def addMeeting(self, data):
        checkMeeting = self.db.collection('Meetings').where("Id", "==", data["Id"]).get()
        if checkMeeting == []:
            doc_ref = self.db.collection(u'Meetings').document(data["Id"])
            doc_ref.set({
                'EmotionsInfo': data["EmotionsInfo"],
                'EngagedInfo': data["EngagedInfo"],
                'Focused': data["Focused"],
            })
            res = {'result': 'Sucess'}
            return res
        else:
            res = {'result': 'Change Username'}
            return res

    def addSampleByMeetingId(self, data):
        doc_ref = self.db.collection('Meetings').document()
        doc_ref.set({
            'MeetingID': data["Id"],
            'EmotionsInfo': data["EmotionsInfo"],
            'EngagedInfo': data["EngagedInfo"],
            'Focused': data["Focused"],
        })
        res = {'result': 'Sucess'}
        return res

    def getSamplesByMeetingId(self, meetingId):
        docs = self.db.collection('Meetings').where("MeetingID", "==", meetingId).get()
        samples = []
        for doc in docs:
            #print(f'{doc.id} => {doc.to_dict()}')
            samples.append(doc.to_dict())
        return samples



#def main():
#    user = userRegister('Akion', 'carloscamp1008@gmail.com', 'Garrido', '1234',
#                        'admin', 'san juan', '85045830', 'tourismSector')
#    fire = firestoreService()
#    res = fire.addUser(user)
#    print(res)

#main()