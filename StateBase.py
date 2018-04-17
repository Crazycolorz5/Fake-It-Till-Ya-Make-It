from enum import Enum
from functools import *

WAR_OF_1812_DOCUMENT = '98e9b50f1327e045364f669dab17a2ea'
MITOSIS_DOCUMENT = 'ad9d680ed1a99a7c856a89991d25d6f7'
GENERAL_RELATIVITY_DOCUMENT = 'fb37bbd8b218a05f8507af653948ba64'
BLACK_BEAR_DOCUMENT = '41009df362f8fe05beadcfe162c03cdd'
ANCIENT_GREECE_DOCUMENT = 'f2c002562bb849b53180ac628da192f5'
PRESIDENTS_DOCUMENT = '2d43e8f7832fbc02fda4bcfbea514667'
QUADRATIC_EQUATION_DOCUMENT = '27ce78f83dc0d72d96e3f5766736992d'
CIRCLE_DOCUMENT = 'ab7facd3213a7156e24ad5f23548f1fd'
JANE_EYRE_DOCUMENT = '33700eb6b0e66773a97012125ba6d800'
THERMODYNAMICS_DOCUMENT = '62108334cc73caa68c4ef1f21c4c7be3'
TALE_OF_TWO_CITIES_DOCUMENT = '181f74c2c11aede44654b969e5d18676'
THIRTEENTH_AMENDMENT_DOCUMENT = '114ec7d948248dd6ff7fc25f82d1c52a'
WORLD_WAR_I_DOCUMENT = '227192aab28b637c7ad5477d012595d0'

class PlayerState(Enum):
    DEFAULT = 1
    CHOOSE_ROOM = 2
    CHOOSE_STUDENT = 3

class LocationState:
    def __init__(self):
        # commandDictionary :: Dictionary String ((Player, LocationState) -> String)
        self.commandDictionary = dict()
        self.students = list()

    # actOnIntent :: (LocationState, Player, String) -> Maybe String
    def actOnIntent(self, player, intent):
        if intent in self.commandDictionary:
            return self.commandDictionary[intent](player, self)
        for student in self.students:
            if intent.casefold() == student.name.casefold():
                player.lastStudent = student
                return student.talkTo()
        else:
            return None
        
    def answered(self, studentName):
        student = self.findStudent(studentName)
        return False if student == None else student.answered
    
    def allAnswered(self):
        for student in self.students:
            if not student.answered:
                return False
        return True
    
    def leaveHook(self, player):
        player.lastStudent = None
        pass
    
    #Finds student object with given name (case insensitive) if in the location, otherwise gives None
    def findStudent(self, stuName):
        for student in self.students:
            if student.name.casefold() == stuName.casefold(): 
                return student
        return None
        
class HallwayState(LocationState):
    def __init__(self, classrooms):
        self.classrooms = classrooms
        LocationState.__init__(self)
    
    def actOnIntent(self, Player, intent):
        for classroom in self.classrooms:
            if classroom.casefold() == intent.casefold():
                return moveToRoom(Player, classroom, self.classrooms[classroom])
        return LocationState.actOnIntent(self, Player, intent)

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
    def answer(self, player, string): #Intend to overwrite?
        if self.answered:
            return self.answeredTalk
        elif string.strip() == self.correctAnswer: #TODO: Better answer validation
            player.score += 20
            self.answered = True
            return self.answeredCorrect
        else:
            player.score -= 3
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
        return ("Which classroom would you like to move to: " + classString + "?")

def moveToRoom(player, classroomName, location):
    player.location = location
    return "You move to the %s classroom." % classroomName.title()
    
