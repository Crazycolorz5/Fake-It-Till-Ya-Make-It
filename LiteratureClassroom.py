from StateBase import *

def literatureClassroomLookaround(player, locationState):
    answeredFrancisBacon = locationState.answered("Francis Bacon")
    answeredKevinPrice = locationState.answered("Kevin Price")
    francisBaconStatus = "Francis is sitting with a paper in front of him, looking like he doesn't know what he is doing" if not answeredFrancisBacon else "Francis Bacon is sitting at their desk." #TODO: Store this as a flag in the location.
    kevinPriceStatus = "Kevin Price is sitting reading a religious text, and not any assigned reading of the class.\nHe seems like he is putting off his work." if not answeredKevinPrice else "Kevin has gone back to reading his Book of Mormon."
    deskStatus = "There's a teacher's desk at the front of the classroom, with a pile of papers on it." if not locationState.gotNotes else "There's a huge desk, where you found the notes on \"A Tale of Two Cities\"."
    computerStatus = "There's a computer on the Teacher's desk that they might use for entering grades and the like." if not locationState.gotWikipedia else "There's a computer on the Teacher's desk, that you used to research \"Jane Eyre\"."
    door = "There is a door to the hallway."
    return "%s\n%s\n%s\n%s\n%s" % (fancisBaconStatus, kevinPriceStatus, deskStatus, computerStatus, door)

def literatureClassroomDesk(player, locationState):
    if locationState.gotNotes:
        return "You've already gotten the notes from the teacher's desk."
    else:
        locationState.gotNotes = True
        player.watson.findDocument(TALE_OF_TWO_CITIES_DOCUMENT)
        return "You go to the desk and grab the lecture notes the regular teacher left you. To reduce prep time, you pull out your phone, take a picture of the notes, and send it to IBM Watson for analysis.\nYou got a document on the \"A Tale of Two Cities\"!"

def literatureClassroomComputer(player, locationState):
    if locationState.gotWikipedia:
        return "You have no further use for the computer at this time."
    elif locationState.students[0].talkedTo: #TODO: Store this as a flag in the location.
        locationState.gotWikipedia = True
        player.watson.findDocument(JANE_EYRE_DOCUMENT)
        return "As per the student's request, you search the web for an article on mitosis.\nYou grab the Wikipedia page and send it to IBM Watson for analysis.\nYou got a document on \"Jane Eyre\"!"
    else:
        return "You have no reason to use a computer at the moment."


literatureClassroomCommands = {
    "move to hallway": makeMoveCommand(lambda gs: gs.Hallway, "You move to the hallway."),
    "talk to student" : selectStudent,
    "look around" : literatureClassroomLookaround,
    "interact with desk" : literatureClassroomDesk,
    "interact with computer" : literatureClassroomComputer
}


def makeLiteratureClassroom():
    BiologyClassroom = LocationState()
    
    BiologyClassroom.commandDictionary = biologyClassroomCommands
    
    BiologyClassroom.gotNotes = False
    BiologyClassroom.gotWikipedia = False
    JohnDoe = Student("John Doe",
                        "Hey there Prof! Say, since you're just subbing, could you help me with this question on my Literature homework? What's the final phase of mitosis? (format: all lowercase)",
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
