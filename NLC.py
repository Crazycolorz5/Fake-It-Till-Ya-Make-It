import json
import os
from watson_developer_cloud import NaturalLanguageClassifierV1

naturalLanguageClassifier = NaturalLanguageClassifierV1(
    username='7c40e7b8-3d9e-44d4-91df-48ae2ccfa5c1',
    password='VAfeJBrBkIhd'
)
# classifier '8fc642x299-nlc-3055'
# Operational
#move to classroom
#move to hallway
#talk to student

# Inoperational 
#interact with desk
#interact with computer
#look around

# classifier "f7e6f0x306-nlc-174"
# Operational
#move to classroom
#move to hallway
#talk to student
#interact with desk
#interact with computer
#look around
#default

#with open('nlc_training_set_0306.csv', 'rb') as training_data:
#    classroomClassifier = naturalLanguageClassifier.create(      
#        training_data = training_data,
#        )

classifiers = naturalLanguageClassifier.list()
#print(json.dumps(classifiers, indent = 2))

classifierID = 'f7e6f0x306-nlc-174'
status = naturalLanguageClassifier.status(classifierID)

class NLC:

    def __init__(self):
        classifierID = 'f7e6f0x306-nlc-174'
        status = naturalLanguageClassifier.status(classifierID)

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = 'default'
        confidence = None
        if status['status'] == 'Available':
            classes = naturalLanguageClassifier.classify(classifierID, string)
            confidence = classes['classes'][0]['confidence']
            print(classes['top_class'])
            print(confidence)
            if confidence > 0.8:
                topClass = classes['top_class']
        return topClass
