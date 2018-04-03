from StateBase import *

def literatureClassroomLookaround(player, locationState):
    answeredFrancisBacon = locationState.answered("Francis Bacon")
    answeredKevinPrice = locationState.answered("Kevin Price")
    francisBaconStatus = "Francis is sitting with a paper in front of him, looking like he doesn't know what he is doing" if not answeredFrancisBacon else "Francis Bacon is sitting at their desk." #TODO: Store this as a flag in the location.
    kevinPriceStatus = "Kevin Price is sitting reading a religious text, and not any assigned reading of the class.\nHe seems like he is putting off his work." if not answeredKevinPrice else "Kevin has gone back to reading his Book of Mormon."
    deskStatus = "There's a teacher's desk at the front of the classroom, with a pile of papers on it." if not locationState.gotNotes else "There's a huge desk, where you found the notes on \"A Tale of Two Cities\"."
    computerStatus = "There's a computer on the Teacher's desk that they might use for entering grades and the like." if not locationState.gotWikipedia else "There's a computer on the Teacher's desk, that you used to research \"Jane Eyre\"."
    door = "There is a door to the hallway."
    return "%s\n%s\n%s\n%s\n%s" % (francisBaconStatus, kevinPriceStatus, deskStatus, computerStatus, door)

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
    "move to hallway": makeMoveCommand(lambda gs: gs.ArtsHallway, "You move to the arts hallway."),
    "talk to student" : selectStudent,
    "look around" : literatureClassroomLookaround,
    "interact with desk" : literatureClassroomDesk,
    "interact with computer" : literatureClassroomComputer
}


def makeLiteratureClassroom():
    LiteratureClassroom = LocationState()
    
    LiteratureClassroom.commandDictionary = literatureClassroomCommands
    
    LiteratureClassroom.gotNotes = False
    LiteratureClassroom.gotWikipedia = False
    # Literature classroom student 1
    FrancisBacon = Student("Francis Bacon",
                          "So what year was \"Tale of Two Cities\", by Charles Dickens, published?",
                          "I know, it's confusing to me too. \"Tale of Two Cities\" was published in what year?",
                          "Thanks for your help!",
                          "1859",
                          "That's it! Thanks, Professor! I could have just looked in the book I guess, but I really hate it.",
                          "I don't think that's right.")
    # Literature classroom student 2
    KevinPrice = Student("Kevin Price",
                          "So in \"Jane Eyre\", by Charlotte Bronte, what's the name of the family she moves in with in her childhood?",
                          "What's the name of her uncle's family in \"Jane Eyre\"?",
                          "I wish you were my full time teacher!",
                          "reed",
                          "That's what it was, of course! Thanks!",
                          "I don't think that's the right last name.")
    LiteratureClassroom.students = [FrancisBacon, KevinPrice]
    return LiteratureClassroom
