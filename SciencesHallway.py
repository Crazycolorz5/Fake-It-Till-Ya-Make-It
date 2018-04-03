from StateBase import *

def sciencesHallwayLookaround(player, locationState):
    status = "There is a Math classroom, a Physics classroom, and a Biology classroom in this hallway.\nThere is also a door to the Arts hallway."
    return "%s" % (status)


sciencesHallwayCommands = {
    "move to classroom" : makeMoveCommand(lambda gs: gs.BiologyClassroom, "You move to the biology classroom."), #TODO: Ask which classroom once we have more.
    "talk to student" : selectStudent,
    "look around" : hallwayLookaround
    }


def makeSciencesHallway():
    SciencesHallway = LocationState()
    
    SciencesHallway.commandDictionary = sciencesHallwaycommands
    
    return SciencesHallway
    

