from StateBase import *

def mathClassroomLookaround(player, locationState):
    answeredJohnDoe = locationState.answered("John Doe")
    answeredSamWinchester = locationState.answered("Sam Winchester")
    johnDoeStatus = "There's a student looking at a diagram of cells, loking somewhat confused." if not answeredJohnDoe else "John Doe is sitting at their desk." #TODO: Store this as a flag in the location.
    samWinchesterStatus = "There's a student waiting by the teacher's desk to ask a question." if not answeredSamWinchester else "Sam Winchester has returned to their desk and is waiting for the school day to end."
    deskStatus = "There's a teacher's desk." if not locationState.gotNotes else "There's a teacher's desk, where you got the lecture notes from."
    computerStatus = "There are several computers in the corner of the room, presumably for students to use during a free period." if not locationState.gotWikipedia else "There are several computers, including the one you get the Wikipedia article from. You have to remember to tell your students not to cite Wikipedia."
    door = "There is a door to the hallway."
    return "%s\n%s\n%s\n%s\n%s" % (johnDoeStatus, samWinchesterStatus, deskStatus, computerStatus, door)

def mathClassroomDesk(player, locationState):
    if locationState.gotNotes:
        return "You've already gotten the lecture notes from the teacher's desk."
    else:
        locationState.gotNotes = True
        player.watson.findDocument(WAR_OF_1812_DOCUMENT)
        return "You open the drawer and grab the lecture notes the regular teacher left you. To reduce prep time, you pull out your phone, take a picture of the notes, and send it to IBM Watson for analysis.\nYou got a document on the War of 1812!"

def mathClassroomComputer(player, locationState):
    if locationState.gotWikipedia:
        return "You have no further use for the computer at this time."
    elif locationState.students[0].talkedTo: #TODO: Store this as a flag in the location.
        locationState.gotWikipedia = True
        player.watson.findDocument(MITOSIS_DOCUMENT)
        return "As per the student's request, you search the web for an article on mitosis.\nYou grab the Wikipedia page and send it to IBM Watson for analysis.\nYou got a document on mitosis!"
    else:
        return "You have no reason to use a computer at the moment."

mathClassroomCommands = {
    "move to hallway": makeMoveCommand(lambda gs: gs.Hallway, "You move to the hallway."),
    "talk to student" : selectStudent,
    "look around" : biologyClassroomLookaround,
    "interact with desk" : biologyClassroomDesk,
    "interact with computer" : biologyClassroomComputer
}


def makeMathClassroom():
    MathClassroom = LocationState()
    
    MathClassroom.backpackNotes = False
    
    MathClassroom.commandDictionary = classroomCommands
    
    # Math classroom student 1
    HoldenCaulfield = Student("Holden Caulfield",
                            "So apparently the quadratic equation is a special equation, because it contains only one unknown. What's the word for that?",
                            "What is the name of a math function that contains only one unknown?",
                            "Thanks for the help!",
                            "univariate",
                            "That makes sense, like one variable. Thanks!",
                            "Math already doesn't make much sense, but I don't think that's right.")
    # Math classroom student 2
    SteveBoxwell = Student("Steve Boxwell",
                            "In geometry, what's the name of a line segment that has its endpoints on the circle, but is not specifically filling any other requirement?\nNeed help? I'll let you look at my notes. They're in my backpack.",
                            "You forget already? I asked you, what is the name of a line segment that has its endpoints on a circle?",
                            "You're an alright substitute teacher, I guess. My hoverboard is full of eels.",
                            "univariate",
                            "I already knew that, but thanks anyway. You're not too bad.",
                            "That's not right. You call yourself a substitute teacher?")
    MathClassroom.students = [HoldenCaulfield, SteveBoxwell]

