from StateBase import *

def physicsClassroomLookaround(player, locationState):
	answeredBettyWhite = locationState.answered("Betty White")
    answeredCharlesDickens = locationState.answered("Charles Dickens")
	bettyWhiteStatus =  "There is a student looking at relations between heat and other forms of energy, looking somewhat confused" if not answeredBettyWhite else "Betty white is sitting at their desk"
	charlesDickensStatus = "There is a student looking at Laws of relativity, looking somewhat confused" if not answeredCharlesDickens else "Charles Dickens is sitting at their desk"
	deskStatus = "There's a teacher's desk." if not locationState.gotNotes else "There's a teacher's desk, where you got the lecture notes from."
    computerStatus = "There are several computers in the corner of the room, presumably for students to use during a free period." if not locationState.gotWikipedia else "There are several computers, including the one you get the Wikipedia article from. You have to remember to tell your students not to cite Wikipedia."
    door = "There is a door to the hallway."
    return "%s\n%s\n%s\n%s\n%s" % (bettyWhiteStatus,charlesDickensStatus,deskStatus,computerStatus,door)
	
def physicsClassroomDesk(player, locationState):
    if locationState.gotNotes:
        return "You've already gotten the lecture notes from the teacher's desk."
    else:
        locationState.gotNotes = True
        player.watson.findDocument(THERMODYNAMICS_DOCUMENT)
        return "You open the drawer and grab the lecture notes the regular teacher left you. To reduce prep time, you pull out your phone, take a picture of the notes, and send it to IBM Watson for analysis.\nYou got a document on the THERMODYNAMICS document!"

def physicsClassroomComputer(player, locationState):
    if locationState.gotWikipedia:
        return "You have no further use for the computer at this time."
    elif locationState.students[0].talkedTo: #TODO: Store this as a flag in the location.
        locationState.gotWikipedia = True
        player.watson.findDocument(GENERAL_RELATIVITY_DOCUMENT)
        return "As per the student's request, you search the web for an article on general relativity.\nYou grab the Wikipedia page and send it to IBM Watson for analysis.\nYou got a document on general relativity!"
    else:
        return "You have no reason to use a computer at the moment."


physicsClassroomCommands = {
    "move to hallway": makeMoveCommand(lambda gs: gs.Hallway, "You move to the hallway."),
    "talk to student" : selectStudent,
    "look around" : physicsClassroomLookaround,
    "interact with desk" : physicsClassroomDesk,
    "interact with computer" : physicsClassroomComputer
}


def makephysicsClassroom():
    physicsClassroom = LocationState()
    
    physicsClassroom.commandDictionary = physicsClassroomCommands
    
    physicsClassroom.gotNotes = False
    physicsClassroom.gotWikipedia = False
	BettyWhite = Student("Betty White",
                              "What's the name of the person that found the theory of general relativity? (format: first last)",
                              "Do you know the scientist who found the theory of general relativity? He's got, like, crazy hair, or something?",
                              "Thank you!",
                              "albert einstein",
                              "Oh yeah, it was him! Thank you!",
                              "That doesn't sound familiar, Professor.")
    # Physics classroom student 2
    CharlesDickens = Student("Charles Dickens",
                              "Hey there, Professor. Do you know what quantity is defined by the second law of thermodynamics?",
                              "The first law of thermodynamics is the one about equal and opposite reactions, I think. What does the second define?",
                              "You're the greatest substitute ever, thanks!",
                              "entropy",
                              "Yeah, entropy! Thanks, Professor!",
                              "I think it was something else.")
    physicsClassroom.students = [BettyWhite, CharlesDickens]
    return physicsClassroom
