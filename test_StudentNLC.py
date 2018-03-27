import json
import os
from NLC import *



def test_classify():
    nlc = StudentNLC()

	
	query = 'talk Francis Bacon'
	result = nlc.classify(query)
	assert result == 'Francis Bacon'
	
	
