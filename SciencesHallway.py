from StateBase import *

def sciencesHallwayLookaround(player, locationState):
    return "You are in the sciences hallway.\nThere are neighboring classrooms for the sciences and maths.\nThe arts hallway is on the other end."

sciencesHallwayCommands = {
    "move to hallway" : makeMoveCommand(lambda gs: gs.ArtsHallway, "You move to the arts hallway."),
    "move to classroom" : selectClassroom,
    "look around" : sciencesHallwayLookaround
    }

def makeSciencesHallway(classrooms):
    SciencesHallway = LocationState()
    SciencesHallway.classrooms = classrooms
    Sciences.commandDictionary = sciencesHallwayCommands
    return SciencesHallway
    

