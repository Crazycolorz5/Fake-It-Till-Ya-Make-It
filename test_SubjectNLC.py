import json
import os
from NLC import *

#Math/science asking: sam, john, steve, frank, betty, charles
#english/history asking: rest


def test_classify():
    nlc = SubjectNLC()
    
    query = 'does anyone have a math question'
    result = nlc.classify(query)
    assert result == 'default'

    query = 'does anyone have a Mathematics question'
    result = nlc.classify(query)
    assert result == 'default'
	
	
	
	
	
	



