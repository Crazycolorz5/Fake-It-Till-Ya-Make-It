import json
import os
from watson_developer_cloud import NaturalLanguageClassifierV1

naturalLanguageClassifier = NaturalLanguageClassifierV1(
    username='7c40e7b8-3d9e-44d4-91df-48ae2ccfa5c1',
    password='VAfeJBrBkIhd'
)
#Classifiers that need kept for other branches

#classifier "2fbbc6x326-nlc-1451"
#created 03/27 from nlc data 03/23
#classifier '2fbf5cx328-nlc-1775'
#created 03/29 from nlc data 0329

#stduent classifier '539e6dx331-nlc-551'
#created 03/27 from student nlc data 03/27

#subject classifier '2fbbc6x326-nlc-1454'
#created 03/27 from subject nlc data 03/27
#subject classifier '2fbda2x327-nlc-1810'
#created 03/29 from subject nlc data 0329


#Create Classifier - keep commented
#with open('nlc_training_set_0412.csv', 'rb') as training_data:
#    classroomClassifier = naturalLanguageClassifier.create(      
#        training_data = training_data,
#        name = 'nlc0412'
#        )
#print(json.dumps(classifiers, indent=2))

classifiers = naturalLanguageClassifier.list()
#New classifiers
classifierID =        'ab2c7bx342-nlc-478'
studentClassifierID = '2fbf5cx328-nlc-1761'
subjectClassifierID = 'ab2c7bx342-nlc-477'

CONFIDENCE_THRESHOLD = 0.8
STUDENT_CONFIDENCE_THRESHOLD = 0.9
SUBJECT_CONFIDENCE_THRESHOLD = 0.9

class NLC:

    def __init__(self):
        self.classifierID = 'ab2c7bx342-nlc-478'
        self.status = naturalLanguageClassifier.status(self.classifierID)
        self.subject = SubjectNLC()
        self.student = StudentNLC()

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = 'default'
        confidence = None
        if self.status['status'] == 'Available' and string and not string.isspace():

            classes = naturalLanguageClassifier.classify(self.classifierID, string)
            confidence = classes['classes'][0]['confidence']
            #print(classes['top_class'])
            #print(confidence)
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
                    
        return topClass

class StudentNLC:
    def __init__(self):
        self.studentClassifierID = '2fbf5cx328-nlc-1761'
        self.status = naturalLanguageClassifier.status(self.studentClassifierID)

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = 'default'
        confidence = None
        if self.status['status'] == 'Available' and string and not string.isspace():

            classes = naturalLanguageClassifier.classify(self.studentClassifierID, string)
            confidence = classes['classes'][0]['confidence']
            #print(classes['top_class'])
            #print(confidence)
            if confidence > STUDENT_CONFIDENCE_THRESHOLD:
                topClass = classes['top_class']
        return topClass

class SubjectNLC:
    def __init__(self):
        self.subjectClassifierID = 'ab2c7bx342-nlc-477'
        self.status = naturalLanguageClassifier.status(self.subjectClassifierID)

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = 'default'
        confidence = None
        if self.status['status'] == 'Available' and string and not string.isspace():
            classes = naturalLanguageClassifier.classify(self.subjectClassifierID, string)
            confidence = classes['classes'][0]['confidence']
            #print(classes['top_class'])
            #print(confidence)
            if confidence > SUBJECT_CONFIDENCE_THRESHOLD:
                topClass = classes['top_class']
        return topClass
