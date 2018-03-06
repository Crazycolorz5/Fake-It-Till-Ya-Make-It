import json
import os
from watson_developer_cloud import NaturalLanguageClassifierV1

naturalLanguageClassifier = NaturalLanguageClassifierV1(
    username='7c40e7b8-3d9e-44d4-91df-48ae2ccfa5c1',
    password='VAfeJBrBkIhd'
)


#move to classroom
#move to hallway
#talk to student
#interact with desk
#interact with computer
#look around


#with open('nlc_training_set.csv', 'rb') as training_data:
#    classroomClassifier = natural_language_classifier.create_classifier(      
#        metadata = json.dumps({'name': 'timebox3-classifier', 'language': 'en'}),
#        training_data = training_data
#        )

classifiers = naturalLanguageClassifier.list()
print(json.dumps(classifiers, indent = 2))

classifierID = '8fc642x299-nlc-3055'
status = naturalLanguageClassifier.status(classifierID)

class NLC:

    def __init__(self):
        pass

    #returns the intent of the classifier given a string
    def classify(self, string):
        topClass = None
        if status['status'] == 'Available':
            classes = naturalLanguageClassifier.classify(classifierID, string)
            topClass = classes['top_class']
        return topClass
