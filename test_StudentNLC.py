import json
import os
from NLC import *



def test_classify():
    nlc = StudentNLC()

	
	query = 'talk Francis Bacon'
	result = StudentNLC.classify(query)
	assert result == 'Francis Bacon'
	
	
