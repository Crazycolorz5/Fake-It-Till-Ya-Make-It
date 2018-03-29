import json
import os
from NLC import *

#Math/science asking: sam, john, steve, frank, betty, charles
#english/history asking: rest


def test_classify():
    nlc = SubjectNLC()
    
    query = 'What questions does frank have'
    result = nlc.classify(query)
    assert result == 'math'
	
	
	
	
	
	



