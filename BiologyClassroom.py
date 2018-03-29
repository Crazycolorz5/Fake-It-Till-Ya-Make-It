from StateBase import *

def biologyClassroomLookaround(player, locationState):
    answeredJohnDoe = locationState.answered("John Doe")
    answeredSamWinchester = locationState.answered("Sam Winchester")
    johnDoeStatus = "There's a student looking at a diagram of cells, loking somewhat confused." if not answeredJohnDoe else "John Doe is sitting at their desk." #TODO: Store this as a flag in the location.
    samWinchesterStatus = "There's a student waiting by the teacher's desk to ask a question." if not answeredSamWinchester else "Sam Winchester has returned to their desk and is waiting for the school day to end."
    deskStatus = "There's a teacher's desk." if not locationState.gotNotes else "There's a teacher's desk, where you got the lecture notes from."
    computerStatus = "There are several computers in the corner of the room, presumably for students to use during a free period." if not locationState.gotWikipedia else "There are several computers, including the one you get the Wikipedia article from. You have to remember to tell your students not to cite Wikipedia."
    door = "There is a door to the hallway."
    return "%s\n%s\n%s\n%s\n%s" % (johnDoeStatus, samWinchesterStatus, deskStatus, computerStatus, door)

def biologyClassroomDesk(player, locationState):
    if locationState.gotNotes:
        return "You've already gotten the lecture notes from the teacher's desk."
    else:
        locationState.gotNotes = True
        player.watson.findDocument(WAR_OF_1812_DOCUMENT)
        return "You open the drawer and grab the lecture notes the regular teacher left you. To reduce prep time, you pull out your phone, take a picture of the notes, and send it to IBM Watson for analysis.\nYou got a document on the War of 1812!"

def biologyClassroomComputer(player, locationState):
    if locationState.gotWikipedia:
        return "You have no further use for the computer at this time."
    elif locationState.students[0].talkedTo: #TODO: Store this as a flag in the location.
        locationState.gotWikipedia = True
        player.watson.findDocument(MITOSIS_DOCUMENT)
        return "As per the student's request, you search the web for an article on mitosis.\nYou grab the Wikipedia page and send it to IBM Watson for analysis.\nYou got a document on mitosis!"
    else:
        return "You have no reason to use a computer at the moment."


biologyClassroomCommands = {
    "move to hallway": makeMoveCommand(lambda gs: gs.Hallway, "You move to the sciences hallway."),
    "talk to student" : selectStudent,
    "look around" : biologyClassroomLookaround,
    "interact with desk" : biologyClassroomDesk,
    "interact with computer" : biologyClassroomComputer
}


def makeBiologyClassroom():
    BiologyClassroom = LocationState()
    
    BiologyClassroom.commandDictionary = biologyClassroomCommands
    
    BiologyClassroom.gotNotes = False
    BiologyClassroom.gotWikipedia = False
    JohnDoe = Student("John Doe",
                        "Hey there Prof! Say, since you're just subbing, could you help me with this question on my Biology homework? What's the final phase of mitosis? (format: all lowercase)",
                        "The question was, what's the final phase of mitosis?",
                        "Thanks for the help!",
                        "telophase",
                        "Yeah, I do think the notes said something like that.",
                        "I don't think that sounds right.")
    SamWinchester = Student("Sam Winchester",
                        "I can't remember what the latin name of the American Black Bear for our homework. Do you remember, Professor? (format: genus species)",
                        "What is the latin name of the American Black Bear?",
                        "Thank you, Professor!",
                        "ursus americanus",
                        "Oh yeah, Ursus Americanus. Thank you!",
                        "I'm not sure that's correct, Professor.")
    BiologyClassroom.students = [JohnDoe, SamWinchester]
    return BiologyClassroom
