import sys

from Discovery import *

def test_findDocument():
    wat = Watson()
    for docID in docIDToName:
        wat.findDocument(docID)
        
def test_acquireDocument():
    wat = Watson()
    query = "When was the Treaty of Ghent signed?"
    cachedRes = [('98e9b50f1327e045364f669dab17a2ea', 'Peace negotiations began in August 1814 and the <a href="/wiki/Treaty_of_Ghent" title="Treaty of Ghent">Treaty of Ghent</a> was signed on December 24 as neither side wanted to continue fighting. News of the peace did not reach America for some time.'), ('98e9b50f1327e045364f669dab17a2ea', 'At the end of 1814, the British launched a double offensive in the South weeks before the Treaty of Ghent was signed. On the Atlantic coast, Admiral George Cockburn was to close the Intracoastal Waterway trade and land Royal Marine battalions to advance through Georgia to the western territories.'), ('98e9b50f1327e045364f669dab17a2ea', 'The British were then able to increase the strength of the blockade on the United States coast, annihilating American maritime trade and bringing the United States government near to bankruptcy. Peace negotiations began in August 1814 and the Treaty of Ghent was signed on December 24 as neither side wanted to continue fighting.'), ('98e9b50f1327e045364f669dab17a2ea', '</p>\n<p>At the end of 1814, the British launched a double offensive in the South weeks before the Treaty of Ghent was signed. On the <a href="/wiki/Atlantic_Ocean" title="Atlantic Ocean">Atlantic</a> coast, Admiral George Cockburn was to close the <a href'), ('98e9b50f1327e045364f669dab17a2ea', 'They both sent delegations to a neutral site in Ghent, Flanders (now part of Belgium). The negotiations began in early August and concluded on December 24, when a final agreement was signed; both sides had to ratify it before it could take effect.'), ('98e9b50f1327e045364f669dab17a2ea', '. They both sent delegations to a neutral site in Ghent, Flanders (now part of Belgium). The negotiations began in early August and concluded on December 24, when a final agreement was signed; both sides had to ratify it before it could take effect.'), ('27ce78f83dc0d72d96e3f5766736992d', ':\n\nOne property of this form is that it yields one valid root when a = 0, while the other root contains division by zero, because when a = 0, the quadratic equation becomes a linear equation, which has one root.'), ('ad9d680ed1a99a7c856a89991d25d6f7', 'Cells may also temporarily or permanently leave the cell cycle and enter G0 phase to stop dividing. This can occur when cells become overcrowded (density-dependent inhibition) or when they differentiate to carry out specific functions for the organism, as is the case for human heart muscle cells and neurons.'), ('27ce78f83dc0d72d96e3f5766736992d', '\xa0, where b has a magnitude one half of the more common one, possibly with opposite sign. These result in slightly different forms for the solution, but are otherwise equivalent.\n\nA number of alternative derivations can be found in the literature.'), ('27ce78f83dc0d72d96e3f5766736992d', 'content="origin-when-cross-origin" name="referrer"/>\n<link href="android-app://org.wikipedia/http/en.m.wikipedia.org/wiki/Quadratic_equation" rel="alternate"/>\n<link href="/w/index.php?title')]
    wat.cachedQueries[query] = cachedRes
    expectedRes1 = []
    assert wat.ask(query) == expectedRes1
    wat.findDocument('98e9b50f1327e045364f669dab17a2ea')
    expectedRes2 = ['Peace negotiations began in August 1814 and the <a href="/wiki/Treaty_of_Ghent" title="Treaty of Ghent">Treaty of Ghent</a> was signed on December 24 as neither side wanted to continue fighting. News of the peace did not reach America for some time.', 'At the end of 1814, the British launched a double offensive in the South weeks before the Treaty of Ghent was signed. On the Atlantic coast, Admiral George Cockburn was to close the Intracoastal Waterway trade and land Royal Marine battalions to advance through Georgia to the western territories.', 'The British were then able to increase the strength of the blockade on the United States coast, annihilating American maritime trade and bringing the United States government near to bankruptcy. Peace negotiations began in August 1814 and the Treaty of Ghent was signed on December 24 as neither side wanted to continue fighting.']
    assert wat.ask(query) == expectedRes2

def test_badQuery():
    wat = Watson()
    res = wat.ask(";{SELECT * from Students}--")
    assert res == []
