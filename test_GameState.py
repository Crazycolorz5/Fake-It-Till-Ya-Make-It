from GameState import *
from Discovery import *

def test_Player_act():
    player = PlayerState("Steve Boxwell")
    '''
    query = ''
    result = player.act(query)
    assert result == "No command specified!"
    '''
    query = 'help'
    result = player.act(query)
    assert result == player.helpString
    
    wat = Watson()
    query = 'query war of 1812'
    result = player.act(query)
    assert result == formatResponse(wat.ask(query))
    '''
    query = 'move to the room'
    result = player.act(query)
    assert result == 'move to classroom'
    
    query = 'move to hallway'
    result = player.act(query)
    assert result == 'move to hallway'
    
    query = 'walk to student'
    result = player.act(query)
    assert result == 'talk to student'
    '''