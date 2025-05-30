from StateBase import *

def worldHistoryClassroomLookaround(player, locationState):
    answeredMarieCurie = locationState.answered("Marie Curie")
    answeredRosalindFranklin = locationState.answered("Rosalind Franklin")
    marieCurieStatus = "Marie is studying WWI at her desk." if not answeredMarieCurie else "Marie Curie is sitting at her desk."
    rosalindFranklinStatus = "Rosalind is arguing something about ancient Greece with other students." if not answeredRosalindFranklin else "Rosalind Franklin is waiting for the school day to end, happy to have won her argument."
    backpackStatus = "There's a student's backpack under a chair." if not locationState.gotNotes else "There's a student's backpack, where you got the notes from."
    computerStatus = "There is a computer in the corner of the room."
    door = "There is a door to the hallway."
    return "%s\n%s\n%s\n%s\n%s" % (marieCurieStatus, rosalindFranklinStatus, backpackStatus, computerStatus, door)

def worldHistoryClassroomBackpack(player, locationState):
    if locationState.gotNotes:
        return "You've already gotten the notes taken by another student."
    else:
        locationState.gotNotes = True
        player.watson.findDocument(WORLD_WAR_I_DOCUMENT)
        return "You saw an open backpack under a chair and noticed the notes on WWI sticking out. You grab the notes for scanning, send it to IBM Watson, and quickly put the notes back.\nYou got a document on World War I!"

def worldHistoryClassroomComputer(player, locationState):
    if locationState.gotWikipedia:
        return "You have no further use for the computer at this time."
    else:
        locationState.gotWikipedia = True
        player.watson.findDocument(ANCIENT_GREECE_DOCUMENT)
        return "You search the web and soon found a page on Wikipedia about ancient Greece. You copy the article and send it to IBM Watson for analysis.\nYou got a document on ancient Greece!"


worldHistoryClassroomCommands = {
    "move to hallway": makeMoveCommand(lambda gs: gs.ArtsHallway, "You move to the arts hallway."),
    "talk to student" : selectStudent,
    "look around" : worldHistoryClassroomLookaround,
    "interact with backpack" : worldHistoryClassroomBackpack,
    "interact with computer" : worldHistoryClassroomComputer
}


def makeWorldHistoryClassroom():
    WorldHistoryClassroom = LocationState()
    
    WorldHistoryClassroom.commandDictionary = worldHistoryClassroomCommands
    
    WorldHistoryClassroom.gotNotes = False
    WorldHistoryClassroom.gotWikipedia = False
    MarieCurie = Student("Marie Curie",
                          "Hey, this question is kinda specific. Who was the German emperor during WWI? (format: title lastname suffix)",
                          "I can't remember who the emperor of Germany during WWI was. Can you help?",
                          "Neat-o, professor! Thanks!",
                          "kaiser wilhelm ii",
                          "That sounds right... At least it sounds German. Thanks!",
                          "That doesn't sound like the right person...")
    RosalindFranklin = Student("Rosalind Franklin",
                          "Okay, so in Ancient Greece, they used some sort of coin with an owl on it. Who was the goddess on the other side?",
                          "What is the name of the goddess on the coins in Ancient Greece?",
                          "Thanks so much, Professor!",
                          "athena",
                          "Yeah! The one that like busted out of Zeus's head or something! Thanks!",
                          "Hm, that doesn't sound like the right Greek goddess.")
    WorldHistoryClassroom.students = [MarieCurie, RosalindFranklin]
    return WorldHistoryClassroom
