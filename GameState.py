from Discovery import Watson
from NLC import *
from StateBase import *
from BiologyClassroom import makeBiologyClassroom
from MathClassroom import makeMathClassroom
from PhysicsClassroom import makePhysicsClassroom
from LiteratureClassroom import makeLiteratureClassroom
from USHistoryClassroom import makeUSHistoryClassroom
from WorldHistoryClassroom import makeWorldHistoryClassroom
from ArtsHallway import makeArtsHallway
from SciencesHallway import makeSciencesHallway

class Player:
    helpString = '''help: gives a brief description of basic commands user can enter
quit: quits the demo
answer _: submits an answer to the current question
query _: queries Watson for given keyword/keyphrase
You can look around to see the environment around you.
Otherwise, just say what you want to do!'''
    
    def __init__(self, name):
        self.name = name
        self.watson = Watson()
        self.nlc = NLC()
        self.studentNLC = StudentNLC()
        self.subjectNLC = SubjectNLC()
        self.gameState = GameState(name)
        self.location = self.gameState.SciencesHallway
        self.lastStudent = None
        self.state = PlayerState.DEFAULT

    # act :: (Player, String) -> String
    def act(self, inputString):
        # Do some small string processing.
        words = inputString.split(' ', 1)
        if not words:
            return "No command specified!"
        elif words[0] == "help":
            return Player.helpString
        elif words[0] == "query":
            if len(words) == 1:
                return "No query specified!"
            else:
                argument = words[1].strip('"')
                return Player.formatResponse(self.watson.ask(argument))
        elif words[0] == "answer":
            if len(words) == 1:
                return "No answer specified!"
            elif self.lastStudent == None:
                return "You have not spoken to a student!"
            elif not self.lastStudent.talkedTo:
                return "You haven't heard what this student has to say yet!"
            else:
                return self.lastStudent.answer(words[1])        
        else:
            if self.state == PlayerState.DEFAULT:
                self.lastStudent = None #Will be set later if we are to talk to a student.
                intent = self.nlc.classify(inputString)
                retStr = self.location.actOnIntent(self, intent)
                return "Invalid command." if retStr is None else retStr
            elif self.state == PlayerState.CHOOSE_ROOM:
                classifiedClassroom = self.subjectNLC.classify(inputString)
                connections = self.location.classrooms
                if classifiedClassroom in connections:
                    self.location = connections[classifiedClassroom]
                    self.state = PlayerState.DEFAULT
                    return "You move to the %s classroom." % classifiedClassroom.title()
                else:
                    self.state = PlayerState.DEFAULT
                    return "That's an invalid classroom. You decide against moving for now."                
            elif self.state == PlayerState.CHOOSE_STUDENT:
                classifiedName = self.studentNLC.classify(inputString)
                if classifiedName == "cancel":
                    self.state = PlayerState.DEFAULT
                    return "You decide against talking to a student right now."
                studentList = self.location.students
                for student in studentList:
                    if student.name.casefold() == classifiedName.casefold(): 
                        #Note: Student names (to the classifier) are case-insensitive, but commands ARE.
                        self.lastStudent = student
                        self.state = PlayerState.DEFAULT
                        return student.talkTo() #breaks control flow.
                return "Invalid student name. Please try again." #Note no state change.
    
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

class GameState:
    def __init__(self, playerName):
        self.BiologyClassroom = makeBiologyClassroom()
        self.MathClassroom = makeMathClassroom()
        self.PhysicsClassroom = makePhysicsClassroom()
        self.LitClassroom = makeLiteratureClassroom()
        self.USHistClassroom = makeUSHistoryClassroom()
        self.WorldHistClassroom = makeWorldHistoryClassroom()
        
        self.SciencesHallway = makeSciencesHallway({ "math" : self.MathClassroom, "biology" : self.BiologyClassroom, "physics" : self.PhysicsClassroom })
        self.ArtsHallway = makeArtsHallway({ "us history" : self.USHistClassroom, "world history" : self.WorldHistClassroom, "literature" : self.LitClassroom })
