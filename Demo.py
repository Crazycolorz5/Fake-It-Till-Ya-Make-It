# coding=utf-8
from Discovery import *

helpstring = '''help: gives a brief description of basic commands user can enter
quit: quits the demo
question: tells you the question your student is currently asking you
answer _: submits an answer to the current question
query _: queries Watson for given keyword/keyphrase
find _: Finds a document to add to the database. Valid documents:
    document 1: A document on the War of 1812
    document 2: A document on Mitosis'''
    
# For answering questions
questionNumber = 0;

def answerQuestion(answerNumber, answer):
    if answerNumber == 0:
        return answer == '12/24/1814'
    if answerNumber == 1:
        return answer.lower() == "james madison"
    if answerNumber == 2:
        return answer.lower() == "telophase"
        
        
def receiveQuestion(questionNumber):
    if questionNumber == 0:
        print("=================================\nWhat date was the treaty of Ghent signed? (format: MM/DD/YYYY)\n=================================\n")
        return
    elif questionNumber == 1:
        print("=================================\nWho was the president during the War of 1812? (first and last name)\n=================================\n")
        return
    elif questionNumber == 2:
        print("=================================\nWhat is the final phase of mitosis? (one word)\n=================================\n")
        return
    else:
        print("All questions answered!")
        return

def formatResponse(stringArr):
    if len(stringArr) == 0:
        return "No results!"
    i = 1
    acc = ""
    for x in stringArr:
        acc += "Result {0}: {1}\n\n".format(i, x)
        i += 1
    return acc.strip()

name = input("Welcome to Washington Elementary! Please input your name: \n>> ")

watson = Watson()

testDocs = { "document 1" : '98e9b50f1327e045364f669dab17a2ea',
             "document 2" : 'ad9d680ed1a99a7c856a89991d25d6f7'}

print("Nice to meet you, %s. \nGood luck as your first day as a substitute teacher!\n" % name)

print("You enter the room of your history class. There are students eagerly awaiting your teaching.\n")

print("Type help for possible commands, or feel free to get started!")

while True:
    currentLine = input(">> ")
    words = currentLine.split(' ', 1)
    if len(words) == 0:
        continue
    firstWord = words[0]
    if firstWord.lower() == "help":
        print(helpstring)
    elif firstWord.lower() == "quit":
        quit()
    elif firstWord.lower() == "question":
        receiveQuestion(questionNumber)
    elif len(words) == 1:
            print("Invalid command! Type \"help\" for a complete list of commands.")
            continue
    else:
        argument = words[1].strip('"')
        if firstWord.lower() == "answer":
            if questionNumber > 2: print("All questions answered!")
            elif answerQuestion(questionNumber, argument): 
                print("That is a correct answer!")
                questionNumber += 1
            else: print("That is not a correct answer!")
        elif firstWord.lower() == "query":
            print(formatResponse(watson.ask(argument)))
        elif firstWord.lower() == "find":
            #if argument.lower() in testDocs and testDocs[argument.lower()] not in docIDToName:
                #print("Invalid document!")
            if argument.lower() in testDocs and testDocs[argument.lower()] in docIDToName:
                watson.findDocument(testDocs[argument.lower()])
                print("Document successfully added.")
            else:
                print("Invalid document!")
        else:
            print("Invalid command! Type \"help\" for a complete list of commands.")



# Unreachable previous demo code:

# Player types help

input("room contents: Looks around the room and tells you possible interactable objects\n" + 
    "help: gives a brief description of basic commands user can enter \n" +
    "move x: moves focus of subsitute teacher to content x\n" + 
    "query x: queries Watson for keyword/keyphrase x\n>>")

# Player types room contents

input("You find yourself in a 5th grade history classroom. \n" +
"There is a student with her hand raised, awaiting your help\n" + 
"There is the teacher's desk, the surface clean, but there is a drawer as well\n>>")

# Player types talk to student

input("The student asks you: \"So, before class starts, what date exactly\n" +
"did the War of 1812 end?\"\n>>")

#We don't know, so we ask Watson
#query War of 1812 
input("No information found. Try looking for documents with this information.\n>>")

# The treaty was unanimously ratified by the United States on February 17, 1815, ending the war with Status quo ante bellum (no boundary changes).

# Player says open drawer

input("You open the drawer and find the teacher's notes about the War of 1812.\nThis document has been added to Watson Discovery.\n>>")

# Player types talk to student

input("The student asks you: \"So, before class starts, what date exactly\n" +
"did the War of 1812 end?\"\n>>")

# query War of 1812

print("\"The War of 1812 ended on February 7th, 1815\" Watson tells you, and you relay this to the student.\nThe bell rings. Now comes the easy part.\nYou tell the students they have the whole class to free read.\nYou have just finished your first challenge as a substitute teacher.\nWell done!")
