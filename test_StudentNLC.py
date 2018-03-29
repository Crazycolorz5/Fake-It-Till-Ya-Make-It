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
	
    query = 'does sam have a question'
    result = nlc.classify(query)
    assert result == 'sam winchester'
	
    query = 'what Math question does Frank have'
    result = nlc.classify(query)
    assert result == 'frank Pierce'
	
    query = 'who else have a questions, does lin have question'
    result = nlc.classify(query)
    assert result == 'lin-Manuel Miranda'
	
	
	
	
	



