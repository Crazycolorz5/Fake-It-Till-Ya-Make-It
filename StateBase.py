from functools import *

WAR_OF_1812_DOCUMENT = '98e9b50f1327e045364f669dab17a2ea'
MITOSIS_DOCUMENT = 'ad9d680ed1a99a7c856a89991d25d6f7'

class LocationState:
    def __init__(self):
        # commandDictionary :: Dictionary String ((Player, LocationState) -> String)
        self.commandDictionary = dict()
        self.students = list()

    # actOnIntent :: (LocationState, Player, String) -> Maybe String
    def actOnIntent(self, Player, intent):
        if intent in self.commandDictionary:
            return self.commandDictionary[intent](Player, self)
        else:
            return None
        
    def answered(self, studentName):
        for student in self.students:
            if student.name == studentName:
                return student.answered
        return False
        
    def leaveHook(self, player):
        player.lastStudent = None
        pass

class Student:
    def __init__(self, name, firstTalk, subsequentTalk, answeredTalk, answer, answeredCorrect, answeredIncorrect):
        self.name = name
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
        if self.answered:
            return self.answeredTalk
        elif string.strip() == self.correctAnswer: #TODO: Better answer validation
            self.answered = True
            return self.answeredCorrect
        else:
            return self.answeredIncorrect


def makeMoveCommand(locationAccessor, msgString):
    def moveCommand(player, locationState):
        player.location = locationAccessor(player.gameState)
        locationState.leaveHook(player)
        return msgString
    return moveCommand


def selectStudent(player, locationState):
    studentList = locationState.students
    if len(studentList) == 1:
        return studentList[0].talkTo()
    studentNames = list(map(lambda x: x.name, studentList))
    studentString = [] if len(studentNames) == 0 else reduce(lambda a, b: a + ', ' + b, studentNames[1:], studentNames[0])
    if not studentString:
        return "No students are available to talk to." 
    else:
        player.state = PlayerState.CHOOSE_STUDENT
        return ("Which student would you like to talk to: " + studentString + "?")
        
def selectClassroom(player, locationState):
    classDict = locationState.classrooms
    classNames = list(classDict.keys())
    classString = [] if len(classNames) == 0 else reduce(lambda a, b: a + ', ' + b, classNames[1:], classNames[0])
    if not classString:
        return "There are no adjacent classrooms." 
    else:
        player.state = PlayerState.CHOOSE_ROOM
        return ("Which classroom would you like to move to?: " + classString + "?")
