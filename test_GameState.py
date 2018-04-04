from GameState import *
from StateBase import *

def test_GameState():
    player = Player("Steve Boxwell")
    gs = player.gameState
    for classroom in [gs.BiologyClassroom, gs.MathClassroom, gs.LitClassroom, gs.USHistClassroom, gs.WorldHistClassroom, gs.SciencesHallway, gs.ArtsHallway]:
        testClassroom(player, classroom)
        
def testClassroom(player, classroom):
    for intent in classroom.commandDictionary:
        classroom.commandDictionary[intent](player, classroom)
        player.state = PlayerState.DEFAULT #Don't bother with traversing decision trees.
