from Discovery import Watson
from NLC import NLC #TODO: Not a real import.

# This used to be in the demo, just here so we can re-implement the questions for testing.
# For answering questions
#questionNumber = 0;

#def answerQuestion(answerNumber, answer):
    #if answerNumber == 0:
        #return answer == '12/24/1814'
    #if answerNumber == 1:
        #return answer.lower() == "james madison"
    #if answerNumber == 2:
        #return answer.lower() == "telophase"
        
        
#def receiveQuestion(questionNumber):
    #if questionNumber == 0:
        #print("=================================\nWhat date was the treaty of Ghent signed? (format: MM/DD/YYYY)\n=================================\n")
        #return
    #elif questionNumber == 1:
        #print("=================================\nWho was the president during the War of 1812? (first and last name)\n=================================\n")
        #return
    #elif questionNumber == 2:
        #print("=================================\nWhat is the final phase of mitosis? (one word)\n=================================\n")
        #return
    #else:
        #print("All questions answered!")
        #return
        
class PlayerState:
    helpString = '''help: gives a brief description of basic commands user can enter
quit: quits the demo
question: tells you the question your student is currently asking you
answer _: submits an answer to the current question
query _: queries Watson for given keyword/keyphrase'''
    
    def __init__(self, name):
        self.location = Hallway
        self.name = name
        self.questionNumber = 0 #TODO
        self.watson = Watson()

    # act :: (PlayerState, String) -> String
    def act(self, inputString):
        # Do some small string processing.
        words = inputString.split(' ', 1)
        if not words:
            return "No command specified!"
        elif words[0] is "help":
            return PlayerState.helpString
        elif words[0] is "quit":
            quit() #TODO: Handle elsewhere?
        elif words[0] is "query":
            if len(words) == 1:
                return "No query specified!"
            else:
                argument = words[1].strip('"')
                return formatResponse(self.watson.query(argument))
        else:
            nlc = NLC()
            intent = nlc.classify(inputString) #TODO: Fake method
            retStr = self.location.actOnIntent(self, intent)
            return "Invalid command." if retStr is None else retStr
    
    @staticmethod
    def formatResponse(stringArr):
        if len(stringArr) == 0:
            return "No results!"
        i = 1
        acc = ""
        for x in stringArr:
            acc += "Result {0}: {1}\n\n".format(i, x)
            i += 1
        return acc.strip()

class LocationState:
    def __init__(self):
        # commandDictionary :: Dictionary String ((PlayerState, LocationState) -> String)
        self.commandDictionary = dict()
    
    # actOnIntent :: (LocationState, PlayerState, String) -> Maybe String
    def actOnIntent(self, playerState, intent):
        if intent in self.commandDictionary:
            return self.commandDictionary[intent](playerState, self)
        else:
            return None
        
    def leaveHook(self):
        pass

class Student:
    def __init__(self, firstTalk, subsequentTalk, answeredTalk, answer): #, answeredCorrect, answeredIncorrect):
        self.firstTalk = firstTalk
        self.subsequentTalk = subsequentTalk
        self.answeredTalk = answeredTalk
        self.answer = answer
        self.talkedTo = False
        self.answered = False
    def talkTo(self):
        if self.answered:
            return answeredTalk
        elif self.talkedTo:
            return subsequentTalk
        else:
            return firstTalk
    def answer(self, string): #Intend to overwrite?
        if string is self.answer:
            pass #TODO!!
        else:
            pass

def makeMoveCommand(location, msgString):
    def moveCommand(playerState, locationState):
        playerState.location = location
        locationState.leaveHook()
        return msgString
    return moveCommand

Hallway = LocationState()
Classroom = LocationState()

def talkToHallwayStudent(playerState, locationState):
    if locationState.answeredStudent:
        return "Thank you for answering my question!"
    elif locationState.talkedToStudent:
        return "To repeat my question, what date was the treaty of Ghent signed? (format: MM/DD/YYYY)"
    else:
        locationState.talkedToStudent = True;
        return "Hey Prof. {0}, I have a question. What date was the treaty of Ghent signed? (format: MM/DD/YYYY)".format(playerState.name)

    
hallwayCommands = {
    "move to classroom" : makeMoveCommand(Classroom, "You move to the classroom.")
    #"talk to student" : talkToHallwayStudent
    }

Hallway.talkedToStudent = False
Hallway.answeredStudent = False
Hallway.commandDictionary = hallwayCommands


classroomCommands = {
    "move to hallway": makeMoveCommand(Hallway, "You move to the hallway.")
    }

Classroom.commandDictionary = classroomCommands
