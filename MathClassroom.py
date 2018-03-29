from StateBase import *

def makeMathClassroom():
    
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
                            "In geometry, what's the name of a line segment that has its endpoints on the circle, but is not specifically filling any other requirement?",
                            "You forget already? I asked you, what is the name of a line segment that has its endpoints on a circle?",
                            "You're an alright substitute teacher, I guess.",
                            "univariate",
                            "I already knew that, but thanks anyway. You're not too bad.",
                            "That's not right. You call yourself a substitute teacher?")
    MathClassroom.students = [HoldenCaulfield, SteveBoxwell]

