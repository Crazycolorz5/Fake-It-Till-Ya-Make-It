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

#stduent classifier '539e6dx331-nlc-551'
#created 03/27 from student nlc data 03/27

#subject classifier '2fbbc6x326-nlc-1454'
#created 03/27 from subject nlc data 03/27


#Create Classifier - keep commented
#with open('subject_nlc_training_set_0329.csv', 'rb') as training_data:
#    classroomClassifier = naturalLanguageClassifier.create(      
#        training_data = training_data,
#        name = 'subject0329'
#        )
#print(json.dumps(classifiers, indent=2))

classifiers = naturalLanguageClassifier.list()
#New classifiers
classifierID =        '2fbf5cx328-nlc-1775'
studentClassifierID = '2fbf5cx328-nlc-1761'
subjectClassifierID = '2fbda2x327-nlc-1810'

CONFIDENCE_THRESHOLD = 0.8
STUDENT_CONFIDENCE_THRESHOLD = 0.9
SUBJECT_CONFIDENCE_THRESHOLD = 0.9

class NLC:

    def __init__(self):
        classifierID = '2fbf5cx328-nlc-1775'
        self.status = naturalLanguageClassifier.status(classifierID)

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = 'default'
        confidence = None
        if self.status['status'] == 'Available' and string and not string.isspace():

            classes = naturalLanguageClassifier.classify(classifierID, string)
            confidence = classes['classes'][0]['confidence']
            #print(classes['top_class'])
            #print(confidence)
            if confidence > CONFIDENCE_THRESHOLD:
                topClass = classes['top_class']
        return topClass

class StudentNLC:
    def __init__(self):
        studentClassifierID = '2fbf5cx328-nlc-1761'
        self.status = naturalLanguageClassifier.status(studentClassifierID)

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = 'default'
        confidence = None
        if self.status['status'] == 'Available' and string and not string.isspace():

            classes = naturalLanguageClassifier.classify(studentClassifierID, string)
            confidence = classes['classes'][0]['confidence']
            #print(classes['top_class'])
            #print(confidence)
            if confidence > STUDENT_CONFIDENCE_THRESHOLD:
                topClass = classes['top_class']
        return topClass

class SubjectNLC:
    def __init__(self):
        subjectClassifierID = '2fbda2x327-nlc-1810'
        self.status = naturalLanguageClassifier.status(subjectClassifierID)

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = 'default'
        confidence = None
        if self.status['status'] == 'Available' and string and not string.isspace():
            classes = naturalLanguageClassifier.classify(subjectClassifierID, string)
            confidence = classes['classes'][0]['confidence']
            #print(classes['top_class'])
            #print(confidence)
            if confidence > SUBJECT_CONFIDENCE_THRESHOLD:
                topClass = classes['top_class']
        return topClass
