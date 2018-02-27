# coding=utf-8
from Discovery import *
import websockets
import asyncio
import _thread


helpstring = '''help: gives a brief description of basic commands user can enter
quit: quits the demo
question: tells you the question your student is currently asking you
answer _: submits an answer to the current question
query _: queries Watson for given keyword/keyphrase
find _: Finds a document to add to the database. Valid documents:
    document 1: A document on the War of 1812
    document 2: A document on Mitosis'''
    
# For answering questions


def answerQuestion(answerNumber, answer):
    if answerNumber == 0:
        return answer == '12/24/1814'
    if answerNumber == 1:
        return answer.lower() == "james madison"
    if answerNumber == 2:
        return answer.lower() == "telophase"
        
        
async def receiveQuestion(websocket, questionNumber):
    if questionNumber == 0:
        await websocket.send("=================================\nWhat date was the treaty of Ghent signed? (format: MM/DD/YYYY)\n=================================\n")
        return
    elif questionNumber == 1:
        await websocket.send("=================================\nWho was the president during the War of 1812? (first and last name)\n=================================\n")
        return
    elif questionNumber == 2:
        await websocket.send("=================================\nWhat is the final phase of mitosis? (one word)\n=================================\n")
        return
    else:
        await websocket.send("All questions answered!")
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


async def websocketHandler(websocket, path):
    print('local address  : {0}'.format(websocket.local_address))
    print('remote address : {0}'.format(websocket.remote_address))

    watson = Watson()
    testDocs = {"document 1" : '98e9b50f1327e045364f669dab17a2ea', "document 2" : 'ad9d680ed1a99a7c856a89991d25d6f7'}
    questionNumber = 0;

    try:
        await websocket.send("You enter the room of your history class. There are students eagerly awaiting your teaching.")
        await websocket.send("Type help for possible commands, or feel free to get started!")

        async for message in websocket:
            print(message)

            words = message.split(' ', 1)
            if len(words) == 0:
                continue
            firstWord = words[0]
            if firstWord.lower() == "help":
                await websocket.send(helpstring)
            elif firstWord.lower() == "quit":
                #quit()
                await websocket.close()
            elif firstWord.lower() == "question":
                await receiveQuestion(websocket, questionNumber)
            elif len(words) == 1:
                await websocket.send("Invalid command! Type \"help\" for a complete list of commands.")
                continue
            else:
                argument = words[1].strip('"')
                if firstWord.lower() == "answer":
                    if questionNumber > 2: await websocket.send("All questions answered!")
                    elif answerQuestion(questionNumber, argument): 
                        await websocket.send("That is a correct answer!")
                        questionNumber += 1
                    else: await websocket.send("That is not a correct answer!")
                elif firstWord.lower() == "query":
                    await websocket.send(formatResponse(watson.ask(argument)))
                elif firstWord.lower() == "find":
                    if argument.lower() in testDocs and testDocs[argument.lower()] in docIDToName:
                        watson.findDocument(testDocs[argument.lower()])
                        await websocket.send("Document successfully added.")
                    else:
                        await websocket.send("Invalid document!")
                else:
                    await websocket.send("Invalid command! Type \"help\" for a complete list of commands.")
    except websockets.exceptions.ConnectionClosed as e:
        quit()



print('listening')
'''
asyncio.get_event_loop().run_until_complete(
    websockets.serve(websocketHandler, 'localhost', 10000))
asyncio.get_event_loop().run_forever()
'''

loop = asyncio.get_event_loop()
asyncio.ensure_future(websockets.serve(websocketHandler, 'localhost', 10000))

def gameLoop():
    loop.run_forever()


_thread.start_new_thread(gameLoop, ())

line = input('>>>')
while (line != 'quit'):
    print(line)
    line = input('>>>')


#name = input("Welcome to Washington Elementary! Please input your name: \n>> ")

#print("Nice to meet you, %s. \nGood luck as your first day as a substitute teacher!\n" % name)




'''
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

'''
