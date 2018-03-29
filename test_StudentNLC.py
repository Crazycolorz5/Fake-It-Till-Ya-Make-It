import json
import os
from NLC import *

#Math/science asking: sam, john, steve, frank, betty, charles
#english/history asking: rest


def test_classify():
    nlc = StudentNLC()
    
    query = 'talk to Francis Bacon'
    result = nlc.classify(query)
    assert result == 'francis bacon'
	
    query = 'say what john doe'
    result = nlc.classify(query)
    assert result == 'john doe'
	
    #query = 'does sam have a question'
    #result = nlc.classify(query)
    #assert result == 'sam winchester'

    # doesnt take first name needs full name 
    query = 'does sam have a question'
    result = nlc.classify(query)
    assert result == 'default'
	
    #testing with last names	
    query = 'what Math question does pierce have'
    result = nlc.classify(query)
    assert result == 'default'
	
    #testing without dash works 	
    query = 'who else have a questions, does lin Manuel Miranda have question'
    result = nlc.classify(query)
    assert result == 'lin-manuel miranda'
	
    query = 'who else have a questions, does lin-Manuel Miranda have question'
    result = nlc.classify(query)
    assert result == 'lin-manuel miranda'
	
	
	
	
	



