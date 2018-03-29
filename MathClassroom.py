from StateBase import *

def mathClassroomLookaround(player, locationState):
    steve = locationState.findStudent("Steve Boxwell")
    if steve.answered:
        steveString = "Steve is sitting at his desk. You think he's looking a bit smug. Maybe it's the fact that he has a hovercraft."
    elif steve.talkedTo:
        steveString = "Steve is impatiently waiting at his desk. His backpack is on the floor next to him."
    else:
        steveString = "Steve is sitting at his desk, playing remotely with a hovercraft."

def mathBackpack(player, locationState):
    pass

mathClassroomCommands = {
    "move to hallway": makeMoveCommand(lambda gs: gs.Hallway, "You move to the sciences hallway."),
    "talk to student" : selectStudent,
    "look around" : mathClassroomLookaround,
    "interact with backpack" : mathBackpack
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
                            "You're an alright substitute teacher, I guess. My hovercraft is full of eels.",
                            "univariate",
                            "I already knew that, but thanks anyway. You're not too bad.",
                            "That's not right. You call yourself a substitute teacher?")
    MathClassroom.students = [HoldenCaulfield, SteveBoxwell]

