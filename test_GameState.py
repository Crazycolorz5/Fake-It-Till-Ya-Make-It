from GameState import *
from StateBase import *
        
def classroomTest(player, classroom):
    for intent in classroom.commandDictionary:
        classroom.commandDictionary[intent](player, classroom)
        player.state = PlayerState.DEFAULT #Don't bother with traversing decision trees.
    for student in classroom.students:
        student.talkTo()
    #Test the intents again in case talking to a student changes state.
    for intent in classroom.commandDictionary:
        classroom.commandDictionary[intent](player, classroom)
        player.state = PlayerState.DEFAULT #Don't bother with traversing decision trees.

def test_GameState():
    player = Player("Steve Boxwell")
    gs = player.gameState
    for classroom in [gs.BiologyClassroom, gs.MathClassroom, gs.LitClassroom, gs.USHistClassroom, gs.WorldHistClassroom, gs.SciencesHallway, gs.ArtsHallway]:
        classroomTest(player, classroom)
