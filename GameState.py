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

WAR_OF_1812_DOCUMENT = '98e9b50f1327e045364f669dab17a2ea'
MITOSIS_DOCUMENT = 'ad9d680ed1a99a7c856a89991d25d6f7'
        
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
        elif words[0] == "query":
            if len(words) == 1:
                return "No query specified!"
            else:
                argument = words[1].strip('"')
                return PlayerState.formatResponse(self.watson.ask(argument))
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

def classroomLookaround(playerState, locationState):
    studentStatus = "There's a student looking at a diagram of cells, loking somewhat confused." if not locationState.student.answered else "There's the student you answered, sitting at their desk."
    deskStatus = "There's a teacher's desk." if not locationState.gotNotes else "There's a teacher's desk, where you got the lecture notes from."
    computerStatus = "There are several computers in the corner of the room, presumably for students to use during a free period." if not locationState.gotWikipedia else "There are several computers, including the one you get the Wikipedia article from. You have to remember to tell your students not to cite Wikipedia."
    door = "There is a door to the hallway."
    return "%s\n%s\n%s\n%s" % (studentStatus, deskStatus, computerStatus, door)

def classroomDesk(playerState, locationState):
    if locationState.gotNotes:
        return "You've already gotten the lecture notes from the teacher's desk."
    else:
        locationState.gotNotes = True
        playerState.watson.findDocument(WAR_OF_1812_DOCUMENT)
        return "You open the drawer and grab the lecture notes the regular teacher left you. To reduce prep time, you pull out your phone, take a picture of the notes, and send it to IBM Watson for analysis.\nYou got a document on the War of 1812!"

def classroomComputer(playerState, locationState):
    if locationState.gotWikipedia:
        return "You have no further use for the computer at this time."
    elif locationState.student.talkedTo:
        locationState.gotWikipedia = True
        playerState.watson.findDocument(MITOSIS_DOCUMENT)
        return "As per the student's request, you search the web for an article on mitosis.\nYou grab the Wikipedia page and send it to IBM Watson for analysis.\nYou got a document on mitosis!"
    else:
        return "You have no reason to use a computer at the moment."

classroomCommands = {
    "move to hallway": makeMoveCommand(Hallway, "You move to the hallway."),
    "talk to student" : talkToStudent,
    "look around" : classroomLookaround,
    "interact with desk" : classroomDesk,
    "interact with computer" : classroomComputer
    }

Classroom.gotNotes = False
Classroom.gotWikipedia = False
Classroom.commandDictionary = classroomCommands
Classroom.student = Student("Hey there Prof! Say, since you're just subbing, could you help me with this question on my Biology homework? What's the final phase of mitosis? (format: all lowercase)",
                            "The question was, what's the final phase of mitosis?",
                            "Thanks for the help!",
                            "telophase",
                            "Yeah, I do think the notes said something like that.",
                            "I don't think that sounds right.")
