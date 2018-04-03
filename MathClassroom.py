from StateBase import *

def mathClassroomLookaround(player, locationState):
    steve = locationState.findStudent("Steve Boxwell")
    if steve.answered:
        steveString = "Steve is sitting at his desk. You think he's looking a bit smug. Maybe it's the fact that he has a hovercraft."
    elif steve.talkedTo:
        steveString = "Steve is impatiently waiting at his desk. His backpack is on the floor next to him."
    else:
        steveString = "Steve is sitting at his desk, playing remotely with a hovercraft."
    holden = locationState.findStudent("Holden Caulfield")
    if holden.answered:
        holdenString = "Holden is waiting impatiently for class to start."
    else:
        holdenString = "Holden is at his desk, studying a bit before class. He seems confused."
    deskString = "The teacher's desk is at the front of the room."
    doorString = "The door to the sciences hallway is near the teacher's desk."
    return "%s\n%s\n%s\n%s" % (steveString, holdenString, deskString, doorString)

def mathBackpack(player, locationState):
    if locationState.backpackNotes:
        return "You have no further reason to search Steve Boxwell's backpack."
    elif locationState.findStudent("Steve Boxwell").talkedTo:
        locationState.backpackNotes = True
        player.watson.findDocument(CIRCLE_DOCUMENT)
        return "You take Steve Boxwell's notes on circles. You attempt to read it, but\nthen decide to just send it to Watson to make sense of the handwriting automatically.\nYou got a document on circles!"
    else:
        return "You shouldn't be going through students' personal belongings without their permission."

def mathDesk(player, locationState):
    if locationState.deskNotes:
        return "You've already retrieved today's lesson plan."
    else:
        locationState.deskNotes = True
        player.watson.findDocument(QUADRATIC_EQUATION_DOCUMENT)
        return "You open the teacher's desk to get the day's lesson plan.\nYou send it to Watson for instant analysis.\nYou got a document on the quadratic formula!"

mathClassroomCommands = {
    "move to hallway": makeMoveCommand(lambda gs: gs.SciencesHallway, "You move to the sciences hallway."),
    "talk to student" : selectStudent,
    "look around" : mathClassroomLookaround,
    "interact with backpack" : mathBackpack,
    "interact with desk" : mathDesk
}


def makeMathClassroom():
    MathClassroom = LocationState()
    
    MathClassroom.backpackNotes = False
    MathClassroom.deskNotes = False;
    
    MathClassroom.commandDictionary = mathClassroomCommands
    
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
                            "You're an alright substitute teacher, I guess. My hovercraft is full of eels.",
                            "chord",
                            "I already knew that, but thanks anyway. You're not too bad.",
                            "That's not right. You call yourself a substitute teacher?")
    MathClassroom.students = [HoldenCaulfield, SteveBoxwell]
    return MathClassroom

