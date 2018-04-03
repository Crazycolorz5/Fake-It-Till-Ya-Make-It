from StateBase import *

def USHistoryClassroomLookaround(player, locationState):
    answeredLinManuelMiranda = locationState.answered("Lin-Manuel Miranda")
    answeredElizabethRoss = locationState.answered("Elizabeth Ross")
    answeredFrankPierce = locationState.answered("Frank Pierce")
    linManuelMirandaStatus = "Lin-Manuel is looking suspiciously into a History textbook." if not answeredLinManuelMiranda else "Lin-Manuel is sitting satisfied at his desk."
    elizabethRossStatus = "Elizabeth is sitting in class, sewing for some reason." if not answeredElizabethRoss else "Elizabeth is sewing contentedly."
    frankPierceStatus = "Frank is looking at a textbook with a picture of a train." if not answeredFrankPierce else "Frank is now looking at a picture of the 14th President of the United States."
    deskStatus = "There's a desk by the blackboard with some papers on it." if not locationState.gotNotesFromDesk else "There's a teacher's desk, with a pretty apple on it."
    podiumStatus = "There is a podium by the front of the room, where the teacher presumably lectures from. What it is doing in a high school classroom is anyone's guess." if not locationState.gotNotesFromPodium else "There is the podium where you found the notes on the War of 1812."
    bookshelfStatus = "There is a rather tall bookshelf in the back of the classroom." if not locationState.gotNotesFromPodium else "There is the tall bookshelf you visited earlier."
    door = "There is a door to the hallway."
    return "%s\n%s\n%s\n%s\n%s\n%s\n%s" % (linManuelMirandaStatus, elizabethRossStatus, frankPierceStatus, deskStatus, podiumStatus, bookshelfStatus, door)

def USHistoryClassroomDesk(player, locationState):
    if locationState.gotNotesFromDesk:
        return "The only thing left on the teacher's desk is a lovely red apple."
    else:
        locationState.gotNotesFromDesk = True
        player.watson.findDocument(PRESIDENTS_DOCUMENT)
        return "Under some ungraded tests lies a printed out Wikipedia article on the Presidents of the U.S.\nYou are confused by this teacher's methods, but don't concern yourself with it too much.\nYou got a document on the U.S. Presidents!"

        
def USHistoryClassroomPodium(player, locationState):
    if locationState.gotNotesFromPodium:
        return "There is nothing else at the podium you can see."
    else:
        locationState.gotNotesFromPodium = True
        player.watson.findDocument(WAR_OF_1812_DOCUMENT)
        return "There are some notes on the War of 1812 sitting on the podium, so you grab them and load them into Watson.\nYou got a document on the War of 1812!"

def USHistoryClassroomBookshelf(player, locationState):
    if locationState.gotNotesFromBookshelf:
        return "You look on top of the bookshelf, but you see nothing else of importance."
    else:
        locationState.gotNotesFromBookshelf = True
        player.watson.findDocument(THIRTEENTH_AMENDMENT_DOCUMENT)
        return "You get on your tiptoes to peek at the top of a bookshelf, and see some papers scattered around up there.\nYou got a document on the 13th Amendment!"

USHistoryClassroomCommands = {
    "move to hallway": makeMoveCommand(lambda gs: gs.Hallway, "You move to the hallway."),
    "talk to student" : selectStudent,
    "look around" : USHistoryClassroomLookaround,
    "interact with desk" : USHistoryClassroomDesk,
    "interact with podium" : USHistoryClassroomPodium,
    "interact with bookshelf" : USHistoryClassroomBookshelf
}


def makeUSHistoryClassroom():
    USHistoryClassroom = LocationState()
    
    USHistoryClassroom.commandDictionary = USHistoryClassroomCommands
    
    USHistoryClassroom.gotNotesFromBookshelf = False
    USHistoryClassroom.gotNotesFromPodium = False
    USHistoryClassroom.gotNotesFromDesk = False
    # US History classroom student 1
    LinManuelMiranda = Student("Lin-Manuel Miranda",
                      "Hey Prof, I have a question. What date was the treaty of Ghent signed, ending the War of 1812? (format: MM/DD/YYYY)",
                      "To repeat my question, what date was the treaty of Ghent signed? (format: MM/DD/YYYY)",
                      "Thank you for answering my question!",
                      '12/24/1814',
                      "Thanks for that answer!",
                      "Hm, I don't think that's quite right...")
    # US History classroom student 2
    ElizabethRoss = Student("Elizabeth Ross",
                          "Hey Professor, I'm really bad with dates. What date was the 13th Amendment ratified? (format: MM/DD/YYYY)",
                          "What was my question? I'm asking what date the 13th Amendment was ratified.",
                          "Thanks so much!",
                          "12/06/1865",
                          "That doesn't sound super familiar, but I'll trust you, thanks Professor!",
                          "I'm not entirely sure, but that doesn't sound like the right answer.")
    # US History classroom student 3
    FrankPierce = Student("Frank Pierce",
                          "Hi! So, how many people have served as the President of the U.S.? Like, total?",
                          "Hi again. If it isn't too much trouble, how many people have been president?",
                          "You're the best!",
                          "44",
                          "Oh, I should have known that! Thank you!",
                          "Are you sure?")
    USHistoryClassroom.students = [LinManuelMiranda, ElizabethRoss, FrankPierce]
    return USHistoryClassroom
