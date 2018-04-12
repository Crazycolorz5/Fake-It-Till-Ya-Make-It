import json
import os
from watson_developer_cloud import NaturalLanguageClassifierV1

naturalLanguageClassifier = NaturalLanguageClassifierV1(
    username='7c40e7b8-3d9e-44d4-91df-48ae2ccfa5c1',
    password='VAfeJBrBkIhd'
)
#Classifiers that need kept for other branches

#classifier "2fbf5cx328-nlc-1775"
#created 03/29 from nlc data 03/29

#stduent classifier '2fbf5cx328-nlc-1761'
#created 03/29 from student nlc data 03/29

#subject classifier '2fbda2x327-nlc-1810'
#created 03/29 from subject nlc data 03/29


#Create Classifier - keep commented
#with open('nlc_training_set_0412.csv', 'rb') as training_data:
#    classroomClassifier = naturalLanguageClassifier.create(      
#        training_data = training_data,
#        name = 'nlc0412'
#        )
#print(json.dumps(classifiers, indent=2))
#classifiers = naturalLanguageClassifier.list()
#New classifiers
classifierID =        'ad3f68x345-nlc-417'
studentClassifierID = 'ab2f65x344-nlc-484'
subjectClassifierID = 'ab2f65x344-nlc-483'

CONFIDENCE_THRESHOLD = 0.8
STUDENT_CONFIDENCE_THRESHOLD = 0.9
SUBJECT_CONFIDENCE_THRESHOLD = 0.9

class NLC:

    def __init__(self):
        classifierID = 'ad3f68x345-nlc-417'
        self.status = tryStatus(classifierID)
        self.subject = SubjectNLC()
        self.student = StudentNLC()

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = 'default'
        confidence = None
        if self.status and self.status['status'] == 'Available' and string and not string.isspace():
            classes = naturalLanguageClassifier.classify(classifierID, string)
            confidence = classes['classes'][0]['confidence']
            if confidence > CONFIDENCE_THRESHOLD:
                topClass = classes['top_class']
            #send to StudentNLC/SubjectNLC if needed
            if topClass == 'move to classroom':
                #print('In subject')
                tempClass = self.subject.classify(string)
                if tempClass != 'default' and tempClass != 'cancel':
                    topClass = tempClass

            if topClass == 'talk to student':
                #print('In student')
                tempClass = self.student.classify(string)
                if tempClass != 'default' and tempClass != 'cancel':
                    topClass = tempClass
        elif not self.status:
            topClass = string
        return topClass

class StudentNLC:
    def __init__(self):
        studentClassifierID = 'ab2f65x344-nlc-484'
        self.status = tryStatus(studentClassifierID)

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = 'default'
        confidence = None
        if self.status and self.status['status'] == 'Available' and string and not string.isspace():

            classes = naturalLanguageClassifier.classify(studentClassifierID, string)
            confidence = classes['classes'][0]['confidence']
            #print(classes['top_class'])
            #print(confidence)
            if confidence > STUDENT_CONFIDENCE_THRESHOLD:
                topClass = classes['top_class']
        elif not self.status:
            topClass = string
        return topClass

class SubjectNLC:
    def __init__(self):
        subjectClassifierID = 'ab2f65x344-nlc-483'
        self.status = tryStatus(subjectClassifierID)

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = 'default'
        confidence = None
        if self.status and self.status['status'] == 'Available' and string and not string.isspace():
            classes = naturalLanguageClassifier.classify(subjectClassifierID, string)
            confidence = classes['classes'][0]['confidence']
            #print(classes['top_class'])
            #print(confidence)
            if confidence > SUBJECT_CONFIDENCE_THRESHOLD:
                topClass = classes['top_class']
        elif not self.status:
            topClass = string
        return topClass

def tryStatus(id):
    try:
        return naturalLanguageClassifier.status(id)
    except:
        return None
