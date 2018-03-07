from Discovery import Watson
from NLC import NLC

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
answer _: submits an answer to the current question
query _: queries Watson for given keyword/keyphrase'''
    
    def __init__(self, name):
        self.location = Hallway
        self.name = name
        self.questionNumber = 0 #TODO
        self.watson = Watson()
        self.nlc = NLC()

    # act :: (PlayerState, String) -> String
    def act(self, inputString):
        # Do some small string processing.
        words = inputString.split(' ', 1)
        if not words:
            return "No command specified!"
        elif words[0] == "help":
            return PlayerState.helpString
        elif words[0] == "quit":
            quit() #TODO: Handle elsewhere?
        elif words[0] == "query":
            if len(words) == 1:
                return "No query specified!"
            else:
                argument = words[1].strip('"')
                return PlayerState.formatResponse(self.watson.query(argument))
        elif words[0] == "answer":
            if len(words) == 1:
                return "No answer specified!"
            else:
                return self.location.answer(words[1])
        else:
            intent = self.nlc.classify(inputString) #TODO: Fake method
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
        self.student = None
        self.talkedToStudent = False

    # actOnIntent :: (LocationState, PlayerState, String) -> Maybe String
    def actOnIntent(self, playerState, intent):
        if intent in self.commandDictionary:
            return self.commandDictionary[intent](playerState, self)
        else:
            return None
        
    def answer(self, string):
        if self.student is None:
            return "No student to answer!"
        elif not self.student.talkedTo:
            return "You haven't heard what this student has to say yet!"
        else:
            return self.student.answer(string)
        
    def leaveHook(self):
        pass

class Student:
    def __init__(self, firstTalk, subsequentTalk, answeredTalk, answer, answeredCorrect, answeredIncorrect):
        self.firstTalk = firstTalk
        self.subsequentTalk = subsequentTalk
        self.answeredTalk = answeredTalk
        self.correctAnswer = answer
        self.talkedTo = False
        self.answered = False
        self.answeredCorrect = answeredCorrect
        self.answeredIncorrect = answeredIncorrect
    def talkTo(self):
        if self.answered:
            return self.answeredTalk
        elif self.talkedTo:
            return self.subsequentTalk
        else:
            self.talkedTo = True
            return self.firstTalk
    def answer(self, string): #Intend to overwrite?
        if string.strip() == self.correctAnswer: #TODO: Better answer validation
            self.answered = True
            return self.answeredCorrect
        else:
            return self.answeredIncorrect

def makeMoveCommand(location, msgString):
    def moveCommand(playerState, locationState):
        playerState.location = location
        locationState.leaveHook()
        return msgString
    return moveCommand

Hallway = LocationState()
Classroom = LocationState()

def talkToStudent(playerState, locationState):
    return locationState.student.talkTo();

def hallwayLookaround(playerState, locationState): 
    if locationState.student.answered:
        return "You see the student whose question you answered. There is also a door to the singular classroom of the school."
    else:
        return "There's a student who appears to want to ask you a question. There is also a door to the singular classroom of the school."
    
hallwayCommands = {
    "move to classroom" : makeMoveCommand(Classroom, "You move to the classroom."),
    "talk to student" : talkToStudent,
    "look around" : hallwayLookaround
    }

Hallway.commandDictionary = hallwayCommands
Hallway.student = Student("Hey Prof., I have a question. What date was the treaty of Ghent signed? (format: MM/DD/YYYY)", #TODO: Allow replacing with player name.
                          "To repeat my question, what date was the treaty of Ghent signed? (format: MM/DD/YYYY)",
                          "Thank you for answering my question!",
                          '12/24/1814',
                          "Thanks for that answer!",
                          "Hm, I don't think that's quite right...")



classroomCommands = {
    "move to hallway": makeMoveCommand(Hallway, "You move to the hallway."),
    "talk to sudent" : talkToStudent
    }

Classroom.commandDictionary = classroomCommands
