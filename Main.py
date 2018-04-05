# coding=utf-8
from Discovery import *
import websockets
import asyncio
import _thread
from GameState import Player
from sys import argv

class IOHandler:
    def out(self, string):
        raise NotImplementedError()
    def inp(self):
        raise NotImplementedError()
        
class Console(IOHandler):
    async def out(self, string): 
        print(string)
    async def inp(self): 
        return input(">> ")
    def multiInstance(self):
        return False

class WebsocketHandler(IOHandler):
    def __init__(self, websocket):
        self.websocket = websocket
    async def out(self, string):
        await self.websocket.send(string)
    async def inp(self):
        return await self.websocket.recv()
    def multiInstance(self):
        return True

async def websocketHandler(websocket, path):
    print('new connection')
    await gameLoop(WebsocketHandler(websocket))
    print('websocket closed')
    websocket.close()


async def gameLoop(handler):
    try:
        await handler.out("Welcome to Washington High School! Please input your name:")
        name = await handler.inp()
        player = Player(name)
        await handler.out("Nice to meet you, %s. \nGood luck as your first day as a substitute teacher!" % player.name)
        await handler.out("You enter the hallway outside the sciences classrooms.")
        await handler.out("You worry for a second that you won't be able to remember any students' names, but luckily you have all the class rosters!")
        await handler.out("Type help for a few possible commands, or look around to get started!")

        while True:
            currentLine = await handler.inp()
            currentCommand = currentLine.lower()
            if "quit" == currentCommand:
                if handler.multiInstance():
                    return
                else:
                    quit()
            await handler.out(player.act(currentCommand))

    except websockets.exceptions.ConnectionClosed as e:
        return


if "--websocket" in argv:
    handler = websockets.serve(websocketHandler, None, 10000)
    print('websocket running')
else:
    handler = asyncio.ensure_future(gameLoop(Console()))

loop = asyncio.get_event_loop()
asyncio.ensure_future(handler)
_thread.start_new_thread(loop.run_forever())
