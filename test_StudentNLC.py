import json
import os
from NLC import *



def test_classify():
    nlc = StudentNLC()
    
    query = 'Exit the classroom, please'
    result = nlc.classify(query)
    assert result == 'move to hallway'

    #does not classify with a high confidence - returns 'default'
    query = 'Would you please enter the hallway for me?'
    result = nlc.classify(query)
    assert result == 'default'
    
    query = 'I must exit the classroom immediately!'
    result = nlc.classify(query)
    assert result == 'move to hallway'
    
    #query = 'I must enter the classroom immediately!'
    #result = nlc.classify(query)
    #assert result == 'move to classroom'
    
    query = 'move to the classroom'
    result = nlc.classify(query)
    assert result == 'move to classroom'

    query = 'move to the room'
    result = nlc.classify(query)
    assert result == 'move to classroom'
    
    query = 'talk to that student over there'
    result = nlc.classify(query)
    assert result == 'talk to student'
    
    query = 'hey student! i want you to ask me a question!'
    result = nlc.classify(query)
    assert result == 'talk to student'
    
    query = 'walk to student'
    result = nlc.classify(query)
    assert result == 'talk to student'
    
    query = 'receive next question'
    result = nlc.classify(query)
    assert result == 'talk to student'

    query = 'can you move to the classroom, Please'
    result = nlc.classify(query)
    assert result == 'move to classroom'
