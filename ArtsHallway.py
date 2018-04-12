from StateBase import *

def artHallwayLookaround(player, locationState): 
    return "You are in the arts hallway.\nThere are neighboring classrooms for the social sciences & language arts.\nThe sciences hallway is on the other end."
    
artHallwayCommands = {
    "move to hallway" : makeMoveCommand(lambda gs: gs.SciencesHallway, "You move to the sciences hallway."),
    "move to classroom" : selectClassroom,
    "look around" : artHallwayLookaround
    }

def makeArtsHallway(classrooms):
    ArtsHallway = LocationState()
    ArtsHallway.classrooms = classrooms
    ArtsHallway.commandDictionary = artHallwayCommands
    
    return ArtsHallway
