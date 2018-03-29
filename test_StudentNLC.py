import json
import os
from NLC import *



def test_classify():
    nlc = studentNLC()
    
    query = 'talk to Francis Bacon'
    result = nlc.classify(query)
    assert result == 'Francis Bacon'


